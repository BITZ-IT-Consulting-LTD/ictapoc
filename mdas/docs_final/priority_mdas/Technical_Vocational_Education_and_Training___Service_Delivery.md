# PART 1: EXECUTIVE SUMMARY

The refined records management process for the State Department for TVET aligns with the **National ICT Policy (2019)**, **Government ICT Standards**, and **Electronic Records Management Standards**. This transformation shifts the department from a manual-heavy registry to a **digitally-indexed, workflow-driven environment**. 

Key objectives include:
- **Registry Modernization:** Reducing manual logging and stamping through digital ingestion and automated file tracking.
- **Legal Alignment:** Ensuring strict compliance with **KNADS (Kenya National Archives and Documentation Service)** protocols for record appraisal and disposal.
- **Operational Efficiency:** Integrating the **E-paper directive** to minimize physical document handling while maintaining a secure audit trail for all records, including **HR Personal Files**.
- **DPI Integration:** Linking with **IPRS** for identity verification and establishing a hybrid rollout for the **Electronic Document and Records Management System (EDRMS)**.

---

# PART 2: UPDATED RECORDS MODEL

The TVET records ecosystem is expanded to include specialized registries with standardized metadata:

### 2.1 HR Personal Files (Mandatory Registry)
All staff records must be maintained within the EDRMS with the following structure:
- **Unique Identifier:** Personal Number (e.g., P/No. 12345678).
- **Core Metadata:** Full Name, National ID (IPRS Verified), Designation, Grade, Date of First Appointment, Academic Qualifications.
- **File Structure:** Appointment Letter, Personal Details Form, Academic Certificates, Promotion Letters, Disciplinary Records (if any).

### 2.2 Institutional & Curriculum Records
- **TVET Provider Files:** Registration status, accreditation reports, and quality audits.
- **Curriculum & Assessment:** CDACC (Curriculum Development, Assessment and Certification Council) records, trade test results, and assessment frameworks.

---

# PART 3: REFINED PROCESS FLOW (TO-BE)

| Step | Actor | Action | System / Component |
|---|---|---|---|
| **1** | Registry Officer | **Digital Capture:** Records (Mails/Reports) are scanned and ingested with automated metadata tagging. | EDRMS / IDP |
| **2** | System | **Validation & Indexing:** Verification of staff/entity IDs via **IPRS** and automated numeric/alphanumeric classification. | KeSEL / IPRS Adapter |
| **3** | Registry Head | **Workflow Routing:** Digital marking of files to relevant Action Officers based on the File Plan. | Workflow Engine (BPMN) |
| **4** | Action Officer | **Active Use:** Referencing, updating, and adding digital minutes to the file. | EDRMS Workbench |
| **5** | System | **Tracking & Audit:** Real-time log of file access, movement, and edits (Audit Trail). | KDEAP Audit Service |
| **6** | Dispatch Officer | **Dispatch of Mails:** Digital or physical dispatch to MDAs and Stakeholders with automated log entry. | Dispatch Module |
| **7** | Records Manager | **Appraisal & Retention:** Automated alerts for semi-active records based on the Retention Schedule. | EDRMS Policy Engine |

---

# PART 4: COMPLIANCE & GOVERNANCE

### 4.1 KNADS & Legal Compliance
- **Disposal Authority:** No record (physical or digital) shall be destroyed without written approval from **KNADS** (Public Archives Act Cap. 19).
- **Metadata Schemas:** Adherence to government-wide schemas for interoperability during inter-agency file transfers.
- **Audit Trails:** Mandatory non-repudiation logs tracking every interaction with sensitive records (especially HR and Assessment files).

### 4.2 Capacity Building & Change Management
- **EDRMS Training:** Systematic upskilling of registry staff and action officers on digital filing and security.
- **Records Management Skills:** Training on the Data Protection Act 2019 and modern archival standards.
- **Executive Literacy:** Upskilling leadership on navigating digital registries for faster decision-making.

---

# PART 5: CHANGE LOG

| Area | Original Issue | Change Made | Impact |
|---|---|---|---|
| **Standards** | General reference to law. | Included **National ICT Policy (2019)** and **Electronic Records Standards**. | Alignment with modern government ICT frameworks. |
| **HR Records** | Not explicitly modeled. | Added **HR Personal Files** with **Personal Number** as unique ID. | Centralized and secure staff records management. |
| **Workflow** | Focus on receipt only. | Added **Dispatch of Mails to MDAs/Stakeholders**. | Complete end-to-end communication tracking. |
| **Manual Work** | High reliance on stamps. | Introduced **Digital Indexing & File Tracking**. | Reduced processing time and loss of physical files. |
| **Compliance** | Minimal detail on disposal. | Included **KNADS Approval** and **Audit Trail** requirements. | Legal protection and accountability in record disposal. |

---

## References
- National ICT Policy (2019)
- Public Archives and Documentation Service Act (Cap. 19)
- Data Protection Act 2019
- Government ICT Standards (ISO 15489 Alignment)

---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)

