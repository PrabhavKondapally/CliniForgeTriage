import streamlit as st

# 1. CORE ALGORITHM LOGIC
def rearrange(hpRoom, normRoom, safety_threshold, bed_limit):
    # Move from High Priority to Normal
    pat_ids_to_move_to_norm = []
    for patID in hpRoom.keys():
        if hpRoom[patID][1] <= safety_threshold:
            pat_ids_to_move_to_norm.append(patID)

    for patID in pat_ids_to_move_to_norm:
        normRoom[patID] = hpRoom.pop(patID)

    # Move from Normal to High Priority (Respecting bed_limit!)
    pat_ids_to_move_to_hp = []
    for patID in normRoom.keys():
        if normRoom[patID][1] > safety_threshold:
            pat_ids_to_move_to_hp.append(patID)

    for patID in pat_ids_to_move_to_hp:
        if len(hpRoom) < bed_limit:
            hpRoom[patID] = normRoom.pop(patID)
        else:
            break


# 2. GLOBAL ROUTING & CONFIGURATION
# Defining the pages using the repository paths
main_page = st.Page("app.py", title="Main Dashboard", icon="📊", default=True)
triage_page = st.Page("pages/Patient_Triage.py", title="Patient Triage", icon="📋")
review_page = st.Page("pages/Chart_Review.py", title="Chart Review", icon="🔍")

# Initialize multi-page navigation layout
pg = st.navigation([main_page, triage_page, review_page])

# Global Page Config (applied across all views)
st.set_page_config(
    page_title="CliniForge Triage", 
    page_icon="cliniforge_logo.png", 
    layout="wide"
)

# Global Session State Initialization
if "high_priority_room" not in st.session_state:
    st.session_state["high_priority_room"] = {}
if "normal_room" not in st.session_state:
    st.session_state["normal_room"] = {}


# 3. PAGE RUNNER & DASHBOARD DISPLAY LOGIC
if pg.current_path == "app.py":
    
    # Inject Inter font formatting
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"], .stMarkdown, p, label, span {
            font-family: 'Inter', sans-serif !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Main Branding Header (Top of Dashboard)
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("cliniforge_logo.png", width=90)
    with col2:
        st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
        st.image("CliniForgeBanner.png", width=350)

    st.divider()

    # Dashboard Content
    st.title("📊 Main Dashboard")
    st.subheader("🏥 Active Room Status Overview")

    col_hp, col_norm = st.columns(2)

    with col_hp:
        st.write("🔴 **High Priority Room**")
        if st.session_state["high_priority_room"]:
            hp_rows = [{"Patient ID": k, "Patient Name": v[0], "Dosage (mg)": v[1]} 
                       for k, v in st.session_state["high_priority_room"].items()]
            st.dataframe(hp_rows, use_container_width=True, hide_index=True)
        else:
            st.info("Room is currently empty.")

    with col_norm:
        st.write("🟢 **Normal Room**")
        if st.session_state["normal_room"]:
            norm_rows = [{"Patient ID": k, "Patient Name": v[0], "Dosage (mg)": v[1]} 
                         for k, v in st.session_state["normal_room"].items()]
            st.dataframe(norm_rows, use_container_width=True, hide_index=True)
        else:
            st.info("Room is currently empty.")

else:
    # If the user clicked Triage or Review, execute that specific file instead!
    pg.run()