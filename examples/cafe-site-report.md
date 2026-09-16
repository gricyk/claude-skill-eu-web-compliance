# EU web compliance review: Example Café (fictional demo)

> **Demo output.** This report was produced with the `eu-web-compliance` skill against the fictional
> site in [`cafe-site/`](cafe-site/). The café, its operator and all data are invented. Legal status
> checks were real and made on the date below.

**This report is not legal advice.** It is a structured, sourced analysis to support a decision by the
site owner. Anything with real regulatory or financial exposure should be reviewed by a lawyer or Data
Protection Officer before relying on it.

- Site / repository reviewed: `examples/cafe-site/` (static HTML, JS widgets, two server handlers)
- Date of review: 16 September 2026
- Operator and country of establishment: Example Café s.r.o., Czech Republic (stated by owner, see
  [`CONTEXT.md`](cafe-site/CONTEXT.md); company ID and registered address not yet provided)
- Target audience: visitors in the Czech Republic (Czech and English)

## Scope

- Regulations covered: GDPR, ePrivacy (Czech transposition), AI Act, DSA, accessibility.
- Out of scope: the database layer (`server/db`, not provided), hosting and email provider contracts,
  the newsletter and booking backends (`/api/newsletter`, `/api/bookings`, not provided).
- Method: manual review of all files, `scripts/scan.py` heuristic scan (output in
  [`cafe-site-scan.txt`](cafe-site-scan.txt)), web checks listed below. Runtime behavior (which cookies
  are actually set in a browser) was **not tested**; findings about cookies are based on code only.

## Live legal-status checks

