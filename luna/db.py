from __future__ import annotations

import os
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine

DB_URL = os.getenv("LUNA_DB_URL", "postgresql://localhost/luna")


class Target(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    domain: str


class Finding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    target_id: Optional[int] = Field(default=None, foreign_key="target.id")
    severity: str
    description: str


def init_db(db_url: str = DB_URL) -> None:
    engine = create_engine(db_url)
    SQLModel.metadata.create_all(engine)
