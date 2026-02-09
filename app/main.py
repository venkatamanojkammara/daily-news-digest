import sys
from pathlib import Path

# Add project root to PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st

st.set_page_config(
    page_title="AI News Digest",
    page_icon="🗞️",
    layout="centered",
)

st.title("🗞️ AI News Digest")
st.subheader("Personalized daily news. Delivered to your inbox.")
