import streamlit as st

def success(msg: str):
    st.success(msg)

def error(msg: str):
    st.error(msg)

def info(msg: str):
    st.info(msg)
