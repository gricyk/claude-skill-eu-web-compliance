#!/usr/bin/env python3
"""
scan.py: fast, dependency-free structural scan of a website's source for
EU-compliance-relevant signals (GDPR / ePrivacy / AI Act / DSA / accessibility).

This is a lead generator, not a verdict. It uses regex heuristics on raw
source text, it does not execute JS or render pages, so it can both miss
things (cookies set only at runtime by a bundled script) and over-flag
things (a false-positive match inside a comment or string). Confirm every
material finding by actually reading the relevant file before including it
in a report.

Usage:
    python3 scan.py /path/to/site/root [--domain example.com ...] [--exclude PATTERN ...] [--json]

--domain can be passed several times, it excludes the site's own domain(s)
(and their subdomains) from the external-request list.

--exclude can be passed several times. Each glob pattern is matched against
the path relative to the root and against the file or directory name, e.g.
--exclude public --exclude "design/*" --exclude "*.dc.html".

Minified HTML (unquoted attribute values, bare boolean attributes such as
`alt` or `checked`) is supported. For static site generators, scan the built
output rather than the templates.

Only depends on the Python standard library, so it runs anywhere without
setup.
"""

import argparse
import fnmatch
import json
import os
import re
import sys
from urllib.parse import urlparse

SOURCE_EXTENSIONS = {
    ".html", ".htm", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".vue", ".php", ".astro", ".svelte",
    ".css", ".scss", ".twig", ".liquid", ".hbs", ".njk", ".ejs", ".erb", ".jinja", ".j2",
}
MARKUP_EXTENSIONS = {
    ".html", ".htm", ".php", ".vue", ".astro", ".svelte", ".jsx", ".tsx",
    ".twig", ".liquid", ".hbs", ".njk", ".ejs", ".erb", ".jinja", ".j2",
}
SKIP_DIRS = {"node_modules", ".git", ".next", ".nuxt", ".svelte-kit", "vendor", ".venv", "__pycache__",
             "coverage"}
# Typical output folders of site generators and bundlers. They are scanned, but a warning is
# printed when they sit next to sources, because findings are then reported twice.
BUILD_OUTPUT_DIRS = {"public", "dist", "build", "_site", "out"}

# Tags and attributes. Values may be double-quoted, single-quoted, unquoted (minified HTML),
# a JSX expression in braces, or absent (bare boolean attribute). Template blocks such as
# {{ if .x }} between attributes are skipped.
BRACES = r"\{(?:[^{}]|\{[^{}]*\})*\}"
RE_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
RE_RAW_TEXT = re.compile(r"<(script|style)\b((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>(.*?)</\1\s*>",
                         re.IGNORECASE | re.DOTALL)
RE_TAG = re.compile(r"<([a-zA-Z][\w:.-]*)((?:[^>\"'{}]|\"[^\"]*\"|'[^']*'|" + BRACES + r")*)>")
RE_ATTR = re.compile(r"(" + BRACES + r")|([^\s\"'<>/={}]+)(?:\s*=\s*(\"[^\"]*\"|'[^']*'|" + BRACES +
                     r"|[^\s\"'=<>`]+))?")
RE_LABEL_BLOCK = re.compile(r"<label\b(?:[^>\"']|\"[^\"]*\"|'[^']*')*>.*?</label\s*>", re.IGNORECASE | re.DOTALL)
RE_HEADING = re.compile(r"<h([1-6])(?=[\s>/])", re.IGNORECASE)

RE_CSS_URL = re.compile(r'(?:url\(\s*["\']?|@import\s+["\'])((?:https?:)?//[^"\')\s]+)', re.IGNORECASE)
RE_JS_SRC_ASSIGN = re.compile(r'\.src\s*=\s*["\'`]((?:https?:)?//[^"\'`\s]+)', re.IGNORECASE)

# Tags whose src is fetched automatically when the page loads.
SRC_TAGS = {"script", "iframe", "frame", "img", "audio", "video", "source", "embed", "track", "input"}
# <link rel> values that make the browser contact the href host without a click.
AUTO_LOAD_RELS = {"stylesheet", "preload", "modulepreload", "prefetch", "preconnect", "dns-prefetch", "icon",
                  "apple-touch-icon", "mask-icon", "manifest"}
