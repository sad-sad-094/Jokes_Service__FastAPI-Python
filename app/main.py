from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.debugger import initialize_fastapi_server_debugger_if_needed
from app.infra.postgres.database import init_connection, get_connection
from app.api.api import api_router


def create_application():
    initialize_fastapi_server_debugger_if_needed()
    
    app = FastAPI(
        title="Jokes Service",
        description="Python-FastAPI learning exercise",
        version="0.1"
    )

    app.include_router(api_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app = create_application()  

@app.on_event("startup")
def startup():
    db = init_connection()
    db.create_tables()


@app.on_event("shutdown")
def shutdown():
    db = get_connection()
    db.close_sessions()
