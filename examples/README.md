# Example: reviewing a fictional café website

A complete run of the skill on a small, deliberately flawed site. **Everything about the café is
fictional**; the legal status checks in the report were real, made on 16 September 2026.

| File | Workflow step | What it shows |
|---|---|---|
| [`cafe-site/CONTEXT.md`](cafe-site/CONTEXT.md) | 1. Establish context | The answers the skill asks the site owner for |
| [`cafe-site/`](cafe-site/) | (input) | HTML pages, JS widgets, and two server handlers with typical real-world problems |
| [`cafe-site-scan.txt`](cafe-site-scan.txt) | 2. Scan the code | Output of `scripts/scan.py`, a lead list, not a verdict |
| [`cafe-site-report.md`](cafe-site-report.md) | 3–4. Legal checks and report | Findings by regulation with provision, file and line, risk, confidence, `VERIFY` tags, and dated sources |
| [`cafe-site-remediation-plan.md`](cafe-site-remediation-plan.md) | 5. Consult before changing | Proposed edits, draft chatbot disclosure, documents to draft, and the facts the owner still has to provide |

What the site gets wrong, in short: a chatbot told to hide that it is an AI, Google Analytics loading
before consent behind an "Accept all"-only banner, a pre-ticked newsletter box, allergy data collected
without explicit consent, chat logs with IP addresses kept forever, blog comments with no way to report
them, and a handful of accessibility issues.

Reproduce the scan from the repository root:

```bash
cd examples && python3 ../scripts/scan.py cafe-site --domain example.com
```
