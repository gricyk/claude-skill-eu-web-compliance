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

## Install

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

If you downloaded a zip instead of cloning, just unzip it and rename the resulting folder to
`eu-web-compliance` inside `.claude/skills/`.

Claude (in Claude Code or claude.ai, wherever Skills are supported) will pick it up automatically when
a conversation matches the triggers described in `SKILL.md`'s frontmatter, no explicit invocation is
required, though you can always ask directly, e.g. "check this site for GDPR and AI Act compliance".

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
└── tests/                            # unit tests for scan.py and SKILL.md (not used by the skill)
```

## Using the scanner on its own

`scan.py` needs only Python 3.9+ and works outside Claude too:

```bash
python3 scripts/scan.py /path/to/site --domain example.com         # summary
python3 scripts/scan.py /path/to/site --domain example.com --json  # per-file detail
```

`--domain` can be repeated and excludes your own domain and its subdomains from the external-request
list.

## Scope and limits

- Built around the GDPR, ePrivacy Directive, EU AI Act, DSA, and WCAG/EAA/Web Accessibility Directive.
  It deliberately keeps national-law specifics as "how to verify" guidance rather than hardcoded facts,
  since these vary by all 27 member states and change over time.
- `scripts/scan.py` is a heuristic lead generator (regex over source text), not a compiler or a
  runtime analyzer. It can both miss things and false-positive. Every material finding should be
  confirmed by reading the actual code before it goes in a report.
- The skill will not edit your files or publish a legal document without first showing you a written
  plan and getting your explicit approval.
- If a finding has real regulatory or financial exposure, the skill will tell you to get a lawyer or
  DPO to review it, that's not a formality, some of what's covered here genuinely needs one.

## Legal snapshot

The reference files contain a dated snapshot of time-sensitive points, last checked on
**16 September 2026**: the Digital Omnibus on AI (reported as Regulation (EU) 2026/1744) postponed the
AI Act's high-risk deadlines, while the GDPR/ePrivacy Digital Omnibus (cookie rules in a new GDPR
Art. 88a) was still in the legislative procedure. The skill is instructed to re-check these with a web
search before citing them, never to rely on the snapshot alone.

## Contributing

Issues and pull requests welcome, especially: additions to `national-law-guide.md`'s per-country
pattern for other member states, corrections to the checklists as the law changes, and improvements to
`scan.py`'s detection patterns. Run the tests before opening a PR:

```bash
python3 -m unittest discover -s tests -v
```

## License

Apache License 2.0, see `LICENSE`. Copyright 2026 Igor Gricyk.
