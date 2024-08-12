from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings
from app.logging import get_logging

log = get_logging(__name__)

base = declarative_base()


class Connection:
    def __init__(self):
        self.engine = create_engine(settings.sql_url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self) -> None:
        from app.infra.postgres.models import user, joke
        base.metadata.create_all(self.engine)

    def close_sessions(self) -> None:
        log.info("Closing database connection...")
        self.session_local.close_all()
        log.info("Succcessfully closed database connection.")


db_connection: Connection = None


def init_connection() -> Connection:
    global db_connection
    log.info("Connecting to database...")
    db_connection = Connection()
    log.info("Successfully connected to database.")
    return db_connection


def get_connection() -> Connection:
    return db_connection


def get_db():
    db = db_connection.session_local()
    try:
        yield db
    finally:
        db.close()