# Script types that are executed; others (JSON-LD, templates, consent-gated text/plain) are not.
EXECUTABLE_SCRIPT_TYPES = {"", "text/javascript", "application/javascript", "module"}
CONSENT_GATED_SCRIPT_TYPES = {"text/plain"}

# Input types that never need a visible label.
UNLABELED_OK_TYPES = {"hidden", "submit", "button", "reset", "image"}
CLICKABLE_NON_BUTTON_TAGS = {"div", "span", "li", "td", "img", "p"}
CLICK_ATTRS = {"onclick", "@click", "v-on:click", "on:click"}

COOKIE_PATTERNS = [
    r"document\.cookie",
    r"\bsetCookie\b",
    r"\blocalStorage\.setItem\b",
    r"\bgtag\s*\(",
    r"google-analytics\.com",
    r"googletagmanager\.com",
    r"\bfbq\s*\(",
    r"connect\.facebook\.net",
    r"_paq\.push",
    r"matomo",
    r"hotjar",
    r"clarity\.ms",
    r"plausible\.io",
    r"segment\.(?:com|io)",
    r"mixpanel",
    r"cookieconsent",
    r"\bcookiebot\b",
    r"onetrust",
    r"usercentrics",
    r"didomi",
    r"iubenda",
    r"klaro",
]

CONSENT_KEYWORDS = [
    r"consent", r"gdpr", r"privacy", r"souhlas", r"datenschutz", r"cookies?\b", r"newsletter",
]

# Matched only against resources the page actually loads (see embedded_resources), so a plain
# <a href> to Google Maps or YouTube is not reported as an embed.
THIRD_PARTY_EMBED_PATTERNS = [
    r"youtube\.com/embed", r"youtube-nocookie\.com", r"player\.vimeo\.com", r"google\.com/maps",
    r"maps\.googleapis\.com", r"fonts\.googleapis\.com", r"fonts\.gstatic\.com", r"platform\.twitter\.com",
    r"instagram\.com/embed", r"facebook\.com/plugins", r"recaptcha", r"hcaptcha\.com",
    r"challenges\.cloudflare\.com",
]

AI_PATTERNS = [
    r"openai\.com", r"\bfrom\s+[\"']openai[\"']", r"anthropic\.com", r"@anthropic-ai/", r"\bchatgpt\b",
    r"\bgpt-\d", r"\bclaude-[a-z0-9]", r"generativelanguage\.googleapis\.com", r"@google/genai",
    r"api\.mistral\.ai", r"api-inference\.huggingface\.co", r"replicate\.com", r"\bchatbot\b",
    r"assistant\b.*widget", r"recommend(?:ation|er)s?\b", r"personali[sz]ation",
]

AD_PATTERNS = [
    r"adsbygoogle", r"doubleclick\.net", r"googlesyndication\.com", r"taboola", r"outbrain",
]

TRACKING_PIXEL_PATTERNS = [
    r"facebook\.com/tr", r"px\.ads\.linkedin\.com", r"snap\.licdn\.com", r"bat\.bing\.com",
    r"analytics\.tiktok\.com",
]

USER_CONTENT_PATTERNS = [
    r"type\s*=\s*[\"']?file\b", r"disqus", r"giscus", r"utteranc\.es", r"commento", r"remark42",
    r"comment[-_]?form", r"wp-comments-post",
]


def is_excluded(rel_path, exclude):
    rel_path = rel_path.replace(os.sep, "/")
    name = rel_path.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(rel_path, pat) or fnmatch.fnmatch(name, pat) for pat in exclude)


def iter_source_files(root, exclude=()):
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = "" if rel_dir == "." else rel_dir + os.sep
        dirnames[:] = sorted(d for d in dirnames
                             if d not in SKIP_DIRS and not d.startswith(".")
                             and not is_excluded(rel_dir + d, exclude))
        for fn in sorted(filenames):
            if fn.endswith((".min.js", ".min.css")) or is_excluded(rel_dir + fn, exclude):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in SOURCE_EXTENSIONS:
                yield os.path.join(dirpath, fn)


def build_output_dirs_next_to_sources(root, exclude=()):
    """Top-level build output folders that would be scanned together with other files."""
    found = [d for d in sorted(BUILD_OUTPUT_DIRS)
             if os.path.isdir(os.path.join(root, d)) and not is_excluded(d, exclude)]
    if not found:
        return []
    for path in iter_source_files(root, exclude):
        top = os.path.relpath(path, root).split(os.sep, 1)[0]
        if top not in found:
            return found
    return []


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def find_matches(patterns, text):
    hits = []
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            hits.append(pat)
    return hits


