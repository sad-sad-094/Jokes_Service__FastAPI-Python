from fastapi import APIRouter

from app.api.routes import users, jokes


api_router = APIRouter()


api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(jokes.router, prefix="/jokes", tags=["jokes"])