# EU web compliance review: Example Hiking Club (fictional demo)

> **Demo output.** This report was produced with the `eu-web-compliance` skill against the fictional
> site in [`hiking-club-site/`](hiking-club-site/). The club and all data are invented. This example
> shows the other half of the job: a small, well-built site where the main risk is **inventing
> obligations that do not apply**.

**This report is not legal advice.** It is a structured, sourced analysis to support a decision by the
site owner. Anything with real regulatory or financial exposure should be reviewed by a lawyer or Data
Protection Officer before relying on it.

- Site reviewed: `examples/hiking-club-site/public/` (Hugo build output, `hugo --minify`, 3 pages, no
  JavaScript)
- Date of review: 16 September 2026
- Operator and country of establishment: Example Hiking Club, z. s., Czech Republic (stated by owner,
  see [`CONTEXT.md`](hiking-club-site/CONTEXT.md))
- Target audience: Czech Republic

## Scope

- Regulations covered: GDPR, ePrivacy (Czech transposition), AI Act, DSA, accessibility.
- Out of scope: the club's offline member register, email and hosting contracts.
- Method: manual review of the built HTML and CSS, `scripts/scan.py` on the build output (no signals,
  [`hiking-club-site-scan.txt`](hiking-club-site-scan.txt)), web checks below.
- Runtime checks: **not done** (fictional site, nothing to load). All findings are code only; the two
  runtime checks that matter here are listed as `VERIFY` items.

## Live legal-status checks