def is_own_domain(url, site_domains):
    host = (urlparse(url).hostname or "").lower()
    for d in site_domains:
        d = d.lower().strip(".")
        if host == d or host.endswith("." + d):
            return True
    return False


def parse_attrs(attr_text):
    """Attributes of one tag as {lowercase name: value}; value is None for a bare attribute."""
    attrs = {}
    for m in RE_ATTR.finditer(attr_text):
        if m.group(1):  # template block between attributes, e.g. {{ if .x }}
            continue
        name, value = m.group(2).lower(), m.group(3)
        if value is not None and value[:1] in ("\"", "'", "{"):
            value = value[1:-1].strip() if value[0] == "{" else value[1:-1]
            if value[:1] in ("\"", "'") and value[-1:] == value[:1]:  # JSX {"text"}
                value = value[1:-1]
        attrs.setdefault(name, value)  # the first occurrence wins, as in browsers
    return attrs


def split_markup(text):
    """Return (markup, raw_blocks): comments removed, <script>/<style> bodies cut out of the markup
    and returned separately as (tag, attrs, body) so their contents are not parsed as tags."""
    text = RE_COMMENT.sub(" ", text)
    raw_blocks = []

    def keep_open_tag(m):
        raw_blocks.append((m.group(1).lower(), parse_attrs(m.group(2)), m.group(3)))
        return "<%s%s></%s>" % (m.group(1), m.group(2), m.group(1))

    return RE_RAW_TEXT.sub(keep_open_tag, text), raw_blocks


def iter_tags(markup):
    for m in RE_TAG.finditer(markup):
        yield m.group(1).lower(), parse_attrs(m.group(2)), m.start()


def absolute_url(url):
    if not url:
        return None
    url = url.strip()
    if url.startswith("//"):
        url = "https:" + url
    return url if url.lower().startswith(("http://", "https://")) else None


def embedded_resources(tags, extra_text=""):
    """URLs the browser fetches without a user action, and URLs held back by a consent tool."""
    loaded, gated = set(), set()
    for name, attrs, _ in tags:
        urls = []
        if name in SRC_TAGS:
            urls.append(attrs.get("src"))
        if name in ("img", "source") and attrs.get("srcset"):
            urls.extend(part.split()[0] for part in attrs["srcset"].split(",") if part.split())
        if name == "video":
            urls.append(attrs.get("poster"))
        if name == "object":
            urls.append(attrs.get("data"))
        if name == "link" and set((attrs.get("rel") or "").lower().split()) & AUTO_LOAD_RELS:
            urls.append(attrs.get("href"))
        if attrs.get("style"):
            urls.extend(RE_CSS_URL.findall(attrs["style"]))
        target = gated if (name == "script" and (attrs.get("type") or "").lower() in CONSENT_GATED_SCRIPT_TYPES) \
            else loaded
        target.update(u for u in map(absolute_url, urls) if u)
    loaded.update(u for u in map(absolute_url, RE_CSS_URL.findall(extra_text) + RE_JS_SRC_ASSIGN.findall(extra_text))
                  if u)
    return loaded, gated


def external_form_targets(tags, site_domains):
    targets = (absolute_url(attrs.get("action")) for name, attrs, _ in tags if name == "form")
    return sorted({u for u in targets if u and not is_own_domain(u, site_domains)})


def analyze_forms(markup, tags):
    label_fors = {attrs.get("for") or attrs.get("htmlfor") for name, attrs, _ in tags if name == "label"}
    label_spans = [(m.start(), m.end()) for m in RE_LABEL_BLOCK.finditer(markup)]
    form_count = 0
    field_types = []
    unlabeled = 0
    prechecked = 0
    for name, attrs, pos in tags:
        if name == "form":
            form_count += 1
        if name not in ("input", "textarea", "select"):
            continue
        field_type = (attrs.get("type") or "text").lower() if name == "input" else name
        field_types.append(field_type)
        if field_type in ("checkbox", "radio"):
            checked = attrs.get("checked", attrs.get("defaultchecked", False))
            # Bare attribute or a literal true value; a JSX variable like checked={isOn} is not counted.
            if checked is None or (checked is not False and checked.lower() in ("", "checked", "true")):
                prechecked += 1
        if field_type in UNLABELED_OK_TYPES:
            continue
        if (attrs.get("aria-label") or attrs.get("aria-labelledby") or attrs.get("title")
                or (attrs.get("id") and attrs["id"] in label_fors)
                or any(start < pos < end for start, end in label_spans)):
            continue
        unlabeled += 1
    return {
        "count": form_count,
        "field_count": len(field_types),
        "field_types": field_types,
        "fields_without_matching_label": unlabeled,
        "prechecked_checkboxes_or_radios": prechecked,
        "nearby_consent_keywords": find_matches(CONSENT_KEYWORDS, markup),
    }


