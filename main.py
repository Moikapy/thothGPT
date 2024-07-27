# app.py
import os
import streamlit as st
from lib.agent import agent_node
from lib.init_app import init_app
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_community.tools import DuckDuckGoSearchRun


def main():
    init_app(app_name="Thoth", app_title="Chat with Thoth")

    with st.sidebar:
        user_id = st.text_input("Username", "Anon")
        llm_provider = st.radio(
            "Choose a LLM provider",
            ("ollama", "openai",),
        )
        llm_model = ''
        if llm_provider == "ollama":
            llm_model = st.radio(
                "Choose a LLM model",
                ("llama3.1:latest", "llama3", "llama2", "gemma2", "starcoder2:3b"),
            )
        # IF provider is openai
        if llm_provider == "openai":
            api_key = st.text_input("API Key", "insert your API key here")
            os.environ["API_KEY"] = api_key
            base_url = st.text_input("Base URL", "insert your base URL here")
            os.environ["BASE_URL"] = base_url

        llm_temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
        llm_file_data = st.file_uploader(
            "Upload a file", type=["txt", "csv", "json", "pdf"])

    memory = StreamlitChatMessageHistory(key="chat_messages")

    
    if not memory.messages:
        memory.add_ai_message(
            "Hello! I am Zeke, your personal AI assistant. How can I help you today?")

    for message in memory.messages:
        st.chat_message(message.type).write(message.content)

    if prompt := st.chat_input():
        print(llm_file_data)
        st.chat_message("human").write(prompt)

        config = {"configurable": {"session_id": user_id}}

        with st.spinner("Thinking..."):
            zeke = agent_node(model=llm_model, memory=memory,
                              system_message="Your name is Zeke. You are apart of University of Louisville - Information Technology Department - Integrative Design and Development Team. The user's user name is " + user_id, temperature=llm_temperature, tools=[DuckDuckGoSearchRun()], file=llm_file_data)

            response = zeke.invoke(
                {'content': prompt}, config=config)

        st.chat_message("ai").write(response.content)


if __name__ == "__main__":
    main()
