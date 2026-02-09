"""
app/main.py
-----------

Single-file Streamlit UI for AI News Digest.

Features:
- Subscribe
- Set / Update preferences
- Pause / Resume subscription
- Unsubscribe
- Clean, simple, production-friendly UI

This file replaces all multi-page Streamlit files.
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from datetime import datetime
from typing import List

from backend.db.connection import get_session
from backend.db import crud
from backend.email.validators import is_valid_email

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="AI News Digest",
    page_icon="📰",
    layout="centered",
)

# --------------------------------------------------
# UI helpers
# --------------------------------------------------
def section(title: str, subtitle: str | None = None):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)
    st.divider()


def success(msg: str):
    st.success(msg, icon="✅")


def error(msg: str):
    st.error(msg, icon="❌")


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.title("📰 AI News Digest")
    st.caption("Personalized daily news delivered to your inbox")

    menu = st.radio(
        "Navigation",
        [
            "Subscribe",
            "Preferences",
            "Manage Subscription",
            "Unsubscribe",
        ],
    )

    st.divider()
    st.caption("Powered by AI + Supabase")


# --------------------------------------------------
# SUBSCRIBE
# --------------------------------------------------
if menu == "Subscribe":
    section("Subscribe", "Get a personalized AI-curated news digest daily")

    email = st.text_input("Email address", placeholder="you@example.com")

    if st.button("Subscribe", use_container_width=True):
        if not is_valid_email(email):
            error("Please enter a valid email address.")
        else:
            with get_session() as db:
                crud.create_subscriber(db, email)
            success("Subscription successful! Please set your preferences next.")

    st.info("After subscribing, go to **Preferences** to choose topics and time.")


# --------------------------------------------------
# PREFERENCES
# --------------------------------------------------
elif menu == "Preferences":
    section("Preferences", "Choose topics and delivery time")

    email = st.text_input("Registered email")

    topics = st.multiselect(
        "Topics you are interested in",
        [
            "Technology",
            "Business",
            "World",
            "Politics",
            "Sports"
        ],
    )

    preferred_time = st.time_input(
        "Preferred delivery time",
        value=datetime.strptime("08:00", "%H:%M").time(),
    )

    time_zone = st.selectbox(
        "Time zone",
        ["Asia/Kolkata", "UTC"],
        index=0,
    )

    if st.button("Save Preferences", use_container_width=True):
        if not is_valid_email(email):
            error("Invalid email address.")
        else:
            with get_session() as db:
                subscriber = crud.get_subscriber_by_email(db, email)
                if not subscriber:
                    error("Email not found. Please subscribe first.")
                else:
                    crud.update_preferences(
                        db=db,
                        email=email,
                        topics=topics,
                        preffered_time=preferred_time.strftime("%H:%M"),
                        time_zone=time_zone,
                    )
                    crud.set_verified(db, email)
                    success("Preferences saved successfully!")

    st.info("You will start receiving emails from the next scheduled time.")


# --------------------------------------------------
# MANAGE SUBSCRIPTION
# --------------------------------------------------
elif menu == "Manage Subscription":
    section("Manage Subscription", "Pause or resume your daily digest")

    email = st.text_input("Registered email")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Pause", use_container_width=True):
            with get_session() as db:
                try:
                    crud.pause_subscription(db, email)
                    success("Subscription paused.")
                except Exception as e:
                    error(str(e))

    with col2:
        if st.button("Resume", use_container_width=True):
            with get_session() as db:
                try:
                    crud.resume_subscription(db, email)
                    success("Subscription resumed.")
                except Exception as e:
                    error(str(e))


# --------------------------------------------------
# UNSUBSCRIBE
# --------------------------------------------------
elif menu == "Unsubscribe":
    section("Unsubscribe", "Stop receiving emails permanently")

    email = st.text_input("Registered email")

    if st.button("Unsubscribe", use_container_width=True):
        with get_session() as db:
            try:
                crud.unsubscribe(db, email)
                success("You have been unsubscribed successfully.")
            except Exception as e:
                error(str(e))

    st.warning(
        "You can re-subscribe anytime using the same email.",
        icon="⚠️",
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption("© AI News Digest — Built with Streamlit, Supabase & Gemini AI")
