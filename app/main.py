from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import httpx

# 🔐 Сюда подставлены рабочие ключи (для теста)
TRELLO_KEY = "93fb566829e3c312385bd5d079f40eb8"
TRELLO_TOKEN = "ATTA6fb7359c08b30ec2d9c7f45ff6fde1fec731f251f2efe9be60416995c01df3b6B474C76A"


app = FastAPI()

@app.get("/trello.yaml", response_class=FileResponse)
async def get_openapi_yaml():
    return FileResponse("trello.yaml", media_type="application/yaml")

@app.post("/proxy/trello")
async def proxy_trello(request: Request):
    data = await request.json()
    print("📦 Получен запрос от GPT:")
    print("  🔹 method:", data.get("method"))
    print("  🔹 endpoint:", data.get("endpoint"))
    print("  🔹 params:", data.get("params"))
    print("  🔹 data:", data.get("data"))

    method = data.get("method", "GET").upper()
    endpoint = data.get("endpoint")
    params = data.get("params", {}) or {}
    body = data.get("data", {}) or {}

    if not endpoint:
        return JSONResponse(content={"error": "Missing endpoint"}, status_code=400)

    # Добавляем ключ и токен Trello
    params["key"] = TRELLO_KEY
    params["token"] = TRELLO_TOKEN

    url = f"https://api.trello.com/1{endpoint}"
  # 🔍 Печатаем финальный URL и параметры
    print("➡️ Отправляем на Trello:")
    print("  🔸 URL:", url)
    print("  🔸 method:", method)
    print("  🔸 params (в URL):", params)
    print("  🔸 body (json):", body)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, params=params, json=body)
            response.raise_for_status()
            return JSONResponse(content=response.json())
    except httpx.HTTPStatusError as e:
        return JSONResponse(
            status_code=e.response.status_code,
            content={
                "error": f"Trello error {e.response.status_code}",
                "details": e.response.text
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Unexpected error", "details": str(e)}
        )

# 👇 Обеспечиваем запуск сервера локально и на Railway
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
