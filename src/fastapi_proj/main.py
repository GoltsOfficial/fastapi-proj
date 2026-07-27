import uvicorn
from fastapi import FastAPI

from fastapi_proj.apps import apps_router

app = FastAPI()

app.include_router(router=apps_router)


def run():
    uvicorn.run(app="fastapi_proj.main:app", reload=True)
