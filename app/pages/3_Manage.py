import streamlit as st

from backend.db.connection import get_session
from backend.db import crud
from app.components.alerts import success, error, info

st.title("🛠 Manage Subscription")
st.caption("Pause or resume your daily news digest anytime")

with st.form("manage_form"):
    email = st.text_input(
        "Email address",
        placeholder="you@example.com",
        help="Enter the email you used to subscribe"
    )

    col1, col2 = st.columns(2)
    with col1:
        pause = st.form_submit_button("Pause Emails")
    with col2:
        resume = st.form_submit_button("Resume Emails")

if pause:
    if not email:
        error("Email address is required.")
    else:
        try:
            with get_session() as db:
                crud.pause_subscription(db, email)
            success("Your subscription has been paused.")
        except Exception:
            error("We could not find a subscription for this email.")

if resume:
    if not email:
        error("Email address is required.")
    else:
        try:
            with get_session() as db:
                crud.resume_subscription(db, email)
            success("Your subscription has been resumed.")
        except Exception:
            error("We could not find a subscription for this email.")
