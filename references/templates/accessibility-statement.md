# Accessibility Statement template

Legally required for public sector bodies under the Web Accessibility Directive (EU) 2016/2102, where
the Commission's model statement (Implementing Decision (EU) 2018/1523) and national rules define the
content, `VERIFY` both before publishing. For private-sector services covered by the European
Accessibility Act, a similar statement is a practical way to provide the Annex V service information.
For everyone else it is voluntary good practice, say so rather than implying a legal duty.

Only claim the conformance level that was actually tested. List known issues honestly, an accurate
"partially compliant" statement is better than an unsupported "fully compliant" one.

---

## Accessibility Statement

{{organization_name}} is committed to making {{site_url}} accessible to as many people as possible,
including people with disabilities.

### Compliance status

This website is {{fully / partially / not}} compliant with {{standard, e.g. WCAG 2.1 Level AA / EN 301 549}}.
{{#if partially_or_not}}The non-compliances and exemptions are listed below.{{/if}}

### Non-accessible content

{{#each known_issues}}
- {{issue_description}} ({{wcag_success_criterion}}). {{planned_fix_and_date_or_alternative}}
{{/each}}

{{#if disproportionate_burden_claimed}}
### Disproportionate burden

{{content_and_justification}}. `VERIFY` that the national rules allow this claim and that an assessment
was actually carried out.
{{/if}}

### Preparation of this statement

This statement was prepared on {{date}} and last reviewed on {{review_date}}. The assessment method was
{{self-assessment / third-party audit by {{auditor}}}}.

### Feedback and contact

If you find an accessibility problem or need information in an accessible format, contact us:

- Email: {{contact_email}}
- {{other_contact_channel}}

We aim to respond within {{response_time}}.

{{#if public_sector}}
### Enforcement procedure

If you are not satisfied with our response, you can contact {{national_enforcement_body}}
({{enforcement_body_url}}).
{{/if}}
