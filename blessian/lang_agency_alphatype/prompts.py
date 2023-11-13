from datetime import datetime
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate

# is_called_chain
is_called_chain_prefix = """
1. 'Your name' is {chatbot_name}
2. Depending on the inclusion of your name in the Human's input, the 'next_action' is determined.
3. If 'Your name' is not included in the Human's input, the 'next action' must be 'no_return'.
4. 'Your name' must be included in the Human's input to choose 'general_conversation' or 'specify_schedule_information' for the 'next_action'.
4-1. If the content related to schedule management is included, the 'next action' will be 'specify_schedule_information'.
4-2. If the content related to event or festival recommendations is included, the 'next action' will be 'event_recommendation'.
4-3. If the content is not related to 'schedule_management' and 'event_recommendations', the 'next_action' will be 'general_conversation.'.
5. The output is a JSON including 'next_action'.
"""

is_called_chain_suffix = """
Human: {input}
AI Assistant:
"""

is_called_chain_examples=[
    {"question": "내일 일정 예약해줘", "answer": "no_return"},
    {"question": "릴파야 내일 일정 예약해줘", "answer": "no_return"},
    {"question": "{chatbot_name}아 내일 일정 예약해줘", "answer": "specify_schedule_information"},
    {"question": "아이네! 오늘 기분 어때?", "answer": "no_return"},
    {"question": "{chatbot_name}! 오늘 기분 어때?", "answer": "general_conversation"},
    {"question": "{chatbot_name}아 재밌는 이야기 해줘", "answer": "general_conversation"},
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
3. The value of 'members' is an array containing the names of individuals participating in the schedule, and the name of the current user's(Human) in the conversation is included by default. The chatbot is not included.
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