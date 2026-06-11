import streamlit as st

# Inject custom CSS to load and apply the Inter font
st.markdown(
    """
    <style>
    /* Import Inter font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Force the entire app to use Inter */
    html, body, [class*="css"], .stMarkdown, p, label, span {
        font-family: 'Inter', sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(
    page_title="CliniForge Triage", 
    page_icon="cliniforge_logo.png", 
    layout="wide"
)

st.sidebar.image("cliniforge_logo.png", use_container_width=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

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

def rearrange(hpRoom, normRoom, safety_threshold, bed_limit):
    # 1. Move from High Priority to Normal (No capacity limit to worry about here)
    pat_ids_to_move_to_norm = []
    for patID in hpRoom.keys():
        if hpRoom[patID][1] <= safety_threshold:
            pat_ids_to_move_to_norm.append(patID)

    for patID in pat_ids_to_move_to_norm:
        normRoom[patID] = hpRoom.pop(patID)

    # 2. Move from Normal to High Priority (Must respect bed_limit!)
    pat_ids_to_move_to_hp = []
    for patID in normRoom.keys():
        if normRoom[patID][1] > safety_threshold:
            pat_ids_to_move_to_hp.append(patID)

    for patID in pat_ids_to_move_to_hp:
        # Only move if there is an available bed
        if len(hpRoom) < bed_limit:
            hpRoom[patID] = normRoom.pop(patID)
        else:
            # If HP room is full, they have to stay in the Normal Room (Overflow)
            break

# 1. Initialize session state at the very top of your app
if "high_priority_room" not in st.session_state:
    st.session_state["high_priority_room"] = {}
if "normal_room" not in st.session_state:
    st.session_state["normal_room"] = {}

st.title("Clinical Triage & Chart Review System")

# 2. Dynamic Input Fields (Restored functionality)
st.header("📥 Patient Data Input")

names_raw = st.text_input(
    "Enter Patient Names (separated by commas)", 
    value="Alice, Bob, Charlie, David, Eve"
)
dosages_raw = st.text_input(
    "Enter Dosages (separated by commas)", 
    value="600, 120, 750, 400, 95"
)

# Configuration settings
col_config_1, col_config_2 = st.columns(2)
with col_config_1:
    safety_threshold = st.number_input("Safety Threshold (mg)", min_value=0.0, value=500.0, step=10.0)
with col_config_2:
    bed_limit = st.number_input("High Priority Bed Limit", min_value=1, value=2, step=1)

# 3. Processing Button with Dynamic Parsing
if st.button("Run Patient Triage Audit"):
    # Convert comma-separated strings into clean Python lists
    patients = [name.strip() for name in names_raw.split(",") if name.strip()]
    
    try:
        dosages = [float(dose.strip()) for dose in dosages_raw.split(",") if dose.strip()]
    except ValueError:
        st.error("❌ Error: Please ensure all dosages entered are valid numbers.")
        st.stop()

    # Validation: Ensure lists match in length
    if len(patients) != len(dosages):
        st.error(f"❌ Mismatch Error: You entered {len(patients)} names but {len(dosages)} dosages. They must match.")
    else:
        # Reset rooms for a fresh audit cycle
        st.session_state["high_priority_room"] = {}
        st.session_state["normal_room"] = {}
        
        # Run triage loop using the user-defined variables
        for i in range(len(patients)):
            patient_id = 101 + i 
            
            if dosages[i] > safety_threshold:
                if len(st.session_state["high_priority_room"]) >= bed_limit:
                    # Overflow: Skip to normal room instead of dropping the patient
                    st.session_state["normal_room"][patient_id] = [patients[i], dosages[i]]
                    continue
                st.session_state["high_priority_room"][patient_id] = [patients[i], dosages[i]]
            else:
                st.session_state["normal_room"][patient_id] = [patients[i], dosages[i]]
                
        st.success("✅ Triage processing complete!")
        st.rerun()

# 4. Clean Row-Based Dashboard Display
st.divider()
st.subheader("🏥 Active Room Status")
col1, col2 = st.columns(2)

with col1:
    st.write("🔴 **High Priority Room**")
    if st.session_state["high_priority_room"]:
        hp_rows = [{"Patient ID": k, "Patient Name": v[0], "Dosage (mg)": v[1]} 
                   for k, v in st.session_state["high_priority_room"].items()]
        st.dataframe(hp_rows, use_container_width=True, hide_index=True)
    else:
        st.info("Room is currently empty.")

with col2:
    st.write("🟢 **Normal Room**")
    if st.session_state["normal_room"]:
        norm_rows = [{"Patient ID": k, "Patient Name": v[0], "Dosage (mg)": v[1]} 
                     for k, v in st.session_state["normal_room"].items()]
        st.dataframe(norm_rows, use_container_width=True, hide_index=True)
    else:
        st.info("Room is currently empty.")

# 5. Chart Review Section in the 1_Chart_Review.py file
