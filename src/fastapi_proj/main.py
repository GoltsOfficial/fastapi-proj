import uvicorn
from fastapi import FastAPI

app = FastAPI()


def run():
    uvicorn.run(
        "fastapi_proj.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )