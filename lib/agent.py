# agent.py
from lib.llm import useOllama
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnableMap,
    RunnablePassthrough,
)

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def agent_node(
    model="llama3.1:latest",
    config={},
    memory=None,
    system_message=(
        "Your name is Thoth."
    ),
    temperature=0.5,
    tools=None,
    file=None
):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message +
             "You have access to the following tools: {tool_names}.  I will avoid generateing fictional references. if tool_calling doesn't provide an answer I will try to find it on the web."),
            MessagesPlaceholder("memory"),
            ("human", "{content}"),
            
        ]
    )

    prompt = prompt.partial(tool_names=", ".join(
        [tool.name for tool in tools]))

    ollama = useOllama(model=model, temperature=temperature)
    if tools:
        ollama = ollama.bind_tools(tools)

    
    chain = prompt | ollama | StrOutputParser() 
    if memory:
        chain = RunnableWithMessageHistory(
            chain,
            lambda session_id: memory,
            input_messages_key="content",
            history_messages_key="memory"
        )

    return chain
