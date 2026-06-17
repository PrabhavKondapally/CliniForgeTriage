import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Clinical Chart Review")
st.write("---")

st.subheader("Hospital Overview")

hp_count = len(st.session_state.get("high_priority_room", {}))
normal_count = len(st.session_state.get("normal_room", {}))
waitlist_count = len(st.session_state.get("waitlist", {}))

total_patients = hp_count + normal_count + waitlist_count

all_dosages = []

for patient in st.session_state.get("high_priority_room", {}).values():
    all_dosages.append(patient[1])

for patient in st.session_state.get("normal_room", {}).values():
    all_dosages.append(patient[1])

for patient in st.session_state.get("waitlist", {}).values():
    all_dosages.append(patient[1])

if all_dosages:
    avg_dosage = round(sum(all_dosages) / len(all_dosages), 2)
    highest_dosage = max(all_dosages)
    lowest_dosage = min(all_dosages)
else:
    avg_dosage = 0
    highest_dosage = 0
    lowest_dosage = 0

bed_limit = st.session_state.get("bed_limit", 2)

if bed_limit > 0:
    bed_utilization = round((hp_count / bed_limit) * 100, 1)
else:
    bed_utilization = 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Patients", total_patients)

with col2:
    st.metric("High Priority", hp_count)

with col3:
    st.metric("Normal Room", normal_count)

with col4:
    st.metric("Waitlist", waitlist_count)

st.write("")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Average Dosage (mg)", avg_dosage)

with col6:
    st.metric("Highest Dosage (mg)", highest_dosage)

with col7:
    st.metric("Lowest Dosage (mg)", lowest_dosage)

with col8:
    st.metric("Bed Utilization (%)", bed_utilization)

st.write("---")

st.subheader("High Priority Bed Occupancy")

occupied_beds = hp_count
total_beds = bed_limit

bed_display = ""

for i in range(total_beds):

    if i < occupied_beds:
        bed_display += "🟥 "
    else:
        bed_display += "⬜ "

st.markdown(f"## {bed_display}")

st.write(
    f"**{occupied_beds} / {total_beds} Beds Occupied**"
)

st.write("---")

st.subheader("Patient Distribution")

distribution_df = pd.DataFrame(
    {
        "Category": [
            "High Priority",
            "Normal Room",
            "Waitlist",
        ],
        "Patients": [
            hp_count,
            normal_count,
            waitlist_count,
        ],
    }
)

fig = px.bar(
    distribution_df,
    x="Category",
    y="Patients",
    title="Patient Distribution by Room",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# Branding footer
st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
st.divider()
foot_col1, foot_col2 = st.columns([1, 5])
with foot_col1:
    st.image("cliniforge_logo.png", width=50)
with foot_col2:
    st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
    st.image("CliniForgeBanner.png", width=180)