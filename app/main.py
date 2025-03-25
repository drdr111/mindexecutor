from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/trello.yaml", response_class=FileResponse)
async def get_openapi_yaml():
    return FileResponse("trello.yaml", media_type="application/yaml")

