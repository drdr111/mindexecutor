from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import os
import httpx

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Trello Proxy is running"}

@app.get("/trello.yaml")
def serve_yaml():
    return FileResponse("trello.yaml", media_type="text/yaml")

@app.post("/proxy/trello")
async def proxy_trello(request: Request):
    data = await request.json()
    method = data.get("method", "GET").upper()
    endpoint = data.get("endpoint")
    params = data.get("params", {}) or {}
    body = data.get("data", {}) or {}

    if not endpoint:
        return JSONResponse(status_code=400, content={"error": "Missing endpoint"})

    # Добавляем авторизацию
    params["key"] = os.getenv("TRELLO_KEY")
    params["token"] = os.getenv("TRELLO_TOKEN")

    url = f"https://api.trello.com/1{endpoint}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, params=params, json=body)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return JSONResponse(
            status_code=e.response.status_code,
            content={
                "error": f"Trello API error {e.response.status_code}",
                "details": e.response.text
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Unexpected error", "details": str(e)})
