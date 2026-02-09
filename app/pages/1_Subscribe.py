import streamlit as st

from backend.db.connection import get_session
from backend.db import crud
from backend.email.validators import is_valid_email
from app.components.alerts import success, error, info

st.title("📩 Subscribe")
st.caption("Start receiving a personalized AI-powered daily news digest")

with st.form("subscribe_form"):
    email = st.text_input(
        "Email address",
        placeholder="you@example.com",
        help="We will send your daily news digest to this email"
    )

    submitted = st.form_submit_button("Subscribe")

if submitted:
    if not email:
        error("Email address is required.")
    elif not is_valid_email(email):
        error("Please enter a valid email address.")
    else:
        with get_session() as db:
            user = crud.get_subscriber_by_email(db, email)
            if user:
                info("You are already subscribed. You can update your preferences.")
            else:
                crud.create_subscriber(db, email)
                success("Subscription successful!")
                info("Next step: Go to the Preferences page to choose topics and delivery time.")
