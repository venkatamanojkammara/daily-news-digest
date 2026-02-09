import streamlit as st
from backend.config import TOPICS

def email_input():
    return st.text_input("Email address")

def topic_selector(default=None):
    return st.multiselect(
        "Select topics you want to receive",
        options=TOPICS,
        default=default or []
    )

def time_selector(default="08:00"):
    return st.time_input(
        "Preferred delivery time",
        value=None,
        help="Your local time"
    )
