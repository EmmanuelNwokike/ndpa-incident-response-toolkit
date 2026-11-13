# AGENTS.md — NDPA Toolkit Engineering Instructions

## Mission
Implement the attached undergraduate proposal faithfully. This is a deterministic incident response and breach-reporting toolkit for Nigerian SMEs, **not** an agentic AI application.

## Strict scope
Use Detection → Triage → Containment → Investigation → Reporting. Deliver playbook, decision tree, templates, tabletop exercise and lightweight web prototype. Include historical incident records and lessons learned. Use simulated data.

## Technology (implementation choices)
Windows 10/11, VS Code + OpenCode (Beam Free), React + TypeScript + Vite, Tailwind CSS, Python + FastAPI, SQLite + SQLAlchemy, pytest. Do not install Ollama, Qwen, LangChain, CrewAI or other model runtimes. Do not import Matplotlib unless a concrete requirement demands it.

## Coding assistant workflow
Use OpenCode with the Beam Free model/provider selected in its interface. OpenCode is a development assistant only; no model calls belong in the deployed application. Do not assume model identifiers or API keys. Work in the VS Code project directory, read these instructions and docs first, and stop after the first vertical slice for review.

## Working rules
1. Read docs/PRD.md, docs/ARCHITECTURE.md and docs/IMPLEMENTATION_PLAN.md before coding.
2. Inspect existing files before creating or overwriting them.
3. Implement the smallest vertical slice first: create incident → persist → view → update stage → generate draft.
4. Use rule-based logic, never generated legal assertions.
5. Keep legal rules in a separate, versioned module with citations/placeholders for verification; unresolved legal questions must yield 'Needs review'.
6. No real client data or credentials in sample records.
7. Use validation, parameterized database access/ORM, safe error handling and authorization for sensitive actions.
8. Keep each feature testable; run tests after changes; report actual test results, not assumptions.
9. Do not send external notifications or connect live security tools.
10. Prefer a complete, locally runnable demonstration to speculative extra features.

## Completion report
Report implemented features, commands run, tests passed/failed, unimplemented requirements, known limitations and next steps.
