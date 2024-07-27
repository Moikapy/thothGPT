# lib.llm.py
# This file contains the useOllama function which is used to create an instance of the ChatOllama class.
import streamlit as st

from langchain_ollama import ChatOllama


def useOllama(model="llama3.1:latest",temperature=0.5):
    return ChatOllama(model=model, keep_alive="5m", temperature=temperature)
