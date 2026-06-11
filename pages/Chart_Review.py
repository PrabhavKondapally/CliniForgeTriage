import streamlit as st

st.title("🔍 Clinical Chart Review")
st.write("---")

st.info("Medical chart AI summaries and electronic health record (EHR) validation toolsets will load here.")

# Branding footer
st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
st.divider()
foot_col1, foot_col2 = st.columns([1, 5])
with foot_col1:
    st.image("cliniforge_logo.png", width=50)
with foot_col2:
    st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
    st.image("CliniForgeBanner.png", width=180)