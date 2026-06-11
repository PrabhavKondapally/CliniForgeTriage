import streamlit as st

# 1. Page Config (Streamlit needs this on every sub-page)
st.set_page_config(
    page_title="Chart Review - CliniForge", 
    page_icon="cliniforge_logo.png",
    layout="wide"
)

st.sidebar.image("cliniforge_logo.png", use_container_width=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# 2. Re-import your font styles so it matches
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

# 1. Creating two columns at the top of your page
# The [1, 4] ratio makes the logo column narrow and the text column wide
col1, col2 = st.columns([1, 4])

with col1:
    # Displaying logo
    st.image("cliniforge_logo.png", width=90)

with col2:
    # Adding a bit of vertical spacing so the text aligns with the middle of the logo
    st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
    
    # Displaying the newly created two-tone CliniForge text banner
    st.image("CliniForgeBanner.png", width=350)

# Adding a thin horizontal divider line underneath the brand-new header
st.divider()

# 3. Bring back your header layout or a sub-page title
st.title("Patient Chart Review & Overrides")
st.divider()

# 4. Your Exact Rearrange Function (Needs to be here to run)
def rearrange(hpRoom, normRoom, safety_threshold, bed_limit):
    pat_ids_to_move_to_norm = [pid for pid in hpRoom.keys() if hpRoom[pid][1] <= safety_threshold]
    for patID in pat_ids_to_move_to_norm:
        normRoom[patID] = hpRoom.pop(patID)

    pat_ids_to_move_to_hp = [pid for pid in normRoom.keys() if normRoom[pid][1] > safety_threshold]
    for patID in pat_ids_to_move_to_hp:
        if len(hpRoom) < bed_limit:
            hpRoom[patID] = normRoom.pop(patID)
        else:
            break

# 5. Place your Editing UI Inputs here
search_id = st.number_input("Enter Patient ID to Review", min_value=101, step=1)
new_dosage_input = st.number_input("New Target Dosage (mg)", min_value=0.0, step=10.0)

# Note: Since the sliders are on the main page, we use a fallback value or add inputs here
safety_threshold = 500.0  
bed_limit = 2

if st.button("Update Patient Record"):
    if "high_priority_room" in st.session_state and search_id in st.session_state["high_priority_room"]:
        st.session_state["high_priority_room"][search_id][1] = new_dosage_input
        patient_name = st.session_state["high_priority_room"][search_id][0]
        rearrange(st.session_state["high_priority_room"], st.session_state["normal_room"], safety_threshold, bed_limit)
        st.success(f"✅ High Priority Updated: {patient_name} (ID: {search_id}) changed to {new_dosage_input}mg.")
        st.rerun()
        
    elif "normal_room" in st.session_state and search_id in st.session_state["normal_room"]:
        st.session_state["normal_room"][search_id][1] = new_dosage_input
        patient_name = st.session_state["normal_room"][search_id][0]
        rearrange(st.session_state["high_priority_room"], st.session_state["normal_room"], safety_threshold, bed_limit)
        st.success(f"✅ Normal Room Updated: {patient_name} (ID: {search_id}) changed to {new_dosage_input}mg.")
        st.rerun()
        
    else:
        st.error(f"❌ Error: Patient ID {search_id} cannot be found in active memory.")