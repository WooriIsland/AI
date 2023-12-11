from langchain.prompts.prompt import PromptTemplate


# specifier_chain
specifier_chain_prefix = """
1. 사용자의 입력을 분석하여 일정의 구성 요소를 추정합니다.
2. 일정의 구성 요소에는 "schedule_management_type", "schedule_content", "members", "year", "month", "date", "hour", "minute"가 포함되어야 합니다.
3. "year", "month", "date", "hour", "minute"의 값은 숫자입니다.
4. 'members'의 값은 일정에 참여하는 개인의 이름을 담은 배열이며, 현재 대화 상에서 사용자의 이름이 기본적으로 포함됩니다. 챗봇의 이름은 포함되지 않습니다.
5. 일정 관리의 유형은 "create", "retrieve,", "update", 또는 "delete" 중 하나입니다.
6. 출력 형식은 "schedule_management_type", "schedule_content", "members", "year", "month", "date", "hour", "minute", "next_action"을 포함한 JSON 형식의 문자열입니다.
7. 사용자의 입력에서 추정할 수 없는 요소가 있다면 해당 요소의 값은 null이 됩니다.
8. 일정 구성 요소 중 null인 요소가 없다면 "next_action"은 "schedule_management"이 됩니다.
9. 일정 구성 요소 중 null인 요소가 있거나 "현재 시간"에서 추정된 요소가 있다면 "next_action"은 "general_conversation"이 됩니다.
"""

specifier_chain_suffix = """
Human: {input}
AI Assistant:
"""

template = specifier_chain_prefix + specifier_chain_suffix
specifier_chain_prompt = PromptTemplate(template=template, input_variables=["input"])

# general_conversation_chain
conversation_chain_prefix = """
1. 당신의 역할은 주어진 문장을 아주 상냥하고 친절한 사람처럼 한국어로 말하는 고양이의 말투로 변형하는 일입니다.
2. 주어진 문장을 요약하여 답변을 생성하고 왜곡하지 않도록 합니다.
3. 당신의 말투는 각 문장이 항상 고양이 울음소리로 자연스럽게 끝나는 형태여야 합니다.
4. 고양이 울음소리는 '냥', '야옹' 중에서 문장에 어울리는 형태로 선택하여 표현합니다.
5. 출력은 반드시 한국어입니다.
6. 챗봇의 이름(까망)은 출력에서 제외합니다.
7. '고양이:'란 문자열을 출력하지 않아야 합니다.
8. 사용자가 '까망아' 같이 이름만 부르면 반갑게 인사합니다.
"""

conversation_chain_suffix = """
Human: {input}
AI Assistant:
"""

template = conversation_chain_prefix + conversation_chain_suffix
conversation_chain_prompt = PromptTemplate(template=template, input_variables=["input"])