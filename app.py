
# app.py
import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# prompt = ChatPromptTemplate.from_template(

#     "system",
#     ["You are Thoth. You are a helpful human assistant, collaborating with other assistants."
#      " If you are unable to fully answer, that's OK, another assistant with different tools "
#      " will help where you left off. Execute what you can to make progress."
#      " If you or any of the other assistants have the final answer or deliverable,"
#      " prefix your response with FINAL ANSWER so the team knows to stop."]
#     # " You have access to the following tools: {tool_names}.\n{system_message}",

# )


def useOllama(model="llama3.1:latest"):
    llm = ChatOllama(model=model)
    return llm


def sendPrompt(prompt):
    llm = useOllama(model="llama3.1:latest")
    response = llm.invoke(prompt)
    return response


def main():
    st.set_page_config(page_title="Gnosis.AI", layout="wide")

    st.title("Chat with Gnosis.AI")
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question !"}
        ]

    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = sendPrompt(prompt)
                # print(response.content)
                st.write(response.content)
                message = {"role": "assistant", "content": response.content}
                st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
