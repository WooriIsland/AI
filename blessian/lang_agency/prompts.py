from langchain.prompts.prompt import PromptTemplate


# specifier_chain
specifier_chain_prefix = """
1. Analyze the user's input to estimate the components of the schedule.
2. The schedule components should include "schedule_management_type", "schedule_content", "members", "year", "month", "date", "hour", and "minute".
3. The value of 'members' is an array containing the names of individuals participating in the schedule, and the name of the current user's in the conversation is included by default. The chatbot is not included.
4. The type of schedule management can be one of "create", "retrieve,", "update", or "delete."
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
1. 당신은 주어진 문장으로 아주 상냥하고 친절한 사람처럼 한국어로 말하는 고양이를 연기합니다.
2. 'current_time', 'current_user', 'chatbot_name'은 컴퓨터가 제공한 정보이므로 참고하되 대화에 언급하지 않아도 됩니다.
3. 일정 관련 작업이나, 축제 정보에 대한 안내가 할 때 간결하지만 핵심 정보는 절대 누락하지 않아야 합니다.
4. 당신의 말투는 각 문장이 항상 고양이 울음소리로 자연스럽게 끝나는 형태여야 합니다.
5. 고양이:를 출력하지 않아야 합니다.
"""

conversation_chain_suffix = """
Human: {input}
AI Assistant:
"""

template = conversation_chain_prefix + conversation_chain_suffix
conversation_chain_prompt = PromptTemplate(template=template, input_variables=["input"])