# Test Plan and User Acceptance Testing

## Automated checks
- Incident creation rejects missing required fields.
- Saved incident persists across API requests.
- Stage changes follow the specified five-stage sequence.
- Action notes and timestamps persist.
- Assessment with missing facts returns 'Needs review'.
- Report draft includes only recorded case facts and identifies missing information.
- Historical incident records and lessons learned are retrievable.

## Tabletop exercise (synthetic)
Scenario: An employee at a fictional Nigerian SME sends a spreadsheet containing customer contact information to an unintended external recipient. Detection time, exposure, recipients, and any subsequent access are initially uncertain.

Participant tasks: register the event; classify it provisionally; document containment; investigate affected data and recipients; complete notification decision questions; draft a report; record lessons learned.

## UAT checklist
- [ ] Register case without technical assistance.
- [ ] Find the case in the incident register.
- [ ] Move through five workflow stages and preserve notes.
- [ ] Use the playbook for a next-action suggestion.
- [ ] Record uncertainty in the notification questionnaire.
- [ ] Generate and edit report draft.
- [ ] Record a lesson learned and retrieve it.
- [ ] Record time taken and missing documentation.

## Measures (from proposal's validation direction)
Elapsed time to complete the scenario; proportion of required incident fields completed; number of missing evidence/notification questions; UAT pass/fail and user feedback. No baseline improvement claim without comparative testing.

## Development environment
Run tests locally on Windows from VS Code; OpenCode with Beam Free may assist with test creation, but results must come from executed tests.
