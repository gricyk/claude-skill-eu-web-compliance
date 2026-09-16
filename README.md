# EU Web Compliance, a Claude Skill

A [Claude Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that reviews
a website you are building or maintaining (including one you're building with Claude Code) against
current EU digital law, GDPR, the ePrivacy Directive, the EU AI Act, the Digital Services Act, and EU
web accessibility rules, and produces a sourced findings report plus draft remediation, only after
consulting you first.

**This is not legal advice, and it does not replace a lawyer or a Data Protection Officer.** It gives
you a structured, sourced starting point and flags what still needs human or legal confirmation.

## Why

EU digital regulation is broad, moving, and easy to get subtly wrong, especially the interaction
between GDPR, cookie rules, and the AI Act's transparency duties, which now apply to a lot of ordinary
websites (chatbots, AI-generated content, personalization). At the same time, both the AI Act's
timeline and the GDPR/ePrivacy "Digital Omnibus" reform are actively changing through 2026 and 2027.
This skill is built to check current status rather than assume a fixed set of facts, and to say clearly
when something is unverified instead of guessing.

## What it does

1. Asks what the site does, who it's for, what data it touches, and whether it uses AI, rather than
   assuming.
2. Scans the codebase, both by reading it directly and with a fast, dependency-free scanner
   (`scripts/scan.py`) that inventories external requests, cookies/trackers, third-party embeds, forms
   (including pre-ticked consent boxes), AI-related code, ad code, comment/upload features, and basic
   accessibility signals.
3. Checks the current legal landscape with a web search before citing any time-sensitive deadline or
   provision (the AI Act timeline and the Digital Omnibus status change often), instead of relying on
   a static, aging snapshot.
4. Produces a findings report (`references/templates/findings-report.md`), grouped by regulation, with article citations and a clear `VERIFY` tag
   on anything not independently confirmed.
5. Proposes a remediation plan, including draft legal documents (privacy policy, cookie policy, DPIA,
   records of processing, AI transparency notices, accessibility statements), and only edits files or
   publishes drafts after you approve the plan.

## Examples

See [`examples/`](examples/) for two full runs on fictional sites:

- **A café website with typical problems**: scanner output, a findings report with dated legal sources,
  and the remediation plan the skill presents before changing anything. It caught a chatbot instructed
  to hide that it is an AI, analytics loading before cookie consent, a pre-ticked newsletter box, and
  allergy data collected without explicit consent.
- **A hiking club website that is already fine** (minified Hugo output): a short report that says
  plainly which obligations do not apply, including why no cookie banner is needed.

## Install

### claude.ai (web and desktop app)

1. Download `eu-web-compliance-vX.Y.Z.zip` from the
   [latest release](https://github.com/gricyk/claude-skill-eu-web-compliance/releases/latest).
   It contains only what the skill needs (`SKILL.md`, `references/`, `scripts/`, `LICENSE`).
2. In claude.ai, open **Settings → Capabilities** and make sure **Code execution** is enabled.
3. Under **Skills**, click **Upload skill**, select the zip, and check that the skill is toggled on.

On claude.ai, Claude cannot read files on your computer, so upload your site's source (as a zip or
individual files) to the conversation, or give it the site's URL.

### Claude Code

This repository's root *is* the skill folder (it contains `SKILL.md` directly). Clone it into your
Claude Skills directory under the skill's own name, `eu-web-compliance`:

```bash
# Project-level (this skill only applies inside this project)
mkdir -p .claude/skills
git clone https://github.com/gricyk/claude-skill-eu-web-compliance.git .claude/skills/eu-web-compliance

# Or user-level (available in every project)
mkdir -p ~/.claude/skills
git clone https://github.com/gricyk/claude-skill-eu-web-compliance.git ~/.claude/skills/eu-web-compliance
```

Start a new Claude Code session after installing. To update later, run
`git -C ~/.claude/skills/eu-web-compliance pull` (or the project-level path).

If you prefer not to use git, unzip the release zip into `.claude/skills/` or `~/.claude/skills/`; it
already contains a folder named `eu-web-compliance`.

### Using it

Claude picks the skill up automatically when a conversation matches the triggers described in
`SKILL.md`'s frontmatter, no explicit invocation is required, though you can always ask directly, e.g.
"check this site for GDPR and AI Act compliance".

## Structure

```
eu-web-compliance/
├── SKILL.md                          # entry point: rules and workflow
├── references/
│   ├── gdpr-checklist.md
│   ├── eprivacy-checklist.md
│   ├── ai-act-checklist.md
│   ├── dsa-checklist.md
│   ├── accessibility-checklist.md
│   ├── national-law-guide.md         # how to verify country-specific law, not static per-country data
│   └── templates/
│       ├── findings-report.md        # structure of the review report
│       ├── privacy-policy.md
│       ├── cookie-policy.md
│       ├── dpia.md
│       ├── ropa.md
│       ├── ai-transparency-notice.md
│       └── accessibility-statement.md
├── scripts/
│   └── scan.py                       # fast, stdlib-only structural scan of site source
├── examples/                         # demo runs on fictional sites (not used by the skill)
└── tests/                            # unit tests for scan.py and SKILL.md (not used by the skill)
```

## Using the scanner on its own

`scan.py` needs only Python 3.9+ and works outside Claude too:

```bash
python3 scripts/scan.py /path/to/site --domain example.com         # summary
python3 scripts/scan.py /path/to/site --domain example.com --json  # per-file detail
python3 scripts/scan.py public --domain example.com                # built output of Hugo & co.
python3 scripts/scan.py . --exclude public --exclude "*.dc.html"   # sources only, skip mockups
```

`--domain` can be repeated and excludes your own domain and its subdomains from the external-request
list. `--exclude` takes a glob matched against the relative path and the file or folder name. Only
resources the browser loads by itself (`src`, stylesheets, preconnect, CSS `url()`) count as external
requests and embeds; plain `<a href>` links do not. Minified HTML is supported.

## Scope and limits

- Built around the GDPR, ePrivacy Directive, EU AI Act, DSA, and WCAG/EAA/Web Accessibility Directive.
  It deliberately keeps national-law specifics as "how to verify" guidance rather than hardcoded facts,
  since these vary by all 27 member states and change over time.
- `scripts/scan.py` is a heuristic lead generator (regex over source text), not a compiler or a
  runtime analyzer. It can both miss things and false-positive. Every material finding should be
  confirmed by reading the actual code before it goes in a report.
- Minified HTML is supported. For static site generators (Hugo, Jekyll, Eleventy, Astro, Next.js static
  export), the skill scans the build output and reads the templates by hand.
- Code review alone misses a lot. When the site is live or can be served locally, the skill checks it in
  a browser: cookies and `Set-Cookie` headers, requests to third-party hosts before and after consent,
  where the server really is (IP → ASN), text contrast over images, and keyboard focus with menus and
  overlays, with the language pinned on multilingual sites. Findings it could not confirm at runtime are
  labeled as code only.
- The skill will not edit your files or publish a legal document without first showing you a written
  plan and getting your explicit approval.
- If a finding has real regulatory or financial exposure, the skill will tell you to get a lawyer or
  DPO to review it, that's not a formality, some of what's covered here genuinely needs one.

## Legal snapshot

The reference files contain a dated snapshot of time-sensitive points, last checked on
**16 September 2026**: the Digital Omnibus on AI (Regulation (EU) 2026/1744) postponed the
AI Act's high-risk deadlines, while the GDPR/ePrivacy Digital Omnibus (cookie rules in a new GDPR
Art. 88a) was still in the legislative procedure. The skill is instructed to re-check these with a web
search before citing them, never to rely on the snapshot alone.

## Official sources

The checklists are built on these primary texts. Consolidated versions (with later amendments) are
linked from each EUR-Lex page.

| Area | Legal act |
|---|---|
| GDPR | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) |
| ePrivacy (cookies, e-marketing) | [Directive 2002/58/EC](https://eur-lex.europa.eu/eli/dir/2002/58/oj), amended by [Directive 2009/136/EC](https://eur-lex.europa.eu/eli/dir/2009/136/oj) |
| AI Act | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), amended by the Digital Omnibus on AI, [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj) |
| Digital Services Act | [Regulation (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj) |
| European Accessibility Act | [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj) |
| Web Accessibility Directive | [Directive (EU) 2016/2102](https://eur-lex.europa.eu/eli/dir/2016/2102/oj), model accessibility statement: [Implementing Decision (EU) 2018/1523](https://eur-lex.europa.eu/eli/dec_impl/2018/1523/oj) |
| SME size definitions (DSA, EAA exemptions) | [Commission Recommendation 2003/361/EC](https://eur-lex.europa.eu/eli/reco/2003/361/oj) |
| Accessibility technical standards | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) (W3C), [EN 301 549](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/) (ETSI, all versions) |
| Pending: Digital Omnibus (GDPR, ePrivacy) | Commission proposal COM(2025) 837, status: [European Parliament Legislative Train](https://www.europarl.europa.eu/legislative-train/theme-a-new-plan-for-europe-s-sustainable-prosperity-and-competitiveness/file-digital-package). Not adopted law as of the last check |

## Contributing

Issues and pull requests welcome, especially: additions to `national-law-guide.md`'s per-country
pattern for other member states, corrections to the checklists as the law changes, and improvements to
`scan.py`'s detection patterns. Run the tests before opening a PR:

```bash
python3 -m unittest discover -s tests -v
```

## License

Apache License 2.0, see `LICENSE`. Copyright 2026 Igor Gricyk.
