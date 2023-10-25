import time

from fastapi import APIRouter
from domain.chatbot.reqeust_schema import ChatbotSchema

router = APIRouter(
    prefix="/api/chatbot",
)

@router.get("/hello", tags=["hello"])
async def hello():
    return {"content": "Hello World!"}

@router.post("/conversation", tags=["conversation"])
async def chat(chatbot_schema: ChatbotSchema):
    content = "채봇이 궁시렁궁시렁 말을 했다!"
    task = "schedule_register"
    data = "Very important data"
    print(chatbot_schema.content)
    
    # 별도로 status(bool)
    if "까망" in chatbot_schema.content:
        content = "까망이가 궁시렁궁시렁 말을 했다!"
        time.sleep(10)
    
    return {
        "island_id": chatbot_schema.island_id, 
        "content": content,
        "task": task,
        "data": {
            "year": 2023, 
            "month": 10, 
            "date": 24, 
            "hour": 20, 
            "minute": 00, 
            "content": "저녁식사 예약"
        }
    }