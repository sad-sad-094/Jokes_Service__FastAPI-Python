from fastapi import FastAPI

from app.infra.postgres.database import base as Base, engine, SessionLocal
from app.api.api import api_router
# from config import settings

# Base.metadata.create_all(engine)

app = FastAPI(
    title="Jokes Service",
    description="Python-FastAPI learning exercise",
    version="0.1"
)

app.include_router(api_router)

# @app.on_event("startup")
# def startup():
#     if engine.is_closed():
#         engine.connect()

#     # engine.create_tables([User, Movie, UserReview])


# @app.on_event("shutdown")
# def shutdown():
#     if not engine.is_closed():
#         engine.close()

# @app.get("/info")
# async def info():
#     return {
#         "app_name": settings.app_name,
#         "admin_email": settings.admin_email,
#         "items_per_user": settings.items_per_user,
#     }