| Topic | Finding | Source | Checked on |
|---|---|---|---|
| CZ: cookie consent | Opt-in consent for non-essential storage, § 89(3) Act No. 127/2005 Sb. Nothing to consent to if nothing is stored | [epravo.cz](https://www.epravo.cz/top/clanky/cookies-nove-jen-se-souhlasem-poslanecka-snemovna-prijala-zprisnujici-pravidla-od-roku-2022-113207.html) | 16 Sep 2026 |
| Digital Omnibus (GDPR / ePrivacy), COM(2025) 837 | Not adopted, current rules unchanged | [European Parliament Legislative Train](https://www.europarl.europa.eu/legislative-train/theme-a-new-plan-for-europe-s-sustainable-prosperity-and-competitiveness/file-digital-package) | 16 Sep 2026 |
| CZ: data protection authority | ÚOOÚ, linked correctly from the privacy page | [uoou.gov.cz](https://uoou.gov.cz/) | 16 Sep 2026 |

## Summary

| Regulation | likely violation | gap | info | VERIFY |
|---|---|---|---|---|
| GDPR | 0 | 0 | 3 | 2 |
| ePrivacy | 0 | 0 | 1 | 1 |
| AI Act | 0 | 0 | 0 | 0 |
| DSA | 0 | 0 | 0 | 0 |
| Accessibility | 0 | 0 | 2 | 0 |

No violations or gaps found in the website. Two things to confirm in a browser, and one question about
the offline member register.

## Applicability, including what does **not** apply

| Rule | Applies? | Why |
|---|---|---|
| GDPR | Yes, narrowly | Email correspondence via the address on the contact page. The site itself collects nothing: no forms, no analytics, no scripts. |
| ePrivacy consent (§ 89(3) Act 127/2005 Sb.) | No consent needed | Nothing is stored on or read from the visitor's device in the code, and no third-party resources are loaded. **A cookie banner is not needed and should not be added**, a banner with nothing behind it misleads visitors. |
| AI Act | No | No AI system is used. |
| DSA | No | No user content is stored or shown (no comments, uploads, or forum). The club's Facebook page is on Facebook's platform; the club is a user there, not an intermediary service provider. |
| Web Accessibility Directive | No | The club is not a public sector body. |
| European Accessibility Act | No | No covered service (no e-commerce, banking, e-books, transport ticketing, etc.); the club is also a microenterprise at most. Findings below are WCAG best practice only. |
| DPO (GDPR Art. 37) | No | Not a public authority; no large-scale monitoring or large-scale special category processing. |
| DPIA (GDPR Art. 35) | No | No high-risk processing on the website. |
| Children's consent (GDPR Art. 8, age 15 in CZ) | No | No information society service is offered directly to children; minors join trips with a parent, arranged by email. |

## Findings

### GDPR

#### G1. Privacy notice covers the email contact

- Provision: GDPR Art. 13
- Evidence: [`public/ochrana-osobnich-udaju/index.html`](hiking-club-site/public/ochrana-osobnich-udaju/index.html)
  names the controller with contact, purpose, legal basis with the specific legitimate interest,
  recipients, no transfers outside the EEA, retention (12 months), data subject rights, and the right
  to complain to ÚOOÚ.
- Risk: info
- Confidence: high
- Note: nothing to fix. Keep the "Aktualizováno" date current when anything changes.

#### G2. Hosting and email provider: confirm location and contract

- Provision: GDPR Art. 28, 44
- Evidence: the notice says a processing agreement is in place and no data leaves the EEA; the owner
  says the hosting is Czech and rented by the association itself, so there is no intermediate person in
  the processor chain.
- Risk: info
- Confidence: medium
- `VERIFY`: resolve the domain and its `MX` records to IP → ASN → operator
  (`references/gdpr-checklist.md`, section 14). If the operator turns out to be a company headquartered
  outside the EEA, the "no transfers" sentence needs review.

#### G3. Offline member register

- Provision: GDPR Art. 30(5)
- Evidence: out of the website's scope, mentioned by the owner.
- Risk: info
- Confidence: low
- `VERIFY`: a member register is regular, not occasional processing, so the under-250-employees
  exemption from keeping records of processing most likely does not apply to it. Worth a one-page record
  (`references/templates/ropa.md`), but this is not a website issue.

### ePrivacy

#### E1. No cookies, storage, or third-party requests in the code

- Provision: ePrivacy Directive Art. 5(3), § 89(3) Act 127/2005 Sb.
- Evidence: no `<script>` on any page; fonts self-hosted via `@font-face`
  ([`public/css/main.min.css`](hiking-club-site/public/css/main.min.css)); all `src`, stylesheet and icon
  URLs are local; Mapy.com, OpenStreetMap and Facebook are plain links, loaded only if the visitor
  clicks.
- Risk: info
- Confidence: medium (code only)
- `VERIFY`: load the live site in a fresh browser profile and confirm no `Set-Cookie` headers (some
  hosting setups add load-balancer or security cookies at the server level) and no requests to other
  hosts (`references/eprivacy-checklist.md`, section 5).

### Accessibility (best practice, no legal duty found)

#### X1. Baseline checks pass in the markup

- Provision: WCAG 2.2 SC 1.1.1, 1.3.1, 1.4.3, 3.1.1
- Evidence: `lang=cs` on all pages; the logo inside the home link has a bare `alt` (decorative, the link
  text names it); the trip photo has descriptive alt text; headings in order; body text `#1f2933` on
  white is 14.76:1, links `#0b5394` are 7.84:1.
- Risk: info
- Confidence: high
- Note: links differ from body text only 1.88:1 by color, but they keep the browser's default underline,
  so SC 1.4.1 is met. Do not remove the underline in CSS without adding another cue.

#### X2. Runtime checks still worth doing

- Provision: WCAG 2.2 SC 1.4.10, 2.4.7
- Evidence: no overlays or menus to trap focus; reflow and focus visibility can only be seen in a
  browser.
- Risk: info
- Confidence: medium
- Suggested check: 320 px width and a Tab walk-through (`references/accessibility-checklist.md`,
  section 4).

## What this report deliberately does not recommend

- A cookie banner or cookie policy: there is nothing to consent to.
- An AI transparency notice, DSA notice-and-action form, or accessibility statement: no rule requires
  them for this site.
- A DPIA or a Data Protection Officer.
- Rewriting the existing privacy notice: it already contains what Art. 13 requires for the one data
  flow the site has.

## Facts needed from the site owner

- None for the website. For G3, whether a written record of the member register exists.
