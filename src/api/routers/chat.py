from fastapi import APIRouter, HTTPException
from src.logger.custom_logger import SingletonLogger
from api.models.chat_response import ChatResponse
from api.models.chat_request import ChatRequest
from src.core.bot.chat_bot import ChatBot

router = APIRouter()
logger = SingletonLogger()
bot = ChatBot()


@router.post("/speak", response_model=ChatResponse)
async def conversate(request: ChatRequest):
    endpoint = "/speak"
    method = "POST"

    try:
        reply = bot.converse(request.user_input)

        logger.log_api_event(
            endpoint=endpoint,
            method=method,
            status_code=200,
            request_payload=request.model_dump(),
            response_payload={"response": reply}
        )

        return ChatResponse(response=reply)

    except Exception as e:
        logger.log_api_event(
            endpoint=endpoint,
            method=method,
            status_code=500,
            request_payload=request.model_dump(),
            response_payload={"error": str(e)}
        )
        raise HTTPException(status_code=500, detail="Internal server error")
