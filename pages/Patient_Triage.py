import streamlit as st
import pandas as pd

st.title("Patient Triage System")
st.write("---")
st.header("Patient Data Input")

st.subheader("Bulk Patient Intake")

uploaded_file = st.file_uploader(
    "Upload Patient CSV",
    type=["csv"]
)

st.caption(
    "Expected columns: Patient Name, Dosage"
)

col_config_1, col_config_2 = st.columns(2)
with col_config_1:
    safety_threshold = st.number_input("Safety Threshold (mg)", min_value=0.0, value=500.0, step=10.0)
with col_config_2:
    bed_limit = st.number_input(
        "High Priority Bed Limit",
        min_value=1,
        value=st.session_state["bed_limit"],
        step=1,
    )

st.session_state["bed_limit"] = bed_limit
if st.button("Run Patient Triage Audit"):
    if uploaded_file is None:
        st.error("Please upload a CSV file.")
        st.stop()

    try:
        df = pd.read_csv(uploaded_file)

        patients = df["Patient Name"].tolist()
        dosages = df["Dosage"].tolist()

    except Exception:
        st.error(
            "CSV format error. Expected columns: Patient Name, Dosage"
        )
        st.stop()

    if len(patients) != len(dosages):
        st.error(
            f"Mismatch Error: You entered {len(patients)} names but {len(dosages)} dosages."
        )
    else:
        st.session_state["high_priority_room"] = {}
        st.session_state["normal_room"] = {}
        st.session_state["waitlist"] = {}
        st.session_state["next_patient_id"] = 101
        st.session_state["next_waitlist_order"] = 1

        for i in range(len(patients)):
            patient_id = st.session_state["next_patient_id"]
            st.session_state["next_patient_id"] += 1
            
            if dosages[i] > safety_threshold:

                if len(st.session_state["high_priority_room"]) < bed_limit:
                    st.session_state["high_priority_room"][patient_id] = [
                        patients[i],
                        dosages[i],
                    ]

                else:
                    arrival_order = st.session_state["next_waitlist_order"]
                    st.session_state["next_waitlist_order"] += 1

                    st.session_state["waitlist"][patient_id] = [
                        patients[i],
                        dosages[i],
                        arrival_order,
                    ]

            else:
                st.session_state["normal_room"][patient_id] = [
                    patients[i],
                    dosages[i],
                ]
                
        st.success(f"""
    Triage processing complete!

    Imported {len(patients)} patients
    """)

# Branding footer
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.divider()
foot_col1, foot_col2 = st.columns([1, 5])
with foot_col1:
    st.image("cliniforge_logo.png", width=50)
with foot_col2:
    st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
    st.image("CliniForgeBanner.png", width=180)