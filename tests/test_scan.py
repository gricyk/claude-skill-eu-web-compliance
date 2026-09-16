import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import scan  # noqa: E402

FIXTURES = os.path.join(HERE, "fixtures")


def by_file(results):
    return {r["file"].replace(os.sep, "/"): r for r in results}


class ScanFixtureSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = by_file(scan.scan(os.path.join(FIXTURES, "site"), ["example.com"]))
        cls.index = cls.results["index.html"]

    def test_external_requests_exclude_own_domain_and_subdomains(self):
        external = self.index["external_requests"]
        self.assertTrue(any("googletagmanager.com" in u for u in external))
        self.assertTrue(any("youtube.com/embed" in u for u in external))
        self.assertFalse(any("example.com" in u for u in external))

    def test_css_urls_and_imports(self):
        css = self.results["assets/style.css"]
        self.assertEqual(css["external_requests"], ["https://fonts.googleapis.com/css2?family=Roboto"])
        self.assertIn("third_party_embeds", css)

    def test_tracking_embeds_ai_and_user_content(self):
        self.assertIn("cookie_or_tracking_code", self.index)
        self.assertIn("third_party_embeds", self.index)
        self.assertIn("ai_related_code", self.index)
        self.assertIn("user_content_features", self.index)
        chat = self.results["assets/chat.js"]
        self.assertIn("ai_related_code", chat)
        self.assertIn("cookie_or_tracking_code", chat)

    def test_forms(self):
        forms = self.index["forms"]
        self.assertEqual(forms["count"], 1)
        # name (placeholder only) and textarea are unlabeled; hidden, labeled and aria-labeled fields are not.
        self.assertEqual(forms["fields_without_matching_label"], 2)
        self.assertEqual(forms["prechecked_checkboxes_or_radios"], 1)
        self.assertIn("textarea", forms["field_types"])

    def test_accessibility_signals(self):
        self.assertEqual(self.index["images_missing_alt"], 1)
        self.assertEqual(self.index["clickable_non_button_elements"], 1)
        self.assertEqual(self.index["heading_level_skips"], ["h1->h3"])
        self.assertTrue(self.index["html_missing_lang"])
        self.assertTrue(self.index["missing_viewport_meta"])

    def test_non_markup_files_skip_markup_checks(self):
        self.assertNotIn("forms", self.results["assets/chat.js"])


class ParseAttrs(unittest.TestCase):
    def test_quoted_unquoted_and_bare(self):
        attrs = scan.parse_attrs(' src=/images/logo.svg alt width=32 title="A title" data-x=\'y\'')
        self.assertEqual(attrs, {"src": "/images/logo.svg", "alt": None, "width": "32",
                                 "title": "A title", "data-x": "y"})

    def test_jsx_and_template_blocks(self):
        attrs = scan.parse_attrs(' checked={true} htmlFor={"email"} {{ with .rel }}rel="{{ . }}"{{ end }}')
        self.assertEqual(attrs["checked"], "true")
        self.assertEqual(attrs["htmlfor"], "email")
        self.assertEqual(attrs["rel"], "{{ . }}")
        self.assertNotIn("with", attrs)

    def test_first_occurrence_wins(self):
        self.assertEqual(scan.parse_attrs(" lang=cs lang=en")["lang"], "cs")


class ScanMinifiedSite(unittest.TestCase):
    def test_minified_dirty_site_has_same_findings_as_formatted(self):
        formatted = by_file(scan.scan(os.path.join(FIXTURES, "site"), ["example.com"]))
        minified = by_file(scan.scan(os.path.join(FIXTURES, "minified-site"), ["example.com"]))
        self.assertEqual(minified, formatted)

    def test_minified_clean_site_has_no_findings(self):
        # lang=cs, name=viewport, bare alt, JSON-LD with YouTube/Maps URLs, plain links to Maps and
        # YouTube, a commented-out <img>, and "1<2" inside an inline script.
        self.assertEqual(scan.scan(os.path.join(FIXTURES, "minified-clean-site"), ["example.com"]), [])

    def test_empty_lang_is_missing(self):
        for html in ("<html lang>", "<html lang=\"\">"):
            finding = scan.analyze_file("x.html", html + "<meta name=viewport>", [])
            self.assertTrue(finding["html_missing_lang"], html)


