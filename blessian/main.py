from fastapi import FastAPI

from domain.chatbot import chatbot_router

description = """
사이좋은 가족을 위한 메타버스 라이프로깅 👨‍👩‍👧‍👦

## Chatbot

기능 목록:

* **Say Hello** (_completely implemented_).
* **Conversation with Chatbot** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "hello",
        "description": "기본적인 연결 테스트를 위한 \"Hello, World!\" API입니다.",
    },
    {
        "name": "conversation",
        "description": "챗봇에게 대화를 전달합니다. 이름을 통해 호출하면 대답하거나 고유 기능을 실행하고 대답을 돌려줍니다.",
        "externalDocs": {
            "description": "그냥 링크",
            "url": "https://url.kr/m17zfu",
        },
    },
]

app = FastAPI(
    title="우리 가족 섬",
    description=description,
    version="0.0.1",
    contact={
        "name": "Blessian",
        "url": "https://github.com/Blessian",
        "email": "blessian.dev@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

app.include_router(chatbot_router.router)