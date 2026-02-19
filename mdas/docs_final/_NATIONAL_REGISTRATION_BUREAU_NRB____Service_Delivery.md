# ·       NATIONAL REGISTRATION BUREAU (NRB) – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** ·       NATIONAL REGISTRATION BUREAU (NRB)
- **Process Name:** Service Delivery (National Identity Card Registration)
- **Document Version:** 1.2
- **Date:** 2026-02-19
- **Classification:** Official

---

## Executive Summary
The National Registration Bureau (NRB) is responsible for the identification and registration of all Kenyans who have attained the age of 18 years. It issues the National Identity Card (ID), which is the primary document for accessing all government and private services (banking, voting, travel).

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Semi-Manual / Fingerprint Intensive).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Citizen turning 18]
        S1["Attains age of 18"]
        S2["Visits Chief/Assistant Chief for Introduction"]
        S3["Visits NRB Office / Huduma Centre"]
        S6["Waits for SMS Notification (2-6 months)"]
        S7["Collects ID Card"]
    end
    subgraph Chief [Chief / Assistant Chief]
        S2a["Vets Applicant & Parents"]
        S2b["Signs Introduction Letter"]
    end
    subgraph NRBOfficer [Registration Officer]
        S4["Vets Documents (Birth Cert, Parent IDs)"]
        S5["Captures Biometrics (Fingerprints) & Photo"]
        S5a["Fills Form 136A (Manual/Digital)"]
    end
    subgraph ProductionCentre [NRB HQ - Nairobi]
        S5b["Receives Batch"]
        S5c["Quality Assurance & AFIS Check"]
        S5d["Prints Card"]
        S5e["Dispatches to Station"]
    end
    
    S1 --> S2
    S2 --> S2a
    S2a --> S2b
    S2b --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S5a
    S5a --> S5b
    S5b --> S5c
    S5c --> S5d
    S5d --> S5e
    S5e --> S6
    S6 --> S7
    S7 --> End((End))
```

---

## Process Overview
### Process Name
National Identity Card Registration (New Application & Replacement)

### Service Category
- G2C (Government to Citizen)

### Scope
- **In Scope:** Registration of Kenyans at 18; Replacement of Lost/Damaged IDs; Change of Particulars.
- **Out of Scope:** Passport issuance (Immigration); Alien ID (Immigration).

### Triggers
- Citizen turning 18 years old.
- Loss or damage of existing ID.

### End States
- **Successful:** Issuance of 2nd Generation (or Maisha) ID Card.

### Policy Context
- Registration of Persons Act (Cap 107).

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Applicant | Presents self for registration with required documents. |
| Chief / Assistant Chief | Vetting Authority | Confirms applicant is a resident/citizen of the area. |
| NRB Registration Officer | Processor | Vets documents, captures biometrics (Live Scan/Ink). |
| Fingerprint Expert (HQ) | Analyst | Compares fingerprints against database (AFIS). |
| Production Centre | Issuer | Prints and personalizes the ID card. |

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | **Preparation:** Obtains parents' ID copies and Birth Certificate. | Manual | Mandatory documents. |
| 2 | Chief / Assistant Chief | **Vetting:** Visits the local administrator for verification of village of origin. Chief signs the introduction letter. | Manual Letter | Crucial for border counties to prevent illegal registration. |
| 3 | Applicant | **Application:** Visits the NRB office (Registrar of Persons) or Huduma Centre. | Manual Queue | Long queues common. |
| 4 | NRB Officer | **Data Capture:** Officer verifies documents against originals. Captures 10 fingerprints (digital scanner or ink pad) and photo. Fills Form 136A. | Live Scan Kit / Form 136A | Connectivity issues often force fallback to manual forms. |
| 5 | NRB HQ | **Processing:** Data transmitted to HQ (Nairobi). 
- **AFIS:** Automated Fingerprint Identification System checks for duplicates. 
- **Production:** Card is printed. | AFIS / Production Machines | Backlogs occur frequently due to material shortages or system downtime. |
| 6 | Logistics | **Dispatch:** Cards are batched and sent back to the district registrar. | Physical Courier | Delays in transport to remote areas. |
| 7 | Applicant | **Collection:** Applicant receives SMS (sometimes), visits office to collect card. | Physical Logbook | Uncollected IDs pile up at offices. |

---

## Pain Points & Opportunities
### Pain Points
- **Turnaround Time:** Takes months (sometimes >6 months) to get the ID.
- **Centralized Production:** All cards printed in Nairobi, creating a bottleneck.
- **Manual Dependencies:** Reliance on Chief's letter is prone to corruption/bribery.
- **Lost Applications:** Manual forms (136A) sometimes get lost in transit to HQ.
- **Retakes:** Poor quality fingerprints require the applicant to return and redo the process.

### Opportunities
- **Decentralized Printing:** Print IDs at County/Regional level.
- **Digital Vetting:** Integrate with Birth Certificate database (CRS) to auto-verify citizenship, removing Chief's letter for straightforward cases.
- **Online Application:** Allow pre-filling of biodata on eCitizen to reduce time at the desk.
- **Maisha Namba:** Transition to digital ID (UPI) issued at birth, upgrading to biometric at 18 without re-vetting.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Repeatable WoG Platform).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph WoG_Platform [Identity Service]
        S1["Fetches Citizen UPI from Birth Record (CRS via X-Road)"]
        S2["Auto-Verifies Age (18+)"]
        S3["Pre-Fills Maisha Namba Upgrade Form"]
    end
    subgraph Citizen [Applicant]
        S4["Logs into eCitizen App"]
        S5["Selects 'Upgrade to Adult ID'"]
        S6["Self-Captures Photo (ICAO Standard)"]
        S7["Visits Biometric Hub (only for fingerprints)"]
    end
    subgraph NRB_System [Biometric Registry]
        S8["Captures & Validates Fingerprints (AFIS Real-time)"]
        S9["Issues Virtual ID to App"]
        S10["Queues Physical Card (Optional)"]
    end
    
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> S9
    S9 --> S10
    S10 --> End((End))
```

## Future State Process (TO-BE)
### Narrative
The process is **Seamless** and **Digital-First**.
1.  **UPI Continuity:** The citizen's UPI (Maisha Namba) from birth is reused. No new application is needed, just an "Upgrade".
2.  **Auto-Vetting:** The platform verifies citizenship via the **IPRS/CRS Link**. Chief's letters are only required for exceptional cases (e.g., late registration without birth cert).
3.  **Self-Service:** Photo and bio-data updates are done via the **eCitizen App**.
4.  **Virtual ID:** A digital ID is issued instantly upon biometric capture to the citizen's secure wallet.
5.  **Decentralized Printing:** Physical cards (if requested) are printed at regional hubs or delivered via courier (Posta).

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Citizen | Upgrades status to "Adult" on eCitizen App. | eCitizen / Maisha |
| 2 | WoG Platform | Auto-verifies birth record via X-Road. | IPRS / CRS |
| 3 | Citizen | Visits local hub for quick fingerprint scan. | Biometric Kit |
| 4 | NRB System | Issues Virtual ID instantly. | Maisha Wallet |

---

## References
- Registration of Persons Act.
