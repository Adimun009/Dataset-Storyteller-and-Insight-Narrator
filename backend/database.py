import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "dataset_storyteller")

DEFAULT_DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=int(POSTGRES_PORT),
    database=POSTGRES_DB,
)

FALLBACK_SQLITE_URL = URL.create(
    "sqlite",
    database=str(BASE_DIR / "dataset_storyteller.db"),
)


def resolve_database_url():
    configured_url = os.getenv("DATABASE_URL")
    if configured_url:
        return configured_url

    use_sqlite = os.getenv("USE_SQLITE", "true").lower() in {"1", "true", "yes", "on"}
    if use_sqlite:
        return FALLBACK_SQLITE_URL

    return DEFAULT_DATABASE_URL


def build_engine(db_url: str):
    if str(db_url).startswith("sqlite"):
        return create_engine(
            db_url,
            connect_args={"check_same_thread": False},
        )

    return create_engine(db_url, pool_pre_ping=True)


DATABASE_URL = resolve_database_url()
engine = build_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()