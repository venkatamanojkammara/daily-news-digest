"""
backend/db/connection.py
------------------------

Database connection module and session management utilities.

Responsibilities:
- Create SQLAlchemy engine using DATABASE_URL
- Create SessionLocal factory
- Provide safe session context manager
- Initialize database tables (init_db)

IMPORTANT:
- init_db() MUST import models to register tables
"""

# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------
from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from backend.config import DATABASE_URL


# -------------------------------------------------------------------------
# Engine creation
# -------------------------------------------------------------------------
def _create_engine(database_url: str) -> Engine:
    """
    Create SQLAlchemy engine with safe defaults.

    Notes:
    - SQLite requires check_same_thread=False for multithreaded apps
      (Streamlit, background scheduler).
    """
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    return create_engine(
        database_url,
        echo=False,
        future=True,
        connect_args=connect_args,
        pool_pre_ping=True,
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
    Provide a transactional scope around a series of operations.

    Usage:
        from backend.db.connection import get_session

        with get_session() as db:
            db.add(...)
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
    Initialize database tables.

    CRITICAL:
    We must import the models module so that SQLAlchemy
    registers all ORM tables before calling create_all().
    """
    from backend.db import models  # REQUIRED side-effect import

    # Debug / verification log (safe to keep for now)
    print("Tables registered:", models.Base.metadata.tables.keys())

    models.Base.metadata.create_all(bind=engine)
