from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routers import incidents, playbook, tabletop, actions, assessment

app = FastAPI(title="NDPA Incident Response Toolkit", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(incidents.router)
app.include_router(playbook.router)
app.include_router(tabletop.router)
app.include_router(actions.router)
app.include_router(assessment.router)