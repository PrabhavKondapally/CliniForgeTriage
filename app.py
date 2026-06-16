import streamlit as st

# Core sorting algorithm for active patient redistribution
def rearrange(hpRoom, normRoom, waitlist, safety_threshold, bed_limit):
    # Demote patients falling below or equal to the safety threshold
    pat_ids_to_move_to_norm = []
    for patID in hpRoom.keys():
        if hpRoom[patID][1] <= safety_threshold:
            pat_ids_to_move_to_norm.append(patID)

    for patID in pat_ids_to_move_to_norm:
        normRoom[patID] = hpRoom.pop(patID)

    # Promote patients exceeding the threshold if beds are available
    pat_ids_to_move_to_hp = []
    for patID in normRoom.keys():
        if normRoom[patID][1] > safety_threshold:
            pat_ids_to_move_to_hp.append(patID)

    for patID in pat_ids_to_move_to_hp:
        if len(hpRoom) < bed_limit:
            hpRoom[patID] = normRoom.pop(patID)
        else:
            patient_data = normRoom.pop(patID)

            arrival_order = st.session_state["next_waitlist_order"]
            st.session_state["next_waitlist_order"] += 1

            waitlist[patID] = [
                patient_data[0],
                patient_data[1],
                arrival_order,
            ]
    
    # Fill any newly available high-priority beds from the waitlist
    while len(hpRoom) < bed_limit and waitlist:

        best_patient_id = sorted(
            waitlist,
            key=lambda pid: (-waitlist[pid][1], waitlist[pid][2]),
        )[0]

        patient_data = waitlist.pop(best_patient_id)

        hpRoom[best_patient_id] = [
            patient_data[0],
            patient_data[1],
        ]

# Navigation configurations
main_page = st.Page("app.py", title="Main Dashboard", icon="📊", default=True)
triage_page = st.Page("pages/Patient_Triage.py", title="Patient Triage", icon="📋")
review_page = st.Page("pages/Chart_Review.py", title="Chart Review", icon="🔍")

pg = st.navigation([main_page, triage_page, review_page])

st.set_page_config(
    page_title="CliniForge Triage", 
    page_icon="cliniforge_logo.png", 
    layout="wide"
)

# Persistent global data stores for tracking patient distribution
if "high_priority_room" not in st.session_state:
    st.session_state["high_priority_room"] = {}
if "normal_room" not in st.session_state:
    st.session_state["normal_room"] = {}
if "waitlist" not in st.session_state:
    st.session_state["waitlist"] = {}
if "next_patient_id" not in st.session_state:
    st.session_state["next_patient_id"] = 101
if "next_waitlist_order" not in st.session_state:
    st.session_state["next_waitlist_order"] = 1

# Route control checkpoint
if pg.title != "Main Dashboard":
    pg.run()
    st.stop()

# =========================================================================
# MAIN DASHBOARD VIEW (Only executes when Main Dashboard is active)
# =========================================================================
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

# Branding Header Section
col1, col2 = st.columns([1, 4])
with col1:
    st.image("cliniforge_logo.png", width=90)
with col2:
    st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
    st.image("CliniForgeBanner.png", width=350)

st.divider()

st.title("Main Dashboard")
st.subheader("Active Room Status Overview")

# Parameter Configuration Inputs
st.write("### Quick Adjustment Controls")

col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    ui_threshold = st.number_input(
        "Adjust Safety Threshold (mg)",
        min_value=0.0,
        value=500.0,
        step=10.0,
    )

with col_ctrl2:
    ui_bed_limit = st.number_input(
        "Adjust Bed Limit Capacity",
        min_value=1,
        value=2,
        step=1,
    )

st.write("### Add New Patient")

with st.form("add_patient_form", clear_on_submit=True):
    col_add1, col_add2 = st.columns(2)

    with col_add1:
        patient_name = st.text_input("Patient Name")

    with col_add2:
        patient_dosage = st.number_input(
            "Patient Dosage (mg)",
            min_value=0.0,
            step=10.0,
        )

    submit_patient = st.form_submit_button("Add Patient")

    if submit_patient:
        patient_id = st.session_state["next_patient_id"]
        st.session_state["next_patient_id"] += 1

        # High-priority candidate
        if patient_dosage > ui_threshold:

            # Bed available
            if len(st.session_state["high_priority_room"]) < ui_bed_limit:
                st.session_state["high_priority_room"][patient_id] = [
                    patient_name,
                    patient_dosage,
                ]

            # No bed available -> send to waitlist
            else:
                arrival_order = st.session_state["next_waitlist_order"]
                st.session_state["next_waitlist_order"] += 1

                st.session_state["waitlist"][patient_id] = [
                    patient_name,
                    patient_dosage,
                    arrival_order,
                ]

        # Normal patient
        else:
            st.session_state["normal_room"][patient_id] = [
                patient_name,
                patient_dosage,
            ]

        st.success(f"Patient added successfully! Assigned ID: {patient_id}")
        st.rerun()
