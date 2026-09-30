CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE repositories (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  url TEXT NOT NULL,
  branch TEXT NOT NULL DEFAULT 'main',
  indexed_commit TEXT,
  sync_status TEXT NOT NULL DEFAULT 'pending',
  last_reconciled_at TIMESTAMPTZ
);

CREATE TABLE provenance (
  id BIGSERIAL PRIMARY KEY,
  repository_id BIGINT NOT NULL REFERENCES repositories(id),
  path TEXT NOT NULL,
  commit_sha TEXT NOT NULL,
  line_start INTEGER,
  line_end INTEGER,
  content_hash TEXT,
  extracted_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE knowledge_chunks (
  id BIGSERIAL PRIMARY KEY,
  provenance_id BIGINT NOT NULL REFERENCES provenance(id),
  content TEXT NOT NULL,
  embedding vector(1536),
  status TEXT NOT NULL DEFAULT 'current'
);

CREATE INDEX idx_provenance_repo_path ON provenance(repository_id, path);
CREATE INDEX idx_knowledge_status ON knowledge_chunks(status);
