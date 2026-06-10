# 🏥 Clinical Patient Priority Queue & Triage Simulator

### 🌐 [Click Here to View the Live Web Application]([https://YOUR-CUSTOM-URL.streamlit.app](https://prabhavkondapally-medical-triage.streamlit.app/))

---

## 📌 Project Overview
This project is an interactive web application designed to simulate hospital capacity management and clinical dosage safety auditing. Built using **Python** and **Streamlit**, the simulator models real-world healthcare operational challenges by automatically routing incoming patients into optimized care facilities based on dynamic safety thresholds and strict room/bed constraints.

I engineered this project to explore the intersection of **Computer Science and Healthcare**, specifically studying how software logic can prevent emergency department overcrowding, mitigate clinical risk, and automate administrative workflows for triage nurses.

---

## ⚙️ Key Features & Technical Architecture

* **Dynamic Risk Evaluation:** Users can input a list of patients and their prescribed medication dosages. The backend parses and cleans the string inputs using data sterilization techniques.
* **Algorithmic Patient Routing:** The system runs a core evaluation loop that categorizes patients into a "High Priority Isolation Wing" or a "Normal Ward" based on a **user-defined safety ceiling**.
* **Embedded Resource Constraints:** Models a real-world hospital bottleneck by tracking maximum bed capacities. If critical patients exceed available beds, the software safely triggers a defensive deployment halt to signal an operational overflow.
* **Interactive UI/UX Dashboard:** Built a clean, professional multi-column dashboard featuring live operational metrics, system state cards, and structured JSON data views.

---

## 🛠️ Tech Stack & Concepts Explored

* **Language:** Python 3
* **Framework:** Streamlit (UI & Cloud Deployment)
* **Version Control:** Git & GitHub Codespaces
* **Computer Science Concepts:** Control flow logic, nested conditional statements, array parsing, error handling (defensive programming), and resource constraint algorithms.
* **Healthcare Concepts:** Patient flow tracking, PHI protection logic, triage tiering, and medical dosage threshold compliance.

---

## 📈 Context & Inspiration (Why I Built This)
In modern healthcare systems, **Patient Flow and Capacity Management** are critical to saving lives. When Intensive Care Units (ICUs) or Emergency Departments bottleneck, it leads to overcrowding and delayed care. 

While commercial Electronic Health Record (EHR) integrations (like Epic or Cerner) use complex database communication protocols like FHIR, this simulator serves as a high-level proof-of-concept. It demonstrates how conditional logic and software constraints can be leveraged to optimize resource allocation during high-intake hospital shifts.

---

## 🚀 How to Run locally

If you would like to run this simulation repository on your local machine:

1. Clone the repository:
   ```bash
   git clone [https://github.com/](https://github.com/)[YOUR-GITHUB-USERNAME]/[YOUR-REPO-NAME].git
