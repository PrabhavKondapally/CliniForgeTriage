import streamlit as st

st.title("Session Information")
st.write("---")

st.subheader("Current Session Summary")

hp_count = len(st.session_state["high_priority_room"])
normal_count = len(st.session_state["normal_room"])
waitlist_count = len(st.session_state["waitlist"])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("High Priority", hp_count)

with col2:
    st.metric("Normal", normal_count)

with col3:
    st.metric("Waitlist", waitlist_count)

with col4:
    st.metric(
        "Total",
        hp_count + normal_count + waitlist_count
    )

st.write("---")

st.subheader("Audit History")

if st.session_state["audit_log"]:
    for event in reversed(st.session_state["audit_log"]):
        st.write(f"• {event}")
else:
    st.info("No audit events recorded yet.")

# Branding footer
st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
st.divider()

foot_col1, foot_col2 = st.columns([1, 5])

with foot_col1:
    st.image("cliniforge_logo.png", width=50)

with foot_col2:
    st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
    st.image("CliniForgeBanner.png", width=180)