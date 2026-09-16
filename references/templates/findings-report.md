# Findings report template (Step 4)

Keep the structure, drop any regulation section that was out of scope and say so in "Scope". Every
finding needs a provision, evidence (file and line, or page and element), a risk label, and a
confidence level. Anything not verified in this session is tagged `VERIFY` with what to check and where.

Risk labels: `info` (observation, no action strictly needed) / `gap` (something missing or weak that
should be fixed) / `likely violation` (the code or content as found probably breaches the provision).

Confidence: `high` (confirmed in code and in the legal text) / `medium` (confirmed in code, legal
applicability depends on facts not yet confirmed) / `low` (heuristic or unconfirmed).

---

# EU web compliance review: {{site_name}}

**This report is not legal advice.** It is a structured, sourced analysis to support a decision by the
site owner. Anything with real regulatory or financial exposure should be reviewed by a lawyer or Data
Protection Officer before relying on it.

- Site / repository reviewed: {{site_url_or_repo_path}} (commit or version: {{version}})
- Date of review: {{date}}
- Operator and country of establishment: {{operator}}, {{country}} (confirmed / `VERIFY`)
- Target audience: {{audience_countries}}

## Scope

- Regulations covered: {{GDPR / ePrivacy / AI Act / DSA / accessibility}}
- Out of scope, and why: {{out_of_scope}}
- Method: manual code review of {{files_or_areas}}, `scripts/scan.py` heuristic scan, web checks listed
  below.
- Runtime checks: {{done / not done}}. URL {{url}}, date {{date}}, browser {{browser}}, pinned language
  {{language_and_how}}, widths {{widths}}. Findings not confirmed at runtime are labeled "code only".

## Live legal-status checks

| Topic | Finding | Source | Checked on |
|---|---|---|---|
| AI Act timeline for obligations in play | {{status}} | {{url}} | {{date}} |
| Digital Omnibus (GDPR / ePrivacy) status | {{status}} | {{url}} | {{date}} |
| {{national_provision}} | {{status}} | {{url}} | {{date}} |

## Summary

| Regulation | likely violation | gap | info | VERIFY |
|---|---|---|---|---|
| GDPR | {{n}} | {{n}} | {{n}} | {{n}} |
| ePrivacy | {{n}} | {{n}} | {{n}} | {{n}} |
| AI Act | {{n}} | {{n}} | {{n}} | {{n}} |
| DSA | {{n}} | {{n}} | {{n}} | {{n}} |
| Accessibility | {{n}} | {{n}} | {{n}} | {{n}} |

Top priorities, in order: {{one_line_each}}

## Applicability

State for each regulation whether it applies and why, including thresholds (DSA micro/small enterprise
exemption, EAA covered services and microenterprise exemption, Web Accessibility Directive public-sector
scope, AI Act only if an AI system is used).

## Findings

### GDPR

#### G1. {{short_title}}

- Provision: {{e.g. GDPR Art. 13(1)(c)}}
- Evidence: {{file:line or page/element, what was found}}
- Risk: {{info / gap / likely violation}}
- Confidence: {{high / medium / low}}
- Why it matters: {{one or two sentences}}
- Suggested fix: {{what to change}}
- `VERIFY`: {{what to check and where, or "none"}}

### ePrivacy

{{same structure, E1, E2, ...}}

### AI Act

{{same structure, A1, A2, ...}}

### DSA

{{same structure, D1, D2, ...}}

### Accessibility

{{same structure, X1, X2, ...}}

## Facts needed from the site owner

- {{e.g. legal entity name and address}}
- {{e.g. retention period for contact form submissions}}
- {{e.g. list of processors and data processing agreements in place}}

## Next step

A remediation plan with proposed file changes and draft documents follows separately. No files have been
changed and no documents published; that happens only after your approval.