def heading_skips(markup):
    skips = []
    levels = [int(m) for m in RE_HEADING.findall(markup)]
    for prev, cur in zip(levels, levels[1:]):
        if cur > prev + 1:
            skips.append(f"h{prev}->h{cur}")
    return skips


def analyze_file(path, text, site_domains):
    findings = {"file": path}
    ext = os.path.splitext(path)[1].lower()
    is_markup = ext in MARKUP_EXTENSIONS

    if is_markup:
        markup, raw_blocks = split_markup(text)
        executed = "\n".join(body for tag, attrs, body in raw_blocks
                             if tag == "style" or (attrs.get("type") or "").lower() in EXECUTABLE_SCRIPT_TYPES)
        tags = list(iter_tags(markup)) + list(iter_tags(executed))
    else:
        markup, executed = text, text
        tags = list(iter_tags(text))  # tags inside JS/CSS strings, e.g. injected iframes

    loaded, gated = embedded_resources(tags, executed)
    external = sorted(u for u in loaded if not is_own_domain(u, site_domains))
    if external:
        findings["external_requests"] = external
    gated_external = sorted(u for u in gated if not is_own_domain(u, site_domains))
    if gated_external:
        findings["consent_gated_requests"] = gated_external

    embed_text = "\n".join(external) + "\n" + executed if is_markup else text
    for key, patterns, haystack in (
        ("cookie_or_tracking_code", COOKIE_PATTERNS, text),
        ("third_party_embeds", THIRD_PARTY_EMBED_PATTERNS, embed_text),
        ("ad_code", AD_PATTERNS, text),
        ("tracking_pixels", TRACKING_PIXEL_PATTERNS, text),
        ("ai_related_code", AI_PATTERNS, text),
        ("user_content_features", USER_CONTENT_PATTERNS, text),
    ):
        hits = find_matches(patterns, haystack)
        if hits:
            findings[key] = hits

    if not is_markup:
        return findings if len(findings) > 1 else None

    page_tags = list(iter_tags(markup))
    form_targets = external_form_targets(page_tags, site_domains)
    if form_targets:
        findings["external_form_targets"] = form_targets

    if any(name in ("form", "input", "textarea", "select") for name, _, _ in page_tags):
        findings["forms"] = analyze_forms(markup, page_tags)

    missing_alt = sum(1 for name, attrs, _ in page_tags if name == "img" and "alt" not in attrs)
    if missing_alt:
        findings["images_missing_alt"] = missing_alt

    clickable = sum(1 for name, attrs, _ in page_tags
                    if name in CLICKABLE_NON_BUTTON_TAGS and CLICK_ATTRS & set(attrs))
    if clickable:
        findings["clickable_non_button_elements"] = clickable

    skips = heading_skips(markup)
    if skips:
        findings["heading_level_skips"] = skips

    html_tags = [attrs for name, attrs, _ in page_tags if name == "html"]
    if html_tags:
        if not (html_tags[0].get("lang") or "").strip():
            findings["html_missing_lang"] = True
        if not any(name == "meta" and (attrs.get("name") or "").lower() == "viewport"
                   for name, attrs, _ in page_tags):
            findings["missing_viewport_meta"] = True

    return findings if len(findings) > 1 else None


def scan(root, site_domains, exclude=()):
    results = []
    for path in iter_source_files(root, exclude):
        text = read_text(path)
        if not text:
            continue
        finding = analyze_file(os.path.relpath(path, root), text, site_domains)
        if finding:
            results.append(finding)
    return results


def print_file_list(title, files):
    print(f"{title}: {len(files)}")
    for f in files:
        print(f"  - {f}")


