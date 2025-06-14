from fastapi import FastAPI
from src.api.routers import chat

app = FastAPI(title="Product ChatBot API")

@app.get("/")
async def root():
    return {"message": "Welcome to the Product ChatBot API Made by hselimtuna"}

app.include_router(chat.router, prefix="")