import streamlit as st
from firebase_auth import login

st.title("🔐 CliniForge Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        user = login(email, password)

        print(user.keys())

        st.session_state["logged_in"] = True
        st.session_state["user_email"] = user["email"]
        st.session_state["user_id"] = user["localId"]

        st.success("Login successful!")
        st.rerun()

    except Exception:
        st.error("Invalid email or password.")