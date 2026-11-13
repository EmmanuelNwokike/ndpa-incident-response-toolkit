# Architecture — NDPA Incident Response Toolkit

## Three-tier architecture (specified in methodology)
1. Presentation: React/TypeScript web UI.
2. Business logic: FastAPI REST endpoints and deterministic workflow/decision-tree services.
3. Data: SQLite database via SQLAlchemy.

Browser → React UI → FastAPI → workflow service / reporting service / notification questionnaire → SQLite.

## Domain flow
Detection (register) → Triage (classify) → Containment (actions) → Investigation (findings/evidence metadata) → Reporting (review and drafts). Record transitions and user notes.

## Proposed API (design decisions)
- GET /health
- GET, POST /incidents
- GET, PATCH /incidents/{id}
- POST /incidents/{id}/actions
- POST /incidents/{id}/assessment
- GET /incidents/{id}/report
- POST /incidents/{id}/lessons
- GET /playbook
- GET /tabletop/scenarios

## Rules
Do not automatically classify any incident as legally reportable from incomplete information. Store questionnaire answers and reviewed determination separately. Record legal-rule version. Deadline calculations must remain disabled until the applicable trigger and conditions are verified.

## Security and data handling
Synthetic demonstration data only; validate all inputs; log state changes; avoid raw evidence uploads in MVP; avoid storing secrets in repository; implement authorization if user accounts are included.

## Future extension, not current scope
Live monitoring integrations, enterprise-grade evidence custody, regulator submission and agentic AI.

## Development tooling (not runtime)
Develop on Windows in VS Code using OpenCode with Beam Free for coding assistance. No OpenCode/Beam Free dependency or API call is part of the application architecture.
