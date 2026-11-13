# Two-hour Implementation Plan (Windows)

## 0–15 minutes — Preflight and documents
Confirm Python, Node/npm, Git, VS Code, and OpenCode configured with Beam Free; read PRD and architecture; create repository and folder layout.

## 15–35 minutes — Backend and persistence
Set up FastAPI, SQLAlchemy, SQLite and migrations/create tables. Add health endpoint, incident CRUD and tests.

## 35–65 minutes — UI and workflow
Build dashboard, incident list, incident creation and detail screens. Implement five-stage transition and action notes.

## 65–90 minutes — Toolkit deliverables
Implement stage-specific playbook, notification questionnaire with 'Needs review' outcome, editable report template and lessons learned.

## 90–105 minutes — Tabletop exercise
Add one synthetic incident scenario and checklist for response time/documentation completeness.

## 105–120 minutes — Validation
Run pytest and frontend build; perform manual end-to-end UAT. Document defects and unimplemented features.

## Definition of done
A Windows user can run frontend and backend locally; create and track a synthetic incident; follow the playbook; save a notification assessment; produce a report draft; record lessons learned; and execute a basic tabletop/UAT scenario.

## Prioritization if behind schedule
Keep incident persistence, five-stage workflow and report template. Reduce visual polish and dashboard charts. Do not skip disclosure of legal limitations or claim tests passed without running them.

## Windows commands (PowerShell)
```powershell
py --version
node --version
npm --version
git --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn sqlalchemy pytest httpx
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
```
If PowerShell activation is blocked, use `.\.venv\Scripts\python.exe` directly rather than changing machine-wide execution policy.

## OpenCode handoff
Open the repository in VS Code, launch OpenCode in the integrated terminal or installed extension, and select Beam Free in the model/provider picker. Paste the handoff prompt supplied with the planning pack. Do not use Codex or assume an OpenCode model ID.
