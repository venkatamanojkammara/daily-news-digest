import streamlit as st
from datetime import time

from backend.db.connection import get_session
from backend.db import crud
from backend.config import TOPICS
from app.components.alerts import success, error, info

st.title("⚙️ Preferences")
st.caption("Customize how and when you receive your news digest")

with st.form("preferences_form"):
    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------
    email = st.text_input(
        "Email address",
        help="Must match the email you used to subscribe"
    )

    # ------------------------------------------------------------------
    # Topics
    # ------------------------------------------------------------------
    topics = st.multiselect(
        "Topics you want to read",
        options=TOPICS,
        help="Select at least one topic"
    )

    # ------------------------------------------------------------------
    # Time settings
    # ------------------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        preffered_time = st.time_input(
            "Preferred delivery time",
            value=time(8, 0),
            help="Your local time"
        )

    with col2:
        time_zone = st.selectbox(
            "Timezone",
            options=[
                "Asia/Kolkata",
                "UTC",
                "Asia/Dubai",
                "Europe/London",
                "America/New_York"
            ],
            index=0
        )

    # ------------------------------------------------------------------
    # Future-ready (not yet used by backend)
    # ------------------------------------------------------------------
    st.divider()
    st.caption("Advanced (coming soon)")

    frequency = st.selectbox(
        "Digest frequency",
        ["Daily", "Weekdays", "Weekly"],
        disabled=True
    )

    max_articles = st.slider(
        "Maximum articles per digest",
        min_value=5,
        max_value=20,
        value=10,
        disabled=True
    )

    # ------------------------------------------------------------------
    # Submit
    # ------------------------------------------------------------------
    submitted = st.form_submit_button("Save Preferences")

# ----------------------------------------------------------------------
# Handle submission
# ----------------------------------------------------------------------
if submitted:
    if not email:
        error("Email is required.")
    elif not topics:
        error("Please select at least one topic.")
    else:
        try:
            with get_session() as db:
                # Update preferences
                crud.update_preferences(
                    db=db,
                    email=email,
                    topics=topics,
                    preffered_time=preffered_time.strftime("%H:%M"),
                    time_zone=time_zone
                )

                # Mark user as verified
                crud.set_verified(db, email, verified=True)

            success("Preferences saved successfully!")
            info("You will start receiving your daily digest at the selected time.")

        except Exception as e:
            error(str(e))