| Topic | Finding | Source | Checked on |
|---|---|---|---|
| AI Act timeline | Art. 50 deployer/provider disclosure duties apply from 2 August 2026, not postponed. Regulation (EU) 2026/1744 postponed Annex III high-risk rules to 2 December 2027 | [EUR-Lex, Reg. (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj) | 16 Sep 2026 |
| Digital Omnibus (GDPR / ePrivacy), proposal COM(2025) 837 | Still in the legislative procedure, not applicable law. Current cookie rules unchanged | [European Parliament Legislative Train](https://www.europarl.europa.eu/legislative-train/theme-a-new-plan-for-europe-s-sustainable-prosperity-and-competitiveness/file-digital-package) | 16 Sep 2026 |
| CZ: age of digital consent (GDPR Art. 8) | 15 years, § 7 of Act No. 110/2019 Sb. | [Act 110/2019 Sb. (EUR-Lex national transposition)](https://eur-lex.europa.eu/legal-content/CS/TXT/PDF/?uri=NIM:272327), [epravo.cz](https://www.epravo.cz/top/clanky/novy-zakon-o-zpracovani-osobnich-udaju-109312.html) | 16 Sep 2026 |
| CZ: cookie consent (ePrivacy Art. 5(3)) | Opt-in consent required since 1 January 2022, § 89(3) of Act No. 127/2005 Sb. as amended by Act No. 374/2021 Sb. | [epravo.cz](https://www.epravo.cz/top/clanky/cookies-nove-jen-se-souhlasem-poslanecka-snemovna-prijala-zprisnujici-pravidla-od-roku-2022-113207.html) | 16 Sep 2026 |
| CZ: e-mail marketing (ePrivacy Art. 13) | Prior demonstrable consent, soft opt-in for own similar products, § 7 of Act No. 480/2004 Sb. | [ÚOOÚ FAQ](https://uoou.gov.cz/cinnost/obchodni-sdeleni/casto-kladene-otazky-k-zakonu-c-4802004-sb) | 16 Sep 2026 |
| CZ: AI Act authority | ČTÚ presented as the market surveillance authority. The national implementing act was still a bill in the sources found, `VERIFY` adoption | [ČTÚ](https://ctu.gov.cz/umela-inteligence), [zakonyprolidi.cz monitor](https://www.zakonyprolidi.cz/monitor/8163146.htm) | 16 Sep 2026 |
| CZ: data protection authority | Úřad pro ochranu osobních údajů (ÚOOÚ) | [uoou.gov.cz](https://uoou.gov.cz/) | 16 Sep 2026 |

## Summary

| Regulation | likely violation | gap | info | VERIFY |
|---|---|---|---|---|
| GDPR | 4 | 4 | 1 | 3 |
| ePrivacy | 2 | 1 | 1 | 2 |
| AI Act | 1 | 0 | 2 | 1 |
| DSA | 0 | 2 | 1 | 1 |
| Accessibility | 0 | 5 | 1 | 0 |

Top priorities, in order:

1. **A1** Chatbot is instructed to hide that it is an AI (AI Act Art. 50(1), applicable now).
2. **E1** Google Analytics and other third-party requests load before any consent, and the banner has no
   reject option.
3. **G3** Allergy and health information collected without an Art. 9 condition.
4. **G1** Privacy notice is missing almost all information required by Art. 13.
5. **E2 / G2** Newsletter consent pre-ticked and bundled with the privacy policy.

## Applicability

- **GDPR:** applies. Controller established in the EU, personal data collected via five forms and the chat.
- **ePrivacy (Czech Act 127/2005 Sb., § 89(3)):** applies. Analytics, third-party embeds and device
  storage are used.
- **AI Act:** applies to the chat assistant. By building the assistant and putting it into service
  under its own name on top of a third-party model, the operator is most likely the **provider** of that
  AI system for Art. 50(1), and the model vendor is the GPAI model provider, `VERIFY` role
  qualification. No Annex III high-risk use found.
- **DSA:** applies partially. Blog comments are stored and shown to the public, so the site is a
  hosting service and an online platform for that feature. The operator (6 employees, turnover under
  EUR 2 million) appears to be a micro enterprise, so Art. 19 disapplies Art. 20 to 28, while Art. 11 to
  18 still apply.
- **Accessibility:** no legal duty found. Not a public sector body (Web Accessibility Directive does not
  apply). Even if online event booking counted as an EAA-covered service, the operator appears to be a
  microenterprise providing services, exempt under Directive (EU) 2019/882 Art. 4(5). Findings below are
  WCAG best practice, not legal obligations.

## Findings

### GDPR

#### G1. Privacy notice lacks the information required by Art. 13

- Provision: GDPR Art. 12 and 13(1) to (2)
- Evidence: [`privacy.html:12-15`](cafe-site/privacy.html#L12-L15) contains three sentences. Missing:
  controller identity and contact, purposes per processing activity with legal bases, recipients
  (Google, LLM provider, hosting), third-country transfers, retention periods, data subject rights,
  right to complain to ÚOOÚ. Chat logs, bookings, comments and analytics are not mentioned at all.
- Risk: likely violation
- Confidence: high
- Why it matters: every form on the site collects data directly from the visitor, so Art. 13 information
  must be given at the time of collection.
- Suggested fix: replace with a full notice drafted from `references/templates/privacy-policy.md`, link
  it next to every form and in the chat widget.
- `VERIFY`: none

#### G2. Consent to newsletter is pre-ticked and bundled with the privacy policy

- Provision: GDPR Art. 4(11), 7(2), 7(4); recital 32
- Evidence: [`index.html:54-55`](cafe-site/index.html#L54-L55), checkbox `checked` by default, label
  "I agree to the privacy policy and want to receive the newsletter".
- Risk: likely violation
- Confidence: high
- Why it matters: pre-ticked boxes are not valid consent, and consent to marketing cannot be bundled with
  acknowledging a privacy notice (which is information, not something to "agree" to).
- Suggested fix: unticked, separate optional checkbox for the newsletter only; a plain link to the privacy
  notice with no checkbox.
- `VERIFY`: none

#### G3. Health data (allergies, health conditions) without an Art. 9 condition

- Provision: GDPR Art. 9(1), 9(2)(a); Art. 5(1)(c)
- Evidence: [`events.html:32-33`](cafe-site/events.html#L32-L33), free-text field "Dietary requirements,
  allergies, or health conditions we should know about". No explicit consent, no explanation of purpose.
- Risk: likely violation
- Confidence: medium (allergies disclosed for a specific person are generally treated as data concerning
  health; the free-text "health conditions" invites more than needed)
- Why it matters: special category data needs both an Art. 6 basis and an Art. 9(2) condition, and must
  be limited to what is necessary.
- Suggested fix: narrow the field to "Food allergies or intolerances relevant to the workshop", add a
  separate unticked explicit-consent checkbox, state the purpose and a short retention (e.g. deleted
  after the event), restrict access in the booking backend.
- `VERIFY`: retention and access control in `/api/bookings` (not provided).

#### G4. Children's data in event bookings

- Provision: GDPR Art. 6(1)(b), 8, 12(1), 13
- Evidence: [`events.html:30-31`](cafe-site/events.html#L30-L31), child's name and age collected via a form
  filled in by the parent.
- Risk: gap
- Confidence: medium
- Why it matters: Art. 8 (Czech age threshold 15, § 7 Act 110/2019 Sb.) applies only when consent is the
  basis for an information society service offered **directly to a child**. Here the parent books, so
  Art. 8 is most likely not triggered, but the booking must still have a clear basis (performance of a
  contract with the parent), and the notice must explain what happens to the child's data.
- Suggested fix: label the section "Parent or guardian booking for a child", collect only first name and
  age, cover it in the privacy notice. Do not use children's data for the newsletter or analytics.
- `VERIFY`: none

#### G5. Chat transcripts and IP addresses stored indefinitely

- Provision: GDPR Art. 5(1)(c), 5(1)(e), 13(2)(a)
- Evidence: [`server/chat.ts:12`](cafe-site/server/chat.ts#L12) and
  [`server/chat.ts:23`](cafe-site/server/chat.ts#L23), full conversation plus IP address inserted into
  `chatLogs` "for quality review", no deletion logic.
- Risk: likely violation
- Confidence: medium (retention may be handled in the database layer, which was not provided)
- Why it matters: visitors may type allergies, names or contact details into the chat. Keeping everything
  with an IP address forever is hard to justify as necessary.
- Suggested fix: do not store the IP, set a short retention (e.g. 30 days) with automatic deletion, tell
  users in the widget that conversations are stored and why.
- `VERIFY`: retention jobs in the database layer.

#### G6. Transfers to US-based services not documented

- Provision: GDPR Art. 13(1)(f), 44 to 46
- Evidence: Google Analytics ([`index.html:8`](cafe-site/index.html#L8)), YouTube, Google Maps, reCAPTCHA,
  Google Fonts, and the LLM API ([`server/chat.ts:1`](cafe-site/server/chat.ts#L1)) all receive visitor
  data (at least IP address; for the LLM API, full chat content).
- Risk: gap
- Confidence: medium
- Why it matters: each transfer needs a mechanism (e.g. EU-US Data Privacy Framework certification or
  SCCs) and must be disclosed.
- Suggested fix: list each recipient, its role (processor or independent controller), location and
  transfer mechanism in the privacy notice; sign the providers' data processing terms.
- `VERIFY`: whether each provider is currently certified under the EU-US Data Privacy Framework and
  whether the LLM API can be used with EU data residency.

#### G7. Blog comments store IP and email without information

- Provision: GDPR Art. 5(1)(c), 13
- Evidence: [`server/comments.ts:11`](cafe-site/server/comments.ts#L11) stores IP; email collected at
  [`blog/ai-latte-art.html:23-24`](cafe-site/blog/ai-latte-art.html#L23-L24).
- Risk: gap
- Confidence: high
- Suggested fix: explain purpose (abuse prevention) and retention for IP and email, or stop storing IP.

#### G8. Records of processing likely required despite small size

- Provision: GDPR Art. 30(1), 30(5)
- Evidence: bookings, newsletter and chat are regular, not occasional processing, and G3 includes special
  category data.
- Risk: gap
- Confidence: medium
- Why it matters: the under-250-employees exemption in Art. 30(5) does not apply where processing is not
  occasional or includes special categories.
- Suggested fix: draft a short record from `references/templates/ropa.md`.

#### G9. DPO and DPIA

- Provision: GDPR Art. 35, 37
- Evidence: small-scale processing, no systematic large-scale monitoring.
- Risk: info
- Confidence: medium
- Why it matters: a DPO is most likely not required; a full DPIA is most likely not required. Revisit if
  chat logs or health data grow in scale.

### ePrivacy

#### E1. Analytics and third-party content load before consent; banner has no reject option

- Provision: ePrivacy Directive Art. 5(3) as transposed in § 89(3) Act 127/2005 Sb.; GDPR Art. 4(11), 7
- Evidence:
  - [`index.html:8-14`](cafe-site/index.html#L8-L14): gtag.js loaded and configured unconditionally in
    `<head>`, before [`cookie-banner.js`](cafe-site/assets/cookie-banner.js) runs.
  - [`events.html:8`](cafe-site/events.html#L8): gtag.js loaded unconditionally.
  - [`assets/cookie-banner.js:9-10`](cafe-site/assets/cookie-banner.js#L9-L10): only "Accept all"; the
    "Settings" link just opens the privacy page. Accepting sets a flag but nothing is blocked or
    unblocked by it.
  - [`privacy.html:13-14`](cafe-site/privacy.html#L13-L14): "By using this site you agree to our use of
    cookies", implied consent.
- Risk: likely violation
- Confidence: high for the code path; runtime cookie list not tested
- Why it matters: Czech law has required opt-in consent for non-essential cookies since 1 January 2022.
- Suggested fix: load Google Analytics only after an explicit "Accept analytics" choice (or switch to a
  configuration that does not need consent, `VERIFY` with ÚOOÚ guidance); add an equally prominent
  "Reject all" button; add a persistent "Cookie settings" link in the footer; remove implied-consent text.
- `VERIFY`: which cookies are actually set on first load, using browser dev tools.

#### E2. Pre-ticked marketing consent

- Provision: ePrivacy Directive Art. 13 as transposed in § 7 Act 480/2004 Sb.
- Evidence: see G2, [`index.html:54`](cafe-site/index.html#L54).
- Risk: likely violation
- Confidence: high
- Suggested fix: see G2. Every newsletter must include a working unsubscribe link.
- `VERIFY`: whether the newsletter backend uses double opt-in and records proof of consent (backend not
  provided).

#### E3. Third-party embeds transmit IP addresses before any choice

- Provision: ePrivacy Art. 5(3) (where cookies are set); GDPR Art. 6, 44 (IP transfer)
- Evidence: YouTube [`index.html:36`](cafe-site/index.html#L36), Google Maps
  [`index.html:39`](cafe-site/index.html#L39), reCAPTCHA
  [`index.html:57`](cafe-site/index.html#L57), Google Fonts
  [`assets/styles.css:1`](cafe-site/assets/styles.css#L1).
- Risk: gap
- Confidence: medium
- Suggested fix: self-host the two fonts; use `youtube-nocookie.com` behind a click-to-load placeholder;
  replace the Maps iframe with a static image linking to the map; consider a CAPTCHA alternative or load
  reCAPTCHA only when the form is used.

#### E4. Chat history in `localStorage`

- Provision: ePrivacy Art. 5(3)
- Evidence: [`assets/chat-widget.js:13`](cafe-site/assets/chat-widget.js#L13),
  [`assets/chat-widget.js:25`](cafe-site/assets/chat-widget.js#L25).
- Risk: info
- Confidence: medium
- Why it matters: storing the conversation the user started is arguably strictly necessary for the chat
  service they requested, so consent is likely not needed, but it should be disclosed and limited in
  time.

### AI Act

#### A1. Chatbot is designed to conceal that it is an AI

- Provision: AI Act Art. 50(1), applicable from 2 August 2026
- Evidence: [`server/chat.ts:8`](cafe-site/server/chat.ts#L8), system prompt "Never mention that you are
  an AI"; the widget presents a human persona "Anna from Example Café"
  ([`assets/chat-widget.js:8`](cafe-site/assets/chat-widget.js#L8)) with no disclosure.
- Risk: likely violation
- Confidence: high
- Why it matters: people interacting with an AI system must be informed of it unless it is obvious. A
  human name and an instruction to hide the AI make it deliberately non-obvious.
- Suggested fix: add a visible disclosure in the widget header (template in
  `references/templates/ai-transparency-notice.md`), rename the persona or label it "AI assistant",
  remove the concealment instruction and have the assistant confirm it is an AI when asked.
- `VERIFY`: role qualification (provider vs deployer), see Applicability. The duty exists in either
  case, only the addressee changes.

#### A2. AI-generated blog images

- Provision: AI Act Art. 50(4)
- Evidence: [`blog/ai-latte-art.html:14`](cafe-site/blog/ai-latte-art.html#L14), owner confirms header
  images are AI-generated; the image shows a clearly fictional robot barista.
- Risk: info
- Confidence: medium
- Why it matters: the Art. 50(4) disclosure duty covers deep fakes, content that resembles real people,
  places or events and would falsely appear authentic. An obviously fictional illustration is unlikely to
  qualify, but a short "Image: AI-generated" caption is cheap and builds trust. Photos of the café or
  staff generated or altered by AI would need a label.

#### A3. AI literacy

- Provision: AI Act Art. 4
- Evidence: organizational, not visible in code.
- Risk: info
- Confidence: low
- Suggested fix: brief staff who maintain the chatbot on what it can get wrong, especially allergen
  answers, which should point to staff rather than be answered by the AI alone.

### DSA

#### D1. No mechanism to report illegal comments

- Provision: DSA Art. 16
- Evidence: comments published immediately ([`server/comments.ts:12`](cafe-site/server/comments.ts#L12));
  no "report" link or form on [`blog/ai-latte-art.html`](cafe-site/blog/ai-latte-art.html).
- Risk: gap
- Confidence: high
- Suggested fix: add a "Report this comment" link to a simple form (reason, explanation, reporter's
  contact) and a confirmation of receipt.

#### D2. No statement of reasons or contact point

- Provision: DSA Art. 11, 12, 14, 17
- Evidence: comments can be deleted ([`server/comments.ts:19`](cafe-site/server/comments.ts#L19)) without
  notifying the author; no published contact point; no terms for comments.
- Risk: gap
- Confidence: medium
- Suggested fix: short comment rules page (what is removed and how), email the author a brief reason when
  a comment is removed, publish a single contact point.

#### D3. Micro enterprise exemption

- Provision: DSA Art. 19
- Evidence: owner reports 6 employees and turnover under EUR 2 million.
- Risk: info
- Confidence: medium
- Why it matters: online platform duties in Art. 20 to 28 (internal complaints, dark patterns, ad and
  recommender transparency, minors) do not apply.
- `VERIFY`: enterprise size including any linked or partner enterprises (Recommendation 2003/361/EC).

### Accessibility (best practice, no legal duty found)

#### X1. Missing `lang` and viewport on the home page

- Provision: WCAG 2.2 SC 3.1.1 Language of Page; SC 1.4.10 Reflow (viewport)
- Evidence: [`index.html:2`](cafe-site/index.html#L2) `<html>` without `lang`; no viewport meta tag.
- Risk: gap
- Confidence: high

#### X2. Images without text alternatives

- Provision: WCAG 2.2 SC 1.1.1
- Evidence: [`index.html:20`](cafe-site/index.html#L20) (logo), [`index.html:33`](cafe-site/index.html#L33)
  (interior photo).
- Risk: gap
- Confidence: high

#### X3. Form fields without labels

- Provision: WCAG 2.2 SC 1.3.1, 3.3.2, 4.1.2
- Evidence: newsletter email [`index.html:43`](cafe-site/index.html#L43) and message textarea
  [`index.html:53`](cafe-site/index.html#L53) rely on placeholder text only.
- Risk: gap
- Confidence: high

#### X4. Menu toggle not keyboard-accessible

- Provision: WCAG 2.2 SC 2.1.1, 4.1.2
- Evidence: [`index.html:21`](cafe-site/index.html#L21), `<div onclick>` instead of `<button>`.
- Risk: gap
- Confidence: high

#### X5. Insufficient text contrast

- Provision: WCAG 2.2 SC 1.4.3 (4.5:1 for normal text)
- Evidence: body text `#9a9a9a` on `#ffffff` is 2.81:1
  ([`assets/styles.css:3`](cafe-site/assets/styles.css#L3)); cookie "Settings" link `#555` on `#222` is
  2.13:1 ([`assets/styles.css:6`](cafe-site/assets/styles.css#L6)), which also makes the only non-accept
  option in the cookie banner hard to see (see E1).
- Risk: gap
- Confidence: high

#### X6. Heading level skipped

- Provision: WCAG 2.2 SC 1.3.1 (advisory)
- Evidence: [`index.html:31-32`](cafe-site/index.html#L31-L32), `<h1>` followed by `<h3>`.
- Risk: info
- Confidence: high

## What the scanner found vs. manual review

The heuristic scan ([`cafe-site-scan.txt`](cafe-site-scan.txt)) pointed to E1, E2/G2, E3, E4, D1, X1
to X4 and X6, and flagged the chat code that led to A1. Manual review was needed for everything else:
health data in a free-text field (G3), children's data (G4), retention and IP logging in server code
(G5, G7), the "never mention AI" instruction (A1), the outdated privacy text (G1), AI-generated images
(A2) and color contrast (X5) are not detectable by the scanner's pattern matching.

## Facts needed from the site owner

- Company ID (IČO), registered address, and a contact email for privacy requests
- Retention periods for bookings, contact messages, comments and chat logs
- Which LLM provider and region are used, and whether its data processing terms are signed
- Whether the newsletter tool uses double opt-in, and which tool it is
- Whether Google Analytics is essential to the business or could be replaced with a consent-free setup
- Confirmation of enterprise size (including linked enterprises)

## Next step

A remediation plan with proposed file changes and draft documents follows in
[`cafe-site-remediation-plan.md`](cafe-site-remediation-plan.md). No files have been changed and no
documents published; that happens only after your approval.
