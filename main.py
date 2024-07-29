import os
import streamlit as st
import logging
from lib.agent import agent_node
from lib.init_app import init_app
from lib.pick_ollama_model import pick_ollama_model
from langchain_core.pydantic_v1 import BaseModel, Field
from lib.message_queue import MessageQueue
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import date
from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun



def main():
    message_queue = MessageQueue()

    init_app(app_name="Thoth", app_title="Chat with Thoth")

    with st.sidebar:
        user_id = st.text_input("Username", "Anon")
        llm_model = st.radio("Choose a LLM model",
                             pick_ollama_model('llama3.1:latest'))
        llm_temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
        llm_file_data = st.file_uploader(
            "Upload a file", type=["txt", "csv", "json", "pdf"])

    # Create or get user-specific chat history
    memory = StreamlitChatMessageHistory(key=f"chat_messages_{user_id}")
    message_queue.add_user(user_id)

    if not memory.messages:
        memory.add_ai_message(
            "Hello! I am the embodiment Thoth, your personal AI assistant. How can I help you today?")

    messages = message_queue.get_messages(user_id)
    for message in memory.messages:
        st.chat_message(message.type).write(message.content)
        logging.info(f"Displayed message for user {user_id}: {message}")

    if prompt := st.chat_input():
        st.chat_message("human").write(prompt)
        message_queue.put_message(
            user_id, {"type": "human", "content": prompt})

        config = {"configurable": {"session_id": user_id}}

        with st.spinner("Thinking..."):
            zeke = agent_node(model=llm_model, memory=memory,
                              system_message=f"Your name is Thoth. The user's username is {
                                  user_id}. Today's Date: {date.today()}",
                              temperature=llm_temperature, tools=[], file=llm_file_data)

            response = zeke.invoke({'content': prompt}, config=config)
        st.chat_message("ai").write(response)
        message_queue.put_message(
            user_id, {"type": "ai", "content": response})


if __name__ == "__main__":
    main()
