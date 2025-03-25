from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "MindExecutor Trello Proxy is running."}

@app.get("/trello.yaml")
def serve_openapi_yaml():
    return FileResponse("trello.yaml", media_type="text/yaml")
