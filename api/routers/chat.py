from fastapi import APIRouter
from models.chat_request import ChatRequest
from models.chat_response import ChatResponse
from src.core.bot.chat_bot import ChatBot

router = APIRouter()
bot = ChatBot()

@router.post("/speak", response_model=ChatResponse)
async def conversate(request: ChatRequest):
    reply = bot.converse(request.user_input)
    return ChatResponse(response=reply)
