import uvicorn
from fastapi import FastAPI

from fastapi_proj.apps import apps_router

app = FastAPI()

app.include_router(router=apps_router)


def run():
    uvicorn.run("fastapi_proj.main:app", host="127.0.0.1", port=8000, reload=True)
