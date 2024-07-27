# agent.py
from lib.llm import useOllama
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory


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
            ("system", system_message),
            MessagesPlaceholder("memory"),
            ("human", "{content}"),
        ]
    )
    ollama = useOllama(model=model, temperature=temperature)
    if tools:
        ollama.bind_tools(tools)
    chain = prompt | ollama
    if memory:
        chain = RunnableWithMessageHistory(
            chain,
            lambda session_id: memory,
            input_messages_key="content",
            history_messages_key="memory"
        )

    return chain