# =========================================================================
# INDIVIDUAL PATIENT DOSAGE OVERRIDE FEATURE
# =========================================================================
st.write("### Individual Patient Dosage Override")
with st.form("override_form", clear_on_submit=True):
    col_ov1, col_ov2 = st.columns(2)
    with col_ov1:
        target_id = st.number_input("Enter Patient ID to update", min_value=100, step=1)
    with col_ov2:
        new_dosage = st.number_input("Enter New Dosage (mg)", min_value=0.0, step=10.0)
        
    submit_override = st.form_submit_button("Update Patient Dosage")
    
    if submit_override:
        found = False
        # Look in high priority room
        if target_id in st.session_state["high_priority_room"]:
            st.session_state["high_priority_room"][target_id][1] = new_dosage
            found = True
        # Look in normal room
        elif target_id in st.session_state["normal_room"]:
            st.session_state["normal_room"][target_id][1] = new_dosage
            found = True
            
        if found:
        # Automatically rearrange patients after a dosage update
            rearrange(
                st.session_state["high_priority_room"],
                st.session_state["normal_room"],
                st.session_state["waitlist"],
                ui_threshold,
                ui_bed_limit,
            )

            st.success(
                f"Patient {target_id} dosage updated to {new_dosage} mg successfully!"
            )

            # Refresh the page so the updated tables appear immediately
            st.rerun()

        else:
            st.error(f"Patient ID {target_id} not found in any active room.")

# Remove Patient form
st.write("### Remove Patient")

with st.form("remove_patient_form", clear_on_submit=True):

    remove_id = st.number_input(
        "Enter Patient ID to Remove",
        min_value=100,
        step=1,
    )

    submit_remove = st.form_submit_button("Remove Patient")

    if submit_remove:

        removed = False

        if remove_id in st.session_state["high_priority_room"]:
            del st.session_state["high_priority_room"][remove_id]
            removed = True

        elif remove_id in st.session_state["normal_room"]:
            del st.session_state["normal_room"][remove_id]
            removed = True

        elif remove_id in st.session_state["waitlist"]:
            del st.session_state["waitlist"][remove_id]
            removed = True

        if removed:

            rearrange(
                st.session_state["high_priority_room"],
                st.session_state["normal_room"],
                st.session_state["waitlist"],
                ui_threshold,
                ui_bed_limit,
            )

            st.success(
                f"Patient {remove_id} removed successfully."
            )

            st.rerun()

        else:
            st.error(
                f"Patient ID {remove_id} not found."
            )


# Display Room Status
col_hp, col_norm, col_wait = st.columns(3)

# High Priority Room Display
with col_hp:
    st.write("**High Priority Room**")
    if st.session_state["high_priority_room"]:
        hp_rows = [{"Patient ID": k, "Patient Name": v[0], "Dosage (mg)": v[1]} 
                   for k, v in st.session_state["high_priority_room"].items()]
        st.dataframe(hp_rows, use_container_width=True, hide_index=True)
    else:
        st.info("Room is currently empty.")

# Normal Room Display
with col_norm:
    st.write("**Normal Room**")
    if st.session_state["normal_room"]:
        norm_rows = [{"Patient ID": k, "Patient Name": v[0], "Dosage (mg)": v[1]} 
                     for k, v in st.session_state["normal_room"].items()]
        st.dataframe(norm_rows, use_container_width=True, hide_index=True)
    else:
        st.info("Room is currently empty.")

# Waitlist Display
# Waitlist Display
with col_wait:
    st.write("**Waitlist**")

    if st.session_state["waitlist"]:
        wait_rows = []

        sorted_waitlist = sorted(
            st.session_state["waitlist"].items(),
            key=lambda item: (-item[1][1], item[1][2]),
        )

        for position, (patient_id, patient_data) in enumerate(
            sorted_waitlist,
            start=1,
        ):
            wait_rows.append(
                {
                    "Position": position,
                    "Patient ID": patient_id,
                    "Patient Name": patient_data[0],
                    "Dosage (mg)": patient_data[1],
                }
            )

        st.dataframe(
            wait_rows,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Waitlist is currently empty.")

st.write("")

# Dynamic rearrangement execution trigger
if st.button("Apply Changes & Rearrange Patients", type="primary"):
    rearrange(
        st.session_state["high_priority_room"], 
        st.session_state["normal_room"], 
        st.session_state["waitlist"],
        ui_threshold, 
        ui_bed_limit
    )
    st.success("Patients successfully redistributed based on updated values!")
    st.rerun()