class ScanMarkupDetails(unittest.TestCase):
    def analyze(self, html, path="x.html"):
        return scan.analyze_file(path, html, ["example.com"]) or {}

    def test_links_are_not_embeds(self):
        finding = self.analyze('<a href="https://www.google.com/maps/place/X">Map</a>'
                               '<a href=https://www.youtube.com/watch?v=1>Video</a>')
        self.assertEqual(finding, {})

    def test_auto_loaded_resources_are_embeds(self):
        finding = self.analyze('<link rel=preconnect href=https://fonts.gstatic.com>'
                               '<img srcset="https://maps.googleapis.com/a.png 1x, /b.png 2x" alt>'
                               '<div style="background:url(//www.youtube.com/embed/x)"></div>')
        self.assertEqual(finding["external_requests"], ["https://fonts.gstatic.com",
                                                        "https://maps.googleapis.com/a.png",
                                                        "https://www.youtube.com/embed/x"])
        self.assertEqual(len(finding["third_party_embeds"]), 3)

    def test_script_injected_embed_in_inline_script(self):
        finding = self.analyze("<script>var s=document.createElement('script');"
                               "s.src='https://www.google.com/recaptcha/api.js'</script>")
        self.assertIn("recaptcha", finding["third_party_embeds"])

    def test_consent_gated_script_is_reported_separately(self):
        finding = self.analyze('<script type="text/plain" data-category="analytics" '
                               'src="https://www.googletagmanager.com/gtag/js?id=G-1"></script>')
        self.assertNotIn("external_requests", finding)
        self.assertEqual(finding["consent_gated_requests"], ["https://www.googletagmanager.com/gtag/js?id=G-1"])
        self.assertIn("cookie_or_tracking_code", finding)

    def test_external_form_target(self):
        finding = self.analyze('<form action=https://formspree.io/f/abc><label>Email '
                               '<input type=email name=email></label></form>')
        self.assertEqual(finding["external_form_targets"], ["https://formspree.io/f/abc"])
        self.assertEqual(finding["forms"]["fields_without_matching_label"], 0)  # wrapped in <label>

    def test_jsx_forms(self):
        finding = self.analyze('<form><label htmlFor="news">News</label>'
                               '<input type="checkbox" id="news" checked={isOn} />'
                               '<input type="checkbox" aria-label="Terms" defaultChecked />'
                               '<div onClick={() => open()}>Menu</div></form>', path="x.jsx")
        self.assertEqual(finding["forms"]["prechecked_checkboxes_or_radios"], 1)
        self.assertEqual(finding["forms"]["fields_without_matching_label"], 0)
        self.assertEqual(finding["clickable_non_button_elements"], 1)


class ScanStaticSiteGenerator(unittest.TestCase):
    ROOT = os.path.join(FIXTURES, "ssg-site")

    def test_templates_and_plain_links(self):
        files = by_file(scan.scan(self.ROOT, ["example.com"]))
        self.assertNotIn("layouts/_partials/nav-link.html", files)  # plain <a href> to Google Maps
        self.assertNotIn("layouts/_default/baseof.html", files)  # lang="{{ ... }}" counts as set

    def test_build_output_next_to_sources_is_detected(self):
        self.assertEqual(scan.build_output_dirs_next_to_sources(self.ROOT), ["public"])
        self.assertEqual(scan.build_output_dirs_next_to_sources(self.ROOT, ["public"]), [])
        # Scanning the build output alone is the recommended way and gives no warning.
        self.assertEqual(scan.build_output_dirs_next_to_sources(os.path.join(self.ROOT, "public")), [])

    def test_exclude(self):
        files = set(by_file(scan.scan(self.ROOT, ["example.com"], ["public", "*.dc.html"])))
        self.assertEqual(files, {"layouts/index.html"})
        files = set(by_file(scan.scan(self.ROOT, ["example.com"], ["design/*", "layouts"])))
        self.assertEqual(files, {"public/index.html"})


class ScanCleanSite(unittest.TestCase):
    def test_clean_site_has_no_findings(self):
        self.assertEqual(scan.scan(os.path.join(FIXTURES, "clean-site"), ["example.com"]), [])


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "scan.py"), *args],
                              capture_output=True, text=True)

    def test_json_output(self):
        proc = self.run_cli(os.path.join(FIXTURES, "site"), "--domain", "example.com", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIsInstance(json.loads(proc.stdout), list)

    def test_summary_output(self):
        proc = self.run_cli(os.path.join(FIXTURES, "site"), "--domain", "example.com")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("pre-checked checkboxes/radios: 1", proc.stdout)

    def test_build_output_warning_goes_to_stderr(self):
        root = os.path.join(FIXTURES, "ssg-site")
        proc = self.run_cli(root, "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("public/", proc.stderr)
        self.assertEqual(len(json.loads(proc.stdout)), 3)
        proc = self.run_cli(root, "--json", "--exclude", "public")
        self.assertEqual(proc.stderr, "")

    def test_missing_directory(self):
        proc = self.run_cli(os.path.join(FIXTURES, "does-not-exist"))
        self.assertEqual(proc.returncode, 1)


class ExampleOutput(unittest.TestCase):
    def test_saved_example_scan_is_up_to_date(self):
        examples = os.path.join(ROOT, "examples")
        proc = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "scan.py"), "cafe-site",
                               "--domain", "example.com"], capture_output=True, text=True, cwd=examples)
        with open(os.path.join(examples, "cafe-site-scan.txt"), encoding="utf-8") as f:
            self.assertEqual(proc.stdout, f.read(),
                             "examples/cafe-site-scan.txt is stale, regenerate it (see examples/README.md)")


if __name__ == "__main__":
    unittest.main()
