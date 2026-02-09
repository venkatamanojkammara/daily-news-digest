"""
backend/db/connection.py
------------------------

Database connection and session management.

Designed to work correctly with:
- Streamlit Cloud
- Supabase (PostgreSQL + PgBouncer)
- Local SQLite (development)
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from backend.config import DATABASE_URL


# -------------------------------------------------------------------------
# Engine creation
# -------------------------------------------------------------------------
def _create_engine(database_url: str) -> Engine:
    """
    Create SQLAlchemy engine with safe defaults.

    IMPORTANT:
    - SQLite: allow multithreading
    - Supabase/Postgres on Streamlit Cloud: MUST use NullPool
    """
    connect_args = {}

    if database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

        return create_engine(
            database_url,
            echo=False,
            future=True,
            connect_args=connect_args,
        )

    # PostgreSQL / Supabase
    return create_engine(
        database_url,
        echo=False,
        future=True,
        poolclass=NullPool,   # 🚨 REQUIRED
    )


engine: Engine = _create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


# -------------------------------------------------------------------------
# Session management
# -------------------------------------------------------------------------
@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Provide a transactional database session.
    """
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# -------------------------------------------------------------------------
# Database initialization
# -------------------------------------------------------------------------
def init_db() -> None:
    """
    Create tables if they do not exist.
    """
    from backend.db import models  # required side-effect import

    print("Tables registered:", models.Base.metadata.tables.keys())
    models.Base.metadata.create_all(bind=engine)
