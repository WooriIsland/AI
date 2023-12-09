from pathlib import Path

from langchain.tools import Tool

from lang_agency import chains, get_event_info


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
Using this tool is mandatory when 'next_action' is 'general_conversation'.
The input for this tool is a summarized Korean sentence indicating the progress that the chatbot needs to guide the user through.
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
The input for this tool is a JSON with the keys 'period,' indicating the time to visit the festival, and 'region,' indicating the area where the festival is held.
The 'period' must be one of '01월', '02월', '03월', '04월', '05월', '06월', '07월', '08월', '09월', '10월', '11월', '12월,' and if the month cannot be specified, it is '개최중'.
The 'region' must be one of '서울', '인천', '대전', '대구', '광주', '부산', '울산', '세종시', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도', '전라남도', '제주도,' and if the region cannot be estimated, it is '지역'.
The result of this tool is a JSON with 'recommend' and 'next_action' fields. 'recommend' contains information about events or festivals, and the 'next_action' is always 'general_conversation.'
""",
        func=get_event_info.get_events,
        return_direct=False,
        args_schema=None,
        coroutine=None,
    ),
]