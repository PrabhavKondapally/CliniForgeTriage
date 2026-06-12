import streamlit as st

st.title("Patient Triage System")
st.write("---")
st.header("Patient Data Input")

names_raw = st.text_input(
    "Enter Patient Names (separated by commas)", 
    value="Alice, Bob, Charlie, David, Eve"
)
dosages_raw = st.text_input(
    "Enter Dosages (separated by commas)", 
    value="600, 120, 750, 400, 95"
)

col_config_1, col_config_2 = st.columns(2)
with col_config_1:
    safety_threshold = st.number_input("Safety Threshold (mg)", min_value=0.0, value=500.0, step=10.0)
with col_config_2:
    bed_limit = st.number_input("High Priority Bed Limit", min_value=1, value=2, step=1)

if st.button("Run Patient Triage Audit"):
    patients = [name.strip() for name in names_raw.split(",") if name.strip()]
    
    try:
        dosages = [float(dose.strip()) for dose in dosages_raw.split(",") if dose.strip()]
    except ValueError:
        st.error("Error: Please ensure all dosages entered are valid numbers.")
        st.stop()

    if len(patients) != len(dosages):
        st.error(f"Mismatch Error: You entered {len(patients)} names but {len(dosages)} dosages.")
    else:
        st.session_state["high_priority_room"] = {}
        st.session_state["normal_room"] = {}
        
        for i in range(len(patients)):
            patient_id = st.session_state["next_patient_id"]
            st.session_state["next_patient_id"] += 1
            
            if dosages[i] > safety_threshold:
                if len(st.session_state["high_priority_room"]) >= bed_limit:
                    st.session_state["normal_room"][patient_id] = [patients[i], dosages[i]]
                    continue
                st.session_state["high_priority_room"][patient_id] = [patients[i], dosages[i]]
            else:
                st.session_state["normal_room"][patient_id] = [patients[i], dosages[i]]
                
        st.success("Triage processing complete! Navigate to the Main Dashboard to view allocations.")

# Branding footer
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.divider()
foot_col1, foot_col2 = st.columns([1, 5])
with foot_col1:
    st.image("cliniforge_logo.png", width=50)
with foot_col2:
    st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
    st.image("CliniForgeBanner.png", width=180)