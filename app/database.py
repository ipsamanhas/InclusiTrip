from __future__ import annotations

from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'inclusitrip.db'}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def migrate_sqlite_users_table(engine_: object) -> None:
    """Add new SQLite columns when the DB file existed before migrations."""
    if "sqlite" not in str(engine_.url):
        return
    from sqlalchemy import inspect, text

    columns = [c["name"] for c in inspect(engine_).get_columns("users")]
    with engine_.begin() as conn:
        if "phone" not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR(64)"))
        if "photo_url" not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN photo_url TEXT"))


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
