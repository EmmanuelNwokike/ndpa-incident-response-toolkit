# User Acceptance Testing Scenarios (Synthetic)

## Scenario 1: Phishing-related credential compromise
- Initial description: A staff member at a fictional Nigerian SME clicks a phishing link and enters credentials; suspicious login detected.
- Expected stages: Detection -> Triage -> Containment -> Investigation -> Reporting.
- Required records: incident, affected system, severity, containment actions, investigation findings, assessment, report draft, lessons learned.
- Expected report output: incident report draft with missing information list.
- Acceptance criteria: case registered, moved through all five stages, report draft generated and edited, lesson recorded.
- Measures: elapsed time; proportion of required fields completed; number of missing evidence/notification questions.

## Scenario 2: Unauthorized disclosure of customer personal information
- Initial description: An employee emails a customer contact spreadsheet to an unintended external recipient.
- Expected stages: Detection -> Triage -> Containment -> Investigation -> Reporting.
- Required records: incident, affected data categories, affected people estimate, containment, assessment (Needs review), report draft.
- Expected report output: draft breach notification (human review required).
- Acceptance criteria: uncertainty recorded; assessment returns Needs review; notification draft labeled draft.
- Measures: elapsed time; documentation completeness.

## Scenario 3: Ransomware affecting an SME's business systems
- Initial description: Ransomware encrypts files on an SME's shared drive; systems isolated.
- Expected stages: Detection -> Triage -> Containment -> Investigation -> Reporting.
- Required records: incident, containment actions with owners/outcomes, evidence metadata, assessment, report, lessons.
- Expected report output: incident report draft plus breach notification draft.
- Acceptance criteria: containment documented, timeline visible, report drafts editable.
- Measures: elapsed time; documentation completeness; missing questions count.

No observed performance results are recorded; these are templates for UAT execution.
