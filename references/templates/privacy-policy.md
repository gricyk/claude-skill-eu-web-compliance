# Privacy Policy template

Fill every `{{placeholder}}` from confirmed facts given by the user. Never invent a legal entity name,
address, DPO contact, retention period, or sub-processor. If a fact is missing, leave the placeholder
visible and list it in the "missing facts" section of the change plan presented to the user, do not
guess a plausible-sounding value.

---

## Privacy Policy

Last updated: {{date}}

### 1. Who we are

{{controller_name}} ("we", "us"), {{controller_address}}, is the controller responsible for your
personal data in connection with this website ({{site_url}}).

Contact: {{contact_email}}
{{#if dpo_appointed}}Data Protection Officer: {{dpo_name}}, {{dpo_contact}}{{/if}}

### 2. What data we collect and why

| Data collected | Purpose | Legal basis (GDPR Art. 6) | Retention |
|---|---|---|---|
| {{data_item_1}} | {{purpose_1}} | {{basis_1}} | {{retention_1}} |
| {{data_item_2}} | {{purpose_2}} | {{basis_2}} | {{retention_2}} |

{{#if special_category_data}}
### 2a. Special category data

We process {{special_category_description}} (Art. 9 GDPR). Our basis for this is
{{art9_condition}}. {{additional_safeguards}}
{{/if}}

{{#if children_data}}
### 2b. Children

{{child_data_description}}. Where the person providing data is a child, we {{parental_consent_process}}.
{{/if}}

### 3. Who we share data with

{{#each recipients}}
- {{name}}, for {{purpose}}, located in {{location}}{{#if outside_eea}}, transferred under
  {{transfer_mechanism}}{{/if}}
{{/each}}

### 4. Your rights

You have the right to access, correct, delete, or restrict the use of your data, to receive a copy of
it in a portable format, and to object to certain processing. To exercise these rights, contact us at
{{contact_email}}. You also have the right to lodge a complaint with {{supervisory_authority_name}}
({{supervisory_authority_url}}), the data protection authority in {{country}}.

### 5. Cookies

See our separate [Cookie Policy]({{cookie_policy_url}}).

### 6. Automated decision-making

{{#if automated_decisions}}
{{automated_decision_description}}, including the logic involved, its significance, and the envisaged
consequences.
{{else}}
We do not use automated decision-making, including profiling, that produces legal or similarly
significant effects on you.
{{/if}}

### 7. Security

{{security_measures_summary}}

### 8. Changes to this policy

We may update this policy from time to time. The date at the top shows the last revision.
