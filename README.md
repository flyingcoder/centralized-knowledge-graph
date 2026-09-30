# Centralized Knowledge Graph

Local-first knowledge graph and provenance service for multiple Git repositories.

## MVP
- PostgreSQL + pgvector for metadata, chunks, provenance, embeddings
- FastAPI knowledge API
- MCP adapter
- Git synchronization worker
- Configuration-driven repository registry
- Local filesystem artifacts

## Quick start
1. Copy .env.example to .env.
2. Run docker compose up -d postgres.
3. Install Python dependencies with pip install -e .
4. Apply migrations.
5. Start the API with uvicorn apps.api.main:app --reload.

See config/project.yaml for the ecosystem definition.
