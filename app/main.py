from fastapi import FastAPI

from app.infra.postgres.database import init_connection, get_connection
from app.api.api import api_router


app = FastAPI(
    title="Jokes Service",
    description="Python-FastAPI learning exercise",
    version="0.1"
)


app.include_router(api_router)
  

@app.on_event("startup")
def startup():
    db = init_connection()
    db.create_tables()


@app.on_event("shutdown")
def shutdown():
    db = get_connection()
    db.close_sessions()
