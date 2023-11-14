from datetime import datetime
import time
import json

from fastapi import APIRouter

from domain.chatbot.reqeust_schema import ChatbotSchema
from lang_agency_prototype import chatbots
from lang_agency_alphatype import chatbot

router = APIRouter(
    prefix="/api/chatbot",
)

@router.get("/hello", tags=["hello"])
async def hello():
    return {"content": "Hello World!"}

@router.post("/test_conversation", tags=["conversation"])
async def test_chat(chatbot_schema: ChatbotSchema):
    content = "챗봇이 궁시렁궁시렁 말을 했다!"
    task = "schedule_register"
    data = "Very important data"
    print(chatbot_schema.content)
    
    # 별도로 status(bool)
    if "까망" in chatbot_schema.content:
        content = "까망이가 궁시렁궁시렁 말을 했다!"
        time.sleep(10)
    
    return {
        "island_id": chatbot_schema.island_id, 
        "answer": content,
        "task": task,
        "data": {
            "year": 2023, 
            "month": 10, 
            "date": 24, 
            "hour": 20, 
            "minute": 0, 
            "content": "저녁식사 예약"
        }
    }
    
@router.post("/prototype_conversation", tags=["conversation"])
async def chat(chatbot_schema: ChatbotSchema):
    answer = chatbots.llm_chain.predict(input=chatbot_schema.content)
    print("#"*3+answer)
    answer = json.loads(answer)
    answer["island_id"] = chatbot_schema.island_id
    return answer

@router.post("/conversation", tags=["conversation"])
async def chat(chatbot_schema: ChatbotSchema):
    day_of_the_week = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    current_time = f" current_time: {datetime.now()} {day_of_the_week[datetime.now().weekday()]}"
    chatbot_name = "까망"
    
    answer = None
    while True:
        try:
            answer = chatbot.agent_chain.run(
                input=chatbot_schema.content \
                + current_time \
                + f" current_user: {chatbot_schema.user_id}" \
                + f" chatbot_name: {chatbot_name}"
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    print("#"*10 + answer + "#"*10)
    final_response = {
        "island_id": chatbot_schema.island_id,
        "answer": answer, 
        "task": "", 
        "data": {
            "year": None, 
            "month": None, 
            "date": None, 
            "hour": None, 
            "minute": None, 
            "content": None,
        }
    }
    if "No Response" in answer:
        final_response["answer"] = ""
        final_response["task"] = "대기"
    return final_response