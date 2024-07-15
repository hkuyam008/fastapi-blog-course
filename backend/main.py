from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import settings
from apis.base import api_router
from apps.base import apps_router


def include_router(app: FastAPI) -> None:
    app.include_router(api_router)
    app.include_router(apps_router)


def configure_staticfiles(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    
def start_application():
    app =  FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_staticfiles(app)
    return app


app = start_application()