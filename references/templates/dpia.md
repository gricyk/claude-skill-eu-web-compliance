# Data Protection Impact Assessment (DPIA) template, GDPR Art. 35

Use only where a real indicator of likely high risk is present (large-scale special-category
processing, systematic monitoring, processing involving children at scale, new technology with
uncertain risk, automated decision-making with significant effect). For an ordinary small site this is
usually not legally required, note that assessment first rather than generating a DPIA reflexively.

---

## DPIA: {{processing_activity_name}}

Date: {{date}}
Conducted by: {{author}}

### 1. Description of the processing

- What: {{description}}
- Why (purpose): {{purpose}}
- Scope: {{data_categories}}, {{data_subjects}}, {{volume}}, {{retention}}
- Context: {{relationship_to_data_subjects}}

### 2. Necessity and proportionality

- Lawful basis: {{legal_basis}}
- Is the processing necessary for the stated purpose, or is there a less intrusive way to achieve it?
  {{necessity_analysis}}
- Data minimisation check: {{minimisation_analysis}}

### 3. Risk to individuals

| Risk | Likelihood | Severity | Notes |
|---|---|---|---|
| {{risk_1}} | {{low/medium/high}} | {{low/medium/high}} | {{notes}} |

### 4. Measures to address the risks

{{mitigation_measures}}

### 5. Outcome

- Residual risk after mitigation: {{residual_risk}}
- {{#if residual_risk_high}}Prior consultation with {{supervisory_authority_name}} required under
  Art. 36, before processing begins.{{/if}}
- Sign-off: {{signoff_name}}, {{signoff_date}}
