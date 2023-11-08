import os
from pathlib import Path

import dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain

from lang_agency_prototype import prompt

# OpenAI API Key from dotenv
dotenv_file = dotenv.find_dotenv(str(Path("./").absolute().joinpath(".env")))
dotenv.load_dotenv(dotenv_file)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Prompt
prompt.suffix
prompt.system_prompt

# LLM
model = ChatOpenAI(model="gpt-3.5-turbo-1106", openai_api_key=OPENAI_API_KEY)

# Memory
memory = ConversationBufferWindowMemory(ai_prefix="AI Assistant")

# Chain
llm_chain = LLMChain(
    prompt=prompt.prompt,
    llm=model,
    verbose=True,
    memory=ConversationBufferWindowMemory(ai_prefix="AI Assistant", k=10)
)