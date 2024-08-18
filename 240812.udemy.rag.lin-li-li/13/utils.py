from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

import os
from langchain.memory import ConversationBufferMemory


def get_chat_response(prompt, memory, openai_api_key):
    model = ChatOpenAI(model="gpt-4o-mini-2024-07-18", openai_api_key=openai_api_key)
    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input": prompt})
    return response["response"]


# memory = ConversationBufferMemory(return_messages=True)
# print(get_chat_response("牛顿提出过哪些知名的定律？", memory, os.getenv("OPENAI_API_KEY")))
# print(get_chat_response("我上一个问题是什么？", memory, os.getenv("OPENAI_API_KEY")))









from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

import os
from langchain.memory import ChatMessageHistory

global_store = {}
def get_session_history(session_id):  
    if session_id not in global_store:
        global_store[session_id] = ChatMessageHistory(return_messages=True)
    return global_store[session_id]

def get_chat_response(input, openai_api_key):
    prompt = ChatPromptTemplate.from_messages([MessagesPlaceholder(variable_name='history'), ('human', '{input}')])
    llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", openai_api_key=openai_api_key)


    chat_with_memory = RunnableWithMessageHistory(prompt | llm, get_session_history, input_messages_key='input', history_messages_key='history')
    response = chat_with_memory.invoke({'input': input}, config={'configurable': {'session_id': 'abc123'}}) 

    return response["response"]


# print(get_chat_response("牛顿提出过哪些知名的定律？", os.getenv("OPENAI_API_KEY")))
# print(get_chat_response("我上一个问题是什么？", os.getenv("OPENAI_API_KEY")))
