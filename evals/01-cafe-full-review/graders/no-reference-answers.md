---
type: regex
target: trace
match: not_contains
# The skill is loaded from the repo, so the agent can reach examples/*-report.md and
# *-remediation-plan.md, the reference answers for the fixture sites. Fail the run if
# any tool call names one. Only tool_use inputs count, not directory listings.
---
"type":"tool_use"[^\n]*?examples/[\w.-]+-(?:report|remediation-plan)\.md
