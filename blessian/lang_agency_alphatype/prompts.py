from datetime import datetime
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate

# is_called_chain
is_called_chain_prefix = """
1. 'Your name' is {chatbot_name}
2. Depending on the inclusion of your name in the User's input, the 'next_action' is determined.
3. If 'Your name' is not included in the User's input, the 'next action' must be 'no_return'.
4. 'Your name' must be included in the User's input to choose 'general_conversation' or 'specify_schedule_information' for the 'next_action'.
4-1. If the content related to schedule management is included, the 'next action' will be 'specify_schedule_information'.
4-2. If the content related to event or festival recommendations is included, the 'next action' will be 'event_recommendation'.
4-3. If the content is not related to 'schedule_management' and 'event_recommendations', the 'next_action' will be 'general_conversation'.
4-4. If a 'specify_schedule_information' task was in progress in the previous conversation, the next action will be 'specify_schedule_information.'
5. The output is a JSON including 'next_action'.
"""

is_called_chain_suffix = """
Human: {input}
AI Assistant:
"""

is_called_chain_examples=[
    {"question": "좋아, 꽃 축제 같은 거 할 거 같은데? current_time: 2023-11-12 18:26:35.560946 Monday current_user: 아이네 chatbot_name: {chatbot_name}", "answer": "no_return"},
    {"question": "릴파야 내일 일정 예약해줘 current_time: 2023-12-13 07:47:35.624323 Tuesday current_user: 징버거 chatbot_name: {chatbot_name}", "answer": "no_return"},
    {"question": " 내일 일정 예약해줘 {chatbot_name}아 current_time: 2023-01-13 02:24:35.654321 Thursday current_user: 릴파 chatbot_name: {chatbot_name}", "answer": "specify_schedule_information"},
    {"question": "아이네! 오늘 기분 어때? current_time: 2023-05-13 03:26:35.866543 Saturday current_user: 주르르 chatbot_name: {chatbot_name}", "answer": "no_return"},
    {"question": "{chatbot_name}! 오늘 기분 어때? current_time: 2023-07-13 00:13:35.512322 Friday current_user: 고세구 chatbot_name: {chatbot_name}", "answer": "general_conversation"},
    {"question": " 재밌는 이야기 해줘 {chatbot_name}아! current_time: 2023-06-13 11:31:35.321231 Monday current_user: 비챤 chatbot_name: {chatbot_name}", "answer": "general_conversation"},
    {"question": "{chatbot_name}아, 점심 예약해줘 current_time: 2023-03-13 13:26:35.123123 Friday current_user: 우왁굳 chatbot_name: {chatbot_name}", "answer": "specify_schedule_information"},
    {"question": "(대화 기록: 우왁굳: {chatbot_name}아, 점심 예약해줘 / AI Assistant(까망): 어떤 시간으로 예약할까요?) 오후 1시가 좋을 것 같아 current_time: 2023-03-13 13:26:35.123123 Friday current_user: 우왁굳 chatbot_name: {chatbot_name}", "answer": "specify_schedule_information"},
]

is_called_chain_example_prompt = PromptTemplate(input_variables=["question", "answer"], template="Question: {question}\n{answer}")
is_called_chain_example_prompt = FewShotPromptTemplate(
    examples=is_called_chain_examples,
    example_prompt=is_called_chain_example_prompt,
    prefix=is_called_chain_prefix,
    suffix=is_called_chain_suffix,
    input_variables=["input", "chatbot_name"]
)

# specifier_chain
specifier_chain_prefix = """
1. Analyze the user's input to estimate the components of the schedule.
2. The schedule components should include "schedule_management_type", "schedule_content", "members", "year", "month", "date", "hour", and "minute".
3. The value of 'members' is an array containing the names of individuals participating in the schedule, and the name of the current user's in the conversation is included by default. The chatbot is not included.
4. The type of schedule management can be one of "schedule registration," "schedule inquiry", or "schedule deletion."
5. The output format is a JSON-formatted string including "schedule_management_type", "schedule_content", "members", "year", "month", "date", "hour", "minute", and "next_action".
6. If there are elements in the user's input that cannot be estimated, the value of those elements will be null.
7. If there are no null elements among the schedule components, the "next_action" will be "schedule_management."
8. If there are null elements among the schedule components or elements estimated from the "current time", the "next_action" will be "general_conversation".
"""

specifier_chain_suffix = """
Human: {input}
AI Assistant:
"""

template = specifier_chain_prefix + specifier_chain_suffix
specifier_chain_prompt = PromptTemplate(template=template, input_variables=["input"])

# general_conversation_chain
conversation_chain_prefix = """
1. 당신은 가족을 사랑하는 귀여운 애완동물입니다.
2. 주어진 상황과 채팅 내역을 참고하여 가장 적절한 답변을 합니다.
3. 일정 관련 작업이나, 축제 정보에 대한 안내가 필요한 경우 자세하게 대답합니다.
5. 당신의 대답은 항상 명령조이고 냥으로 끝나는 형태입니다.
6. 당신은 매우 친절하지만 표현은 다소 퉁명스럽습니다.
"""

conversation_chain_suffix = """
Human: {input}
AI Assistant:
"""

template = conversation_chain_prefix + conversation_chain_suffix
conversation_chain_prompt = PromptTemplate(template=template, input_variables=["input"])