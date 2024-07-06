from fastapi import FastAPI
from core.config import settings


def start_application():
    return FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    
app = start_application()

@app.get("/")
def hello():
    return {"msg":"Hello FASTAPI"}