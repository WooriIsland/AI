from datetime import datetime
from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool
from langchain.tools.base import ToolException
from pydantic import BaseModel, Field


class ScheduleSchema(BaseModel):
    island_id: str = Field(description="고유한 ID입니다.")
    content: str = Field(description="일정의 내용입니다.")
    year: int = Field(description="MINYEAR <= year <= MAXYEAR")
    month: int = Field(description="1 <= month <= 12")
    day: int = Field(description="1 <= day <= 주어진 month와 year에서의 날의 수입니다.")
    hour: int = Field(description="0 <= hour < 24")
    minute: int = Field(description="0 <= minute < 60")


class ScheduleRegister(BaseTool):
    name = "일정 등록"
    description = "일정을 등록해야 할 때 유용합니다."
    args_schema: Type[ScheduleSchema] = ScheduleSchema
    handle_tool_error = ToolException("일정 등록에 실패했습니다.")
    
    today = datetime.now()

    def _run(
        self,
        island_id: str,
        content: str,
        year: int = today.year,
        month: int = today.month,
        date: int = today.date,
        hour: int = today.hour,
        minute: int = today.minute,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return """"""


class ScheduleRetriever(BaseTool):
    name = "일정 조회"
    description = "일정을 조회해야 할 때 유용합니다."
    args_schema: Type[ScheduleSchema] = ScheduleSchema
    handle_tool_error = ToolException("일정 조회에 실패했습니다.")
    
    today = datetime.now()

    def _run(
        self,
        island_id: str,
        content: str,
        year: int = today.year,
        month: int = today.month,
        date: int = today.date,
        hour: int = today.hour,
        minute: int = today.minute,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return """"""


class ScheduleModifier(BaseTool):
    name = "일정 수정"
    description = "일정을 수정해야 할 때 유용합니다."
    args_schema: Type[ScheduleSchema] = ScheduleSchema
    handle_tool_error = ToolException("일정 수정에 실패했습니다.")
    
    today = datetime.now()

    def _run(
        self,
        island_id: str,
        content: str,
        year: int = today.year,
        month: int = today.month,
        date: int = today.date,
        hour: int = today.hour,
        minute: int = today.minute,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return """"""
    
    
class ScheduleDeleter(BaseTool):
    name = "일정 삭제"
    description = "일정을 삭제해야 할 때 유용합니다."
    args_schema: Type[ScheduleSchema] = ScheduleSchema
    handle_tool_error = ToolException("일정 삭제에 실패했습니다.")
    
    today = datetime.now()

    def _run(
        self,
        island_id: str,
        content: str,
        year: int = today.year,
        month: int = today.month,
        date: int = today.date,
        hour: int = today.hour,
        minute: int = today.minute,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return """"""