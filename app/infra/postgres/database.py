from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

base = declarative_base()


class Connection:
    def __init__(self):
        self.engine = create_engine(settings.sql_url)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self) -> None:
        from app.infra.postgres.models import user, joke
        base.metadata.create_all(self.engine)

    def close_sessions(self) -> None:
        print("Closing database connection...")
        self.session_local.close_all()
        print("Succcessfully closed database connection.")


db_connection: Connection = None


def init_connection() -> Connection:
    global db_connection
    print("Connecting to database...")
    db_connection = Connection()
    print("Successfully connected to database.")
    return db_connection


def get_connection() -> Connection:
    return db_connection


def get_db():
    db = db_connection.session_local()
    try:
        yield db
    finally:
        db.close()