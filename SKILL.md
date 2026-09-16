---
name: eu-web-compliance
description: "Use when building, reviewing, or preparing to publish a website or web app subject to EU digital law: GDPR, ePrivacy (cookies, e-marketing), the EU AI Act, the Digital Services Act, or EU accessibility rules (EAA, Web Accessibility Directive, WCAG). Triggers: requests to check or improve 'GDPR compliance', 'cookie consent', 'privacy policy', 'AI Act', 'accessibility' or 'WCAG' for a site; requests to draft a privacy policy, cookie policy, DPIA, records of processing, or accessibility statement; reviewing a site 'before it goes live' or 'for EU users'. Also use proactively when generating a site that collects personal data (forms, accounts, newsletters, analytics, chat widgets) or uses an AI feature. Produces a sourced findings report and draft materials for human review; it is not a substitute for a lawyer or DPO and never asserts final legal certainty."
license: Apache-2.0
---

# EU Web Compliance

Analyzes a website's code and content against current EU digital law (GDPR, ePrivacy, AI Act, DSA,
accessibility rules), produces a sourced findings report, and drafts remediation, code changes, and
legal documents for the user to review and approve.

## Non-negotiable rules

1. **This is not legal advice.** Say so in every report. The output supports a human decision, a
   lawyer or DPO makes the final call on anything with real regulatory exposure.
2. **Never invent a citation.** Article numbers, regulation numbers, deadlines, national provisions,
   case law, DPA guidance: if you did not verify it in this session (from the reference files below,
   which are stable primary-law text, or from a fresh web search for anything time-sensitive), mark
   it `VERIFY` instead of stating it as fact. A wrong citation is worse than an honest gap.
3. **EU digital law is a moving target in 2026 to 2027.** The GDPR's core articles are stable. The AI
   Act's timeline, the "Digital Omnibus" package amending the GDPR and ePrivacy rules, and national
   implementing law are all actively changing. Before stating any deadline, threshold, or provision
   that is less than roughly two years old, do a web search for its current status and name the
   source and the date you checked it. Never silently rely on a hardcoded date in these reference
   files without confirming it is still current.
4. **Never edit site files or publish a legal document without a prior written change plan and
   explicit user approval.** Show what will change, where, and why, then wait.
5. **Preserve the site owner's own words.** Fix compliance defects, do not rewrite content, tone, or
   structure that is not a compliance problem. When drafting a new document (privacy policy etc.),
   ask for the missing facts rather than inventing company details, addresses, or contact data.
6. **Scope every obligation before asserting it applies.** GDPR applies broadly, but the DSA and the
   accessibility rules have size, sector, or audience thresholds. State the threshold and whether this
   site meets it, or mark it `VERIFY`.

## Workflow

### Step 1: Establish context

Do not guess. Confirm with the user, or read it directly from the code if it is unambiguous there:

- What does the site do, and who is the intended audience (which country or countries)?
- What personal data does it collect or plan to collect (contact forms, accounts, newsletters,
  payments, event or membership registration, photos of identifiable people)?
- Does the site involve children, or content directed at children?
- Does the site use any AI feature (chatbot, generated text/image/audio/video, recommendations,
  personalization, automated decisions)?
- Does it have comments, forums, marketplace listings, user uploads, or advertising (relevant to the
  DSA)?
- Is there an identifiable legal entity or natural person operating the site, and in which EU member
  state (or outside the EU, if targeting EU users) are they established? This determines which
  national data protection authority, which national implementing law, and which accessibility regime
  applies.

If the user only wants a specific slice of the review (for example, only cookies, or only
accessibility), scope the work to that and say so in the report, rather than running the full check
silently.

### Step 2: Scan the code

Read the relevant source files (HTML, JS/TS, server templates, CMS config, form handlers, cookie
banner config) directly. For larger codebases, first run the scanner against the site root to get a
fast structured inventory (external domains referenced, cookie- and tracking-related code, third-party
embeds, forms and their fields, pre-ticked checkboxes, `<img>` tags without `alt`, missing
`lang`/`viewport`, clickable non-button elements, skipped heading levels, AI/API calls, ad code,
comment/upload mechanisms):

```bash
python3 scripts/scan.py /path/to/site --domain example.com        # human-readable summary
python3 scripts/scan.py /path/to/site --domain example.com --json # per-file detail
```

`--domain` (repeatable) excludes the site's own domain(s) from the external-request list. `--exclude`
(repeatable glob, e.g. `public`, `"design/*"`, `"*.dc.html"`) skips files that are not published. The
path is relative to this skill's folder. Treat the script's output as a lead list, not a verdict,
confirm anything material by reading the actual code.

