---
type: llm
focus: {source: file, path: compliance-report.md}
---
The report contains a finding that meets BOTH of these:
1. It says Google Analytics / gtag (or other third-party analytics) loads before the visitor has given any consent.
2. It cites the ePrivacy rule on storing or accessing information on a device (Directive 2002/58/EC Art. 5(3)) and/or the Czech implementing provision.
Pass only if both hold. Any severity wording (blocking, high, likely violation, gap) is acceptable; only a finding that treats it as a non-issue fails.
