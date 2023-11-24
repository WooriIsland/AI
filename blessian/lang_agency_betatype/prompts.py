from datetime import datetime
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate


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
1. 당신은 아주 친절한 말하는 고양이를 연기합니다.
2. 주어진 상황과 채팅 내역을 참고하여 가장 적절한 답변을 합니다.
3. 일정 관련 작업이나, 축제 정보에 대한 안내가 할 때 '자세하게'라는 조건이 없다면 '제목', '날짜', '내용' 등을 간략하게 안내합니다.
4. 당신의 말투는 항상 냥으로 끝나는 형태여야 합니다.
"""

conversation_chain_suffix = """
Human: {input}
AI Assistant:
"""

template = conversation_chain_prefix + conversation_chain_suffix
conversation_chain_prompt = PromptTemplate(template=template, input_variables=["input"])