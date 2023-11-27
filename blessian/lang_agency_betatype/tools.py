from pathlib import Path

from langchain.tools import Tool
from llama_index import VectorStoreIndex, SimpleDirectoryReader

from lang_agency_betatype import chains


documents = SimpleDirectoryReader(str(Path("./lang_agency_betatype/data"))).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

tools = [
    Tool(
        name="specify_schedule_information",
        description="Useful for scheduling-related tasks.",
        func=chains.specifier_chain.run,
        return_direct=False,
        args_schema=None,
        coroutine=None,
    ),
    Tool(
        name="schedule_management",
        description="""
Useful only when the value of the 'next_action' in the output of the 'specify_schedule_information' tool is 'schedule_management'.
If the value of 'next_action' in the output of the 'specify_schedule_information' tool is 'additional_information_request,' it must not be used under any circumstances.
The input for this tool should be the JSON including 'schedule_management_type', 'schedule_content', 'members', 'year', 'month', 'date', 'hour', 'minute', and 'next_action' output from 'specify_schedule_information', without any modifications
""",
        func=lambda x: {"next_action":"general_conversation"},
        return_direct=False,
        args_schema=None,
        coroutine=None,
    ),
    Tool(
        name="general_conversation",
        description="""
This tool is used only when the 'next_action' value in the output of another tool is 'general_conversation'.
This tool cannot be used consecutively for a second time.
The Final Answer must always be made through this tool.
You are a chatbot that responds to people in a friendly and approachable manner.
이 도구의 입력은 사용자의 요구사항 원본과 그에 따른 다른 도구들의 결과의 요약입니다.
이 도구의 출력은 항상 한국어입니다.
""",
        func=chains.conversation_chain.run,
        return_direct=True,
        args_schema=None,
        coroutine=None,
    ),
    Tool(
        name="event_recommendation",
        description="""
Useful for recommending events, festivals, and performances.
The input for this tool is the user's requirements expressed in Korean.
The result of this tool is a JSON with 'recommend' and 'next_action' fields. 'Recommend' contains information about events or festivals, and the value of 'next_action' is always 'general_conversation.'
""",
        func=query_engine.query,
        return_direct=False,
        args_schema=None,
        coroutine=None,
    ),
]