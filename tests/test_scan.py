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
