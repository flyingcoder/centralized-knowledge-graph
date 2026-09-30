from fastapi import FastAPI
from sqlalchemy import text
from .db import engine

app = FastAPI(title="Centralized Knowledge Graph API", version="0.1.0")

@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}

@app.get("/repositories")
def repositories():
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT name, branch, indexed_commit, sync_status "
            "FROM repositories ORDER BY name"
        )).mappings().all()
    return list(rows)
