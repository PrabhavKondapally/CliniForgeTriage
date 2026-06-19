# CliniForge Triage (v 2.1)

An interactive clinical workflow simulation developed in Python and Streamlit for modeling patient prioritization, capacity-aware room allocation, and dynamic patient redistribution under configurable operating constraints.

🌐 **Live Application:** https://cliniforgetriage.streamlit.app

> **Disclaimer:** CliniForge is an educational software project designed for demonstration and learning purposes. It is **not** intended for clinical deployment, diagnosis, treatment, or medical decision support.

---
<img width="1917" height="863" alt="image" src="https://github.com/user-attachments/assets/8648725d-dbbe-488a-b8d7-d55ca4219923" />
<img width="1918" height="867" alt="image" src="https://github.com/user-attachments/assets/7af5a3ba-5ad3-4035-8ae8-be9af1f7ee7b" />
<img width="1918" height="867" alt="image" src="https://github.com/user-attachments/assets/1b4f5077-516d-44d9-8982-3ad03c4f7f4d" />
<img width="1918" height="868" alt="image" src="https://github.com/user-attachments/assets/d00c6a51-2419-4bca-adbb-b8e141b52df5" />




## Overview

CliniForge Triage provides a configurable environment for simulating patient allocation and redistribution within a simplified hospital workflow. The application emphasizes software architecture, state management, algorithmic decision-making, and interactive user experience through a healthcare-inspired use case.

The project is designed to demonstrate practical programming concepts while maintaining a professional and intuitive interface for experimentation and visualization.

---

## Core Functionality

### Patient Intake

* Register new patients through an interactive dashboard
* Automatic assignment of unique patient identifiers
* Configurable dosage-based triage thresholds
* Real-time room assignment upon admission

### Dynamic Redistribution

* Automatic reassessment following dosage updates
* Configurable high-priority bed capacity
* Threshold-driven promotion and demotion logic
* Persistent state management across application pages

### High-Priority Waitlist

* Automatic overflow handling when capacity is exceeded
* Hybrid prioritization model:

  * Primary ranking by dosage
  * Secondary ranking by arrival order
* Automatic promotion when capacity becomes available

### Dashboard Interface

* Multi-page navigation
* Real-time room visualization
* Interactive patient management
* Configurable operational parameters

### Authentication & Access Control

* Secure Firebase Authentication integration
* Email/password account creation and login
* Protected access to application pages
* User-specific account identification via Firebase UID
* Foundation for future cloud-based persistence

---

## System Design

```text
                  +----------------+
                  |  New Patient   |
                  +-------+--------+
                          |
                          v
                 Dosage > Threshold?
                    /            \
                  Yes             No
                  |               |
                  v               v
        High Priority        Normal Room
             |
             | Capacity Full
             v
      High Priority Waitlist
             |
             | Bed Available
             v
        High Priority Room
```

Patient redistribution is performed dynamically as operating parameters or patient attributes change, ensuring that assignments remain consistent with current system constraints.

---

## Technical Stack

* Python
* Streamlit
* Firebase Authentication
* Firestore (cloud persistence foundation)
* Session State Management
* Custom redistribution algorithms
* Dynamic UI rendering


---

## Repository Structure

```text
CliniForgeTriage/
│
├── app.py
├── firebase_auth.py
├── firebase_config.py
├── pages/
│   ├── Login.py
│   ├── Patient_Triage.py
│   ├── Chart_Review.py
│   └── Session_Info.py
├── cliniforge_logo.png
├── CliniForgeBanner.png
└── README.md

```

---

## Development Roadmap

Planned enhancements include:

* CSV-based patient import/export
* Statistical summaries and reporting
* Interactive data visualization
* Cloud-based patient persistence
* Historical patient activity tracking
* Expanded chart review capabilities
* Clinical analytics dashboard
* Multi-user cloud synchronization

---

## Design Philosophy

CliniForge has been developed through iterative refinement, with new functionality added as workflow requirements evolved. The project prioritizes maintainability, modular design, and transparent system behavior over unnecessary complexity.

Its objective is not to replicate a production electronic health record system, but to explore how software engineering principles—including state management, algorithm design, and user-centered interface development—can be applied to healthcare-inspired operational problems.

---

## License

This project is licensed under the **MIT License**.

Please refer to the `LICENSE` file included in this repository for the complete license text.
