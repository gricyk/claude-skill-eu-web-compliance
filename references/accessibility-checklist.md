# Accessibility checklist (WCAG, European Accessibility Act, Web Accessibility Directive)

Three different things are easy to conflate here, keep them separate in the report.

## 1. Which legal regime, if any, actually applies

- **Web Accessibility Directive (EU 2016/2102)**: binds public sector bodies' websites and mobile
  apps. If the site belongs to a public authority, this applies, and normally requires a published
  accessibility statement with a feedback mechanism (draft one from
  `templates/accessibility-statement.md`). The technical benchmark is the harmonised standard
  EN 301 549, whose V3.2.1 maps to WCAG 2.1 Level AA; a V4.1.1 was published in September 2026, `VERIFY` which version is currently cited in the Official Journal and what it references.
- **European Accessibility Act (Directive (EU) 2019/882)**: binds specific private-sector products and
  services, e-commerce, banking, e-books, certain transport and telecom services, among others, with
  requirements applicable from 28 June 2025 (national transposition laws apply, with transitional
  periods for some existing services, `VERIFY` per member state). Check whether the specific site
  actually falls into one of the EAA's covered service categories, plenty of ordinary informational,
  community, or non-commercial sites do not, `VERIFY` applicability against the current list of covered
  services rather than assuming it applies just because the organization is EU-based.
  - **Microenterprises providing services are exempt** (Art. 4(5)): fewer than 10 persons and annual
    turnover or balance sheet total not exceeding EUR 2 million. A small online shop may therefore be
    outside the EAA even though e-commerce is a covered service, state this explicitly when it applies.
  - Covered service providers must publish information on how the service meets the accessibility
    requirements (Annex V), typically in the terms and conditions or an accessibility statement.
- **No specific legal duty**: many non-commercial, non-public-sector sites (church, community group,
  personal, informational) fall outside both regimes as a strict legal matter. Say so plainly if that
  is the case, and frame WCAG conformance as strong best practice and an expression of care for
  disabled visitors, not as a claimed legal requirement, overstating legal duty where none exists is
  also a credibility problem.

## 2. Technical baseline regardless of legal duty (WCAG, aim for 2.1 or 2.2 Level AA)

**Perceivable**
- Every meaningful `<img>` has descriptive `alt` text, purely decorative images have `alt=""`.
- Sufficient color contrast (roughly 4.5:1 for normal text, 3:1 for large text).
- Video/audio content has captions or a transcript.
- Content and layout do not rely on color alone to convey information.

**Operable**
- Entire site usable by keyboard alone, visible focus indicator on interactive elements.
- No content that flashes more than three times per second.
- Skip-to-content link for pages with repeated navigation.
- Touch targets sized and spaced for mobile use.

**Understandable**
- `<html lang="...">` set correctly, and set again for any passage in a different language.
- Form fields have visible, programmatically associated labels (`<label for>` matching the input `id`,
  not placeholder text used as the only label).
- Error messages are specific and describe how to fix the problem, not just "invalid input".
- Navigation and interaction patterns are consistent across the site.

**Robust**
- Valid, semantic HTML (headings in logical order, lists as `<ul>/<ol>`, buttons as `<button>` not a
  styled `<div>` with a click handler).
- ARIA used only where native HTML semantics are insufficient, and used correctly, incorrect ARIA is
  often worse than none.

## 3. Practical scan targets

Missing `alt`, missing `lang`, missing `<label for>`/`aria-label` on inputs, non-button clickable
`<div>`/`<span>` elements, heading levels that skip (e.g. `<h1>` straight to `<h4>`), and low-contrast
color combinations in the CSS, are the highest-value, cheapest-to-fix items to flag first.
