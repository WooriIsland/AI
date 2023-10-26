from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class ChatbotSchema(BaseModel):
    island_id: str = "island1221"
    user_id: str = "user1221"
    content: str
    datetime: Optional[str] = str(datetime.now())