**Static site generators** (Hugo, Jekyll, Eleventy, Astro, Next.js static export, etc.): build the site
and scan the output folder (`public/`, `_site/`, `dist/`, `out/`), because that is what visitors
receive; read the templates by hand to find where to fix things. Minified HTML is normal input, the
scanner handles unquoted and bare attributes. If the scanner warns that build output sits next to the
sources, the findings are doubled, rerun it on the output folder or with `--exclude`.

### Step 2b: Check the running site

Code shows intent, the browser shows what actually happens, and in practice the most important findings
often come from here. If the site is live or a local build can be served, and a browser tool is
available, check at runtime and record the URL, date, browser, locale, and viewport widths in the report.
If it cannot be done, say so and mark code-only findings accordingly.

- **Pin the language first on multilingual sites.** Sites that pick a language from
  `navigator.languages`, a cookie, or a locale redirect will silently show a test browser (usually
  English) the wrong version. Set the choice explicitly (the site's own `localStorage` key or cookie,
  or the `Accept-Language` header), check `location` after load, and repeat key checks per language.
- **Cookies, storage, third-party requests** before any consent choice, after "reject", and after
  "accept": `eprivacy-checklist.md`, section 5.
- **Where the server really is and who runs it** (IP → ASN → provider): `gdpr-checklist.md`,
  section 14.
- **Accessibility at runtime**: automated checker results including "incomplete" items, text contrast
  over images, keyboard and focus behavior with menus and overlays: `accessibility-checklist.md`,
  section 4.

### Step 3: Ground the analysis in current law

Load the checklist(s) relevant to what Step 1 revealed, from `references/`:

- `references/gdpr-checklist.md`, always
- `references/eprivacy-checklist.md`, if there are cookies, trackers, or marketing
- `references/ai-act-checklist.md`, if there is any AI feature
- `references/dsa-checklist.md`, if there are comments, uploads, marketplace features, or ads
- `references/accessibility-checklist.md`, always, since WCAG is good practice even where EAA/WAD do
  not strictly apply
- `references/national-law-guide.md`, to identify what to search for the site's specific member state

Then web search, at minimum: current status of the AI Act implementation timeline for the obligations
in play, current status of the GDPR/ePrivacy "Digital Omnibus" proposal (do not treat any of its
provisions as current law unless a search confirms adoption), and the national provision(s) flagged by
`national-law-guide.md` for the site's jurisdiction. Record the date of these checks in the report.

### Step 4: Report findings

Produce a structured report using `references/templates/findings-report.md`, grouped by regulation,
each finding stating: the article or provision,
what was found in the code or content, a risk label (`info` / `gap` / `likely violation`), and a
confidence level. Anything not independently verified gets `VERIFY` with a note on what to check and
where. Do not smooth over uncertainty to make the report read more authoritative than it is.

### Step 5: Consult before changing anything

Present a remediation plan: what would change, in which files, and draft text for any new or updated
document (privacy policy, cookie policy, DPIA, records of processing, AI transparency notice,
accessibility statement), built
from `references/templates/`. List missing facts you need from the user (legal entity name, address,
DPO contact, retention periods, sub-processors, etc.) rather than inventing them. Let the user approve
the whole plan or go item by item. Only after approval, edit files or write the documents out.

### Step 6: Deliverables

- The findings report (markdown)
- Draft legal documents as needed, filled in only with confirmed facts, placeholders left visible for
  anything unconfirmed
- The list of code changes made, or proposed and pending approval

## Reference files

| File | Covers |
|---|---|
| `references/gdpr-checklist.md` | GDPR: lawful basis, consent, transparency, data subject rights, children's data, special categories (incl. donations to religious bodies), security, breach notification, DPO, records, international transfers, processor chain and real hosting location |
| `references/eprivacy-checklist.md` | Cookie/tracker consent, direct electronic marketing, third-party embeds, runtime verification of cookies and requests |
| `references/ai-act-checklist.md` | Prohibited practices, transparency for AI-generated/interactive content, high-risk classification, GPAI, current timeline caveats |
| `references/dsa-checklist.md` | Intermediary/hosting obligations, notice-and-action, dark patterns, ad transparency, applicability thresholds |
| `references/accessibility-checklist.md` | WCAG technical checks, EAA and Web Accessibility Directive applicability, runtime checks (text over images, focus with overlays) |
| `references/national-law-guide.md` | What to verify per member state, and how to search for it |
| `references/templates/findings-report.md` | Structure of the Step 4 findings report |
| `references/templates/` (other files) | Draft privacy policy, cookie policy, DPIA, records of processing (ROPA), AI transparency notice, accessibility statement |
| `scripts/scan.py` | Fast, dependency-free structural scan of a site's source for the signals above |

## Limits

This skill supports judgment, it does not replace one. It cannot confirm facts about a business that
are not in the code or given by the user (legal entity, contracts with processors, actual retention
practice). It cannot certify legal compliance. For anything with real regulatory or financial exposure,
say so plainly and recommend the user get a lawyer or DPO to review before relying on the output.
