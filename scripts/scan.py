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
    python3 scan.py /path/to/site/root [--domain example.com ...] [--json]

--domain can be passed several times, it excludes the site's own domain(s)
(and their subdomains) from the external-request list.

Only depends on the Python standard library, so it runs anywhere without
setup.
"""

import argparse
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
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit", "vendor", ".venv",
             "__pycache__", "coverage"}

RE_SRC_HREF = re.compile(r'(?:src|href|action)\s*=\s*["\'](https?://[^"\']+)["\']', re.IGNORECASE)
RE_CSS_URL = re.compile(r'(?:url\(\s*["\']?|@import\s+["\'])(https?://[^"\')\s]+)', re.IGNORECASE)
RE_FORM = re.compile(r"<form\b[^>]*>", re.IGNORECASE)
RE_INPUT = re.compile(r"<input\b[^>]*>", re.IGNORECASE)
RE_TEXTAREA_SELECT = re.compile(r"<(?:textarea|select)\b[^>]*>", re.IGNORECASE)
RE_INPUT_TYPE = re.compile(r'\btype\s*=\s*["\']?([\w-]+)', re.IGNORECASE)
RE_LABEL_FOR = re.compile(r'<label\b[^>]*\b(?:for|htmlFor)\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
RE_ID = re.compile(r'\bid\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
RE_ARIA_LABEL = re.compile(r'\baria-label(?:ledby)?\s*=', re.IGNORECASE)
RE_CHECKED = re.compile(r'\s(?:checked|defaultChecked)(?:\s*=\s*(?:["\'](?:checked|true)?["\']|\{\s*true\s*\}))?(?=[\s/>])',
                        re.IGNORECASE)
RE_IMG = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
RE_ALT = re.compile(r'\balt\s*=', re.IGNORECASE)
RE_HTML_TAG = re.compile(r"<html\b([^>]*)>", re.IGNORECASE)
RE_LANG_ATTR = re.compile(r'\blang\s*=\s*["\']', re.IGNORECASE)
RE_VIEWPORT = re.compile(r'<meta\b[^>]*name\s*=\s*["\']viewport["\']', re.IGNORECASE)
RE_CLICKABLE_NON_BUTTON = re.compile(r'<(?:div|span|li|td|img)\b[^>]*\s(?:onclick|onClick|@click|v-on:click|on:click)\s*=',
                                     re.IGNORECASE)
RE_HEADING = re.compile(r"<h([1-6])\b", re.IGNORECASE)

# Input types that never need a visible label.
UNLABELED_OK_TYPES = {"hidden", "submit", "button", "reset", "image"}

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


def iter_source_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            if fn.endswith((".min.js", ".min.css")):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in SOURCE_EXTENSIONS:
                yield os.path.join(dirpath, fn)


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


def analyze_forms(text):
    fields = RE_INPUT.findall(text) + RE_TEXTAREA_SELECT.findall(text)
    label_fors = set(RE_LABEL_FOR.findall(text))
    input_types = []
    unlabeled = 0
    prechecked = 0
    for tag in fields:
        if tag.lower().startswith("<input"):
            type_match = RE_INPUT_TYPE.search(tag)
            field_type = type_match.group(1).lower() if type_match else "text"
        else:
            field_type = tag[1:].split()[0].rstrip(">").lower()
        input_types.append(field_type)
        if field_type in ("checkbox", "radio") and RE_CHECKED.search(tag):
            prechecked += 1
        if field_type in UNLABELED_OK_TYPES:
            continue
        # A field wrapped in <label>...</label> is labeled too, but a regex cannot see
        # nesting reliably, so this count can over-flag; confirm in the source.
        id_match = RE_ID.search(tag)
        if RE_ARIA_LABEL.search(tag) or (id_match and id_match.group(1) in label_fors):
            continue
        unlabeled += 1
    return {
        "count": len(RE_FORM.findall(text)),
        "field_count": len(fields),
        "field_types": input_types,
        "fields_without_matching_label": unlabeled,
        "prechecked_checkboxes_or_radios": prechecked,
        "nearby_consent_keywords": find_matches(CONSENT_KEYWORDS, text),
    }


def heading_skips(text):
    skips = []
    levels = [int(m) for m in RE_HEADING.findall(text)]
    for prev, cur in zip(levels, levels[1:]):
        if cur > prev + 1:
            skips.append(f"h{prev}->h{cur}")
    return skips


def analyze_file(path, text, site_domains):
    findings = {"file": path}
    ext = os.path.splitext(path)[1].lower()

    urls = set(RE_SRC_HREF.findall(text)) | set(RE_CSS_URL.findall(text))
    external = sorted(u for u in urls if not is_own_domain(u, site_domains))
    if external:
        findings["external_requests"] = external

    for key, patterns in (
        ("cookie_or_tracking_code", COOKIE_PATTERNS),
        ("third_party_embeds", THIRD_PARTY_EMBED_PATTERNS),
        ("ad_code", AD_PATTERNS),
        ("tracking_pixels", TRACKING_PIXEL_PATTERNS),
        ("ai_related_code", AI_PATTERNS),
        ("user_content_features", USER_CONTENT_PATTERNS),
    ):
        hits = find_matches(patterns, text)
        if hits:
            findings[key] = hits

    if ext not in MARKUP_EXTENSIONS:
        return findings if len(findings) > 1 else None

    if RE_FORM.search(text) or RE_INPUT.search(text) or RE_TEXTAREA_SELECT.search(text):
        findings["forms"] = analyze_forms(text)

    imgs = RE_IMG.findall(text)
    missing_alt = sum(1 for tag_attrs in imgs if not RE_ALT.search(tag_attrs))
    if missing_alt:
        findings["images_missing_alt"] = missing_alt

    clickable = len(RE_CLICKABLE_NON_BUTTON.findall(text))
    if clickable:
        findings["clickable_non_button_elements"] = clickable

    skips = heading_skips(text)
    if skips:
        findings["heading_level_skips"] = skips

    html_tag = RE_HTML_TAG.search(text)
    if html_tag:
        if not RE_LANG_ATTR.search(html_tag.group(1)):
            findings["html_missing_lang"] = True
        if not RE_VIEWPORT.search(text):
            findings["missing_viewport_meta"] = True

    return findings if len(findings) > 1 else None


def scan(root, site_domains):
    results = []
    for path in iter_source_files(root):
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
    forms = [r["forms"] for r in results if "forms" in r]

    print(f"Scanned root: {root}")
    print(f"Files with findings: {len(results)}")
    print()
    print(f"External hosts referenced: {len(external_hosts)} ({len(all_external)} distinct URLs)")
    for h in external_hosts[:40]:
        print(f"  - {h}")
    if len(external_hosts) > 40:
        print(f"  ... and {len(external_hosts) - 40} more, use --json for the full list")
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
    parser.add_argument("root", help="Path to the site's source root")
    parser.add_argument("--domain", action="append", default=[],
                        help="The site's own domain(s), excluded (with subdomains) from 'external request' "
                             "findings. Can be passed multiple times.")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of a summary")
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"Not a directory: {args.root}", file=sys.stderr)
        sys.exit(1)

    results = scan(args.root, args.domain)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_summary(args.root, results)


if __name__ == "__main__":
    main()
