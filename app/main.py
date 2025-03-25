from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

import os
import httpx
from fastapi import Request

@app.post("/proxy/trello")
async def proxy_trello(request: Request):
    data = await request.json()

    method = data.get("method", "GET").upper()
    endpoint = data.get("endpoint")
    params = data.get("params", {}) or {}
    body = data.get("data", {}) or {}

    if not endpoint:
        return {"error": "Missing endpoint"}

    # 🔐 Добавляем ключ и токен из Railway переменных окружения
    params["key"] = os.getenv("TRELLO_KEY")
    params["token"] = os.getenv("TRELLO_TOKEN")

    # 🔗 Финальный URL запроса к Trello
    url = f"https://api.trello.com/1{endpoint}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, params=params, json=body)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"Trello API error {e.response.status_code}",
                "details": e.response.text
            }
        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}