def print_summary(root, results):
    if not results:
        print("No signals found by the heuristic scan. This does not mean the site is compliant, "
              "it means this fast pass found nothing to flag, read the code directly for a full check.")
        return

    def files_with(*keys):
        return [r["file"] for r in results if any(r.get(k) for k in keys)]

    all_external = sorted(set(u for r in results for u in r.get("external_requests", [])))
    external_hosts = sorted(set(urlparse(u).hostname or u for u in all_external))
    gated_hosts = sorted(set(urlparse(u).hostname or u for r in results for u in r.get("consent_gated_requests", [])))
    form_hosts = sorted(set(urlparse(u).hostname or u for r in results for u in r.get("external_form_targets", [])))
    forms = [r["forms"] for r in results if "forms" in r]

    print(f"Scanned root: {root}")
    print(f"Files with findings: {len(results)}")
    print()
    print(f"External hosts loaded automatically: {len(external_hosts)} ({len(all_external)} distinct URLs)")
    for h in external_hosts[:40]:
        print(f"  - {h}")
    if len(external_hosts) > 40:
        print(f"  ... and {len(external_hosts) - 40} more, use --json for the full list")
    if gated_hosts:
        print(f"External hosts held back by a consent tool (type=text/plain): {len(gated_hosts)}")
        for h in gated_hosts:
            print(f"  - {h}")
    print_file_list("Forms submitting to external hosts (" + ", ".join(form_hosts) + ")" if form_hosts
                    else "Forms submitting to external hosts", files_with("external_form_targets"))
    print()
    print_file_list("Files containing cookie/storage/tracking or consent-tool code",
                    files_with("cookie_or_tracking_code"))
    print_file_list("Files with third-party embeds, fonts, or CAPTCHA (may transfer IP before consent)",
                    files_with("third_party_embeds"))
    print_file_list("Files containing ad code or tracking pixels", files_with("ad_code", "tracking_pixels"))
    print_file_list("Files containing AI-related code/keywords", files_with("ai_related_code"))
    print_file_list("Files with comment/upload features (possible DSA hosting duties)",
                    files_with("user_content_features"))
    print()
    print(f"Forms found: {sum(f['count'] for f in forms)}, "
          f"fields with no matching <label>/aria-label: {sum(f['fields_without_matching_label'] for f in forms)}, "
          f"pre-checked checkboxes/radios: {sum(f['prechecked_checkboxes_or_radios'] for f in forms)}")
    print(f"Images missing alt attribute: {sum(r.get('images_missing_alt', 0) for r in results)}")
    print(f"Clickable non-button elements: {sum(r.get('clickable_non_button_elements', 0) for r in results)}")
    print_file_list("Files with skipped heading levels", files_with("heading_level_skips"))
    print_file_list("Files with <html> missing a lang attribute", files_with("html_missing_lang"))
    print_file_list("Files with <html> but no viewport meta tag", files_with("missing_viewport_meta"))
    print()
    print("This is a heuristic lead list, not a verdict. Confirm every item against the source and "
          "against references/*.md before including it in a compliance report.")


def main():
    parser = argparse.ArgumentParser(description="Scan a website's source for EU-compliance signals.")
    parser.add_argument("root", help="Path to the site's source root, or to the build output of a static site")
    parser.add_argument("--domain", action="append", default=[],
                        help="The site's own domain(s), excluded (with subdomains) from 'external request' "
                             "findings. Can be passed multiple times.")
    parser.add_argument("--exclude", action="append", default=[], metavar="PATTERN",
                        help="Glob matched against the relative path and the file or directory name, "
                             "e.g. public, 'design/*', '*.dc.html'. Can be passed multiple times.")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of a summary")
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"Not a directory: {args.root}", file=sys.stderr)
        sys.exit(1)

    build_dirs = build_output_dirs_next_to_sources(args.root, args.exclude)
    if build_dirs:
        names = ", ".join(d + "/" for d in build_dirs)
        print(f"Warning: {names} looks like build output and is scanned together with the sources, so "
              f"findings may be reported twice. For a static site generator, scan the build output alone "
              f"(scan.py {os.path.join(args.root, build_dirs[0])}) and read templates by hand, or pass "
              f"--exclude {build_dirs[0]}.", file=sys.stderr)

    results = scan(args.root, args.domain, args.exclude)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_summary(args.root, results)


if __name__ == "__main__":
    main()
