import os
from sqlalchemy import create_engine

engine = create_engine(
    os.getenv(
        "DATABASE_URL",
        "postgresql://pkg:pkg@localhost:5432/project_knowledge",
    )
)
