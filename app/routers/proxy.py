from fastapi import APIRouter, Request
import os
import requests

router = APIRouter()

@router.post("/proxy")
async def proxy(request: Request):
    data = await request.json()

    service = data.get("service", "trello")
    method = data.get("method", "GET").upper()
    endpoint = data.get("url")
    params = data.get("params", {})
    body = data.get("body", {})

    if service == "trello":
        base_url = "https://api.trello.com/1"
        params["key"] = os.getenv("TRELLO_KEY")
        params["token"] = os.getenv("TRELLO_TOKEN")
    elif service == "notion":
        base_url = "https://api.notion.com/v1"
    elif service == "gdrive":
        base_url = "https://www.googleapis.com/drive/v3"
    else:
        return {"error": "Unknown service"}

    headers = {}
    if service == "notion":
        headers["Authorization"] = f"Bearer {os.getenv('NOTION_TOKEN')}"
        headers["Notion-Version"] = "2022-06-28"
    elif service == "gdrive":
        headers["Authorization"] = f"Bearer {os.getenv('GDRIVE_TOKEN')}"

    url = f"{base_url}{endpoint}"
    response = requests.request(
        method=method,
        url=url,
        params=params if method in ["GET", "DELETE"] else None,
        json=body if method in ["POST", "PUT", "PATCH"] else None,
        headers=headers
    )
    return response.json()