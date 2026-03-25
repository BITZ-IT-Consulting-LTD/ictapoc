# PART 1: EXECUTIVE SUMMARY

The refined process for the State Department for Livestock Development (SDLD) focuses on the digital transformation of regulatory and quality assurance workflows. Beyond practitioner licensing, this iteration embeds **Milk Quality Analysis** and **Structured Inspection Frameworks** into the national livestock data ecosystem. 

Key improvements include:
- **Renewable License Management:** A full-lifecycle approach for veterinary practitioners and facilities, moving away from "one-off" issuance to continuous compliance monitoring.
- **Evidence-Based Inspections:** Replacement of handwritten reports with structured, geo-tagged digital inspection data.
- **New Quality Assurance Stream:** Modelling of the monthly **Milk Analysis Workflow** (14th–15th monthly cycle) to ensure dairy safety and farmer accountability.
- **Systemic Validation:** Integration of practice location validation and mandatory document uploads via eCitizen to ensure legal and operational traceability.

---

# PART 2: UPDATED LICENSING & INSPECTION PROCESS

The licensing lifecycle is refactored as a **Decision-Support System** anchored on the National Livestock Digital Registry (NLDR).

### Refined TO-BE Steps (Digital)

| Step | Actor | Action | System / Component |
|---|---|---|---|
| **1** | Applicant | **Submission:** Logs into eCitizen, selects service, and **uploads supporting documents** (Certificates, Logbooks). | eCitizen / IDP |
| **2** | SDLD Officer | **Location Validation:** Verification of the physical practice location/facility via GIS mapping. | GIS Engine / NLDR |
| **3** | System (KeSEL) | **Registration Check:** Automated verification against KVB (Veterinary Board) and Pharmacy & Poisons Board APIs. | KeSEL / X-Road |
| **4** | Field Inspector | **Structured Inspection:** Conducts field visit using a **Digital Checklist** (No handwritten reports allowed). | Mobile Inspection App |
| **5** | Director (DVS) | **Approval:** Final review of structured inspection data and geo-location proofs. | Workflow Engine |
| **6** | System | **Issuance & Renewal Setup:** Generates QR-coded license and sets automated 90-day renewal reminders. | NLDR / Notifications |

---

# PART 3: NEW MILK ANALYSIS PROCESS (QUALITY ASSURANCE)

This process tracks milk safety from the farm gate to the laboratory, occurring on a **Monthly Schedule (14th–15th of every month)**.

| Stage | Activity | Data Points | Actor |
|---|---|---|---|
| **1. Identification** | **Farmer & Farm Registration:** Linking the milk source to a unique farmer ID and farm location. | Maisha Namba, Farm GPS, NLDR ID | County Extension Officer |
| **2. Animal Registry** | **Batch Tracking:** Identifying the specific animal/herd from which the sample is drawn. | Animal ID / RFID Tag | Extension Officer |
| **3. Collection** | **Protocol-Based Sampling:** Collection of milk samples using standardized digital batch codes. | Timestamp, Sample ID, Temp | Lab Assistant |
| **4. Lab Testing** | **Analysis & Results Entry:** Laboratory testing for contaminants, butterfat, and bacterial count. | Lab Results, Rejection Codes | Lab Technician |
| **5. Reporting** | **Automated Feedback:** Sending results to the farmer via SMS/App and updating the national dairy dashboard. | Quality Score, Alert | National Dairy Board |

---

# PART 4: POLICY & REGULATORY ALIGNMENT

The livestock regulatory framework is governed by the following critical instruments:

- **Animal Health Act (Cap. 360):** Governing disease control and animal movement.
- **Veterinarians and Veterinary Para-Professionals Act (Cap. 366):** Professional licensing authority.
- **Meat Control Act (Cap. 356):** Standards for slaughterhouse operations.
- **Pharmacy and Poisons Act (Cap. 244):** Regulation of veterinary medicines and practitioner drug-handling licenses.
- **Dairy Industry Act:** Foundation for the Milk Analysis and Quality Assurance process.

---

# PART 5: CHANGE LOG

| Area | Original Issue | Change Made | Impact |
|---|---|---|---|
| **Licensing** | Missing document upload stage. | Added "Upload Supporting Documents" after service selection. | Improved completeness and documentation audit trail. |
| **Inspection** | Handwritten/Unstructured reports. | Mandated **Structured Digital Reports** via mobile app. | Standardized compliance scoring and real-time dashboarding. |
| **Lifecycle** | Focused on one-time issuance. | Included **Renewable License Lifecycle** management. | Continuous oversight of practitioner compliance. |
| **QA Scope** | Missing dairy quality workflows. | Modeled the **Monthly Milk Analysis Process**. | Enhanced food safety and dairy sector traceability. |
| **Validation** | Generic application check. | Added **Practice Location (GIS) Validation**. | Verified operational presence and facility standards. |

---

## References
- https://kilimo.go.ke
- Animal Health Act / Pharmacy and Poisons Act
- Kenya Digital Justice Program Roadmap
- Data Protection Act 2019

---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)
