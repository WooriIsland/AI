from typing import Optional
from datetime import datetime

from fastapi import APIRouter
from domain.chatbot.request_schema import ChatbotSchema

router = APIRouter(
    prefix="/api/chatbot",
)

@router.get("/hello", tags=["hello"])
async def hello():
    return {"content": "Hello World!"}

@router.post("/conversation", tags=["conversation"])
async def chat(chatbot_schema: ChatbotSchema):
    content = "success"
    task = "schedule_register"
    data = "Very important data"
    return {
        "island_id": chatbot_schema.island_id, 
        "content": content, 
        "data": {
            "task": task,
            "data": data
        }
    }