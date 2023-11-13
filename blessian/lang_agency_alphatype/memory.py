from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import MessagesPlaceholder


chat_history = MessagesPlaceholder(variable_name="chat_history")
memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=5)
agent_kwargs={
    "memory_prompts": [chat_history],
    "input_variables": ["input", "agent_scratchpad", "chat_history"]
}