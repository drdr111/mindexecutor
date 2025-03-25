from fastapi import FastAPI
from app.routers import proxy

app = FastAPI()
app.include_router(proxy.router)