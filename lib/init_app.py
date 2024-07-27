# app.py
import streamlit as st

def init_app(app_name="Thoth", app_title="Chat with Thoth"):
    # Set the page tab title and layout
    st.set_page_config(page_title=app_name, layout="wide")
    # Set the title of the app
    st.title(app_title)
