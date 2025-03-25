from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/trello.yaml", response_class=FileResponse)
async def get_openapi_yaml():
    return FileResponse("trello.yaml", media_type="application/yaml")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

