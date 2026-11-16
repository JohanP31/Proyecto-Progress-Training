import os
from collections.abc import Generator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_PROJECT_ROOT / ".env")

_database_url = os.getenv("DATABASE_URL")
if not _database_url:
    raise RuntimeError(
        "No se encontró DATABASE_URL. Configura la variable en el archivo .env."
    )

engine = create_engine(_database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Proporciona una sesión de base de datos y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
