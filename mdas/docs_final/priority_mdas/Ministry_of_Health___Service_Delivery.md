# MINISTRY OF HEALTH – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** MINISTRY OF HEALTH
- **Process Name:** Health Information Exchange
- **Document Version:** 2.1
- **Date:** 2026-02-24
- **Classification:** Official

---

## Executive Summary
The Ministry of Health plays a foundational role in the citizen lifecycle. Current health systems are highly fragmented, leading to poor patient experiences with multiple hospital-specific IDs and incomplete medical histories. The transition to the Kenya Health Information Exchange (KHIE) Architecture and a Shared Health Record (SHR) aims to unify patient identities and care data across all facilities.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Fragmented Patient Identity based on Deep Dive).*

```mermaid
graph TD
    Start((Start)) --> FacA["Patient Arrives at Facility A"]
    
    subgraph Facility_A [Facility A]
        FacA --> RegA["New Registration (Paper/Local EMR)"]
        RegA --> ID_A["Assign Local Facility ID"]
    end
    
    subgraph Facility_B [Facility B]
        ID_A --> FacB["Patient Arrives at Facility B"]
        FacB --> Search["Search Records"]
        Search --> NotFound["No Record Found"]
        NotFound --> RegB["New Registration B"]
        RegB --> ID_B["Assign New Facility ID"]
    end
    
    subgraph National_Level [MOH / National]
        ID_B --> Multiple["Multiple IDs Generated"]
        Multiple --> Fragmented["Fragmented Patient History"]
    end
    
    Fragmented --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    class Start start;
    class End endNode;
    class FacA,RegA,ID_A,FacB,Search,NotFound,RegB,ID_B,Multiple,Fragmented userTask;
```

---

## Process Overview
### Process Name
Health Service Delivery & Identity

### Service Category
- G2C (Government to Citizen)

### Scope
- **In Scope:** Patient registration, clinical encounters, and data aggregation across public and private health facilities.
- **Out of Scope:** Core hospital billing logic (managed locally).

### Triggers
- Patient arriving at a health facility for care.

### End States
- **Successful (Current):** Care is provided, but data remains siloed in local facility systems.

### Policy Context
- Digital Health Act 2023; Health Act 2017; Data Protection Act 2019.

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Patient | Arrives at Facility A. | Physical | |
| 2 | Registration Clerk | Creates a new patient file and assigns a local Facility A ID. | Paper/Local EMR | |
| 3 | Patient | Later visits a different facility (Facility B) for care. | Physical | |
| 4 | Registration Clerk | Searches for the patient in Facility B's system, finds no record. | Local EMR | |
| 5 | Registration Clerk | Creates another new patient file and assigns a new Facility B ID. | Paper/Local EMR | |
| 6 | MOH Systems | Patient ends up with multiple disconnected IDs across the health ecosystem, leading to fragmented medical history and duplicate testing. | Siloed Systems | |

---

## Pain Points & Opportunities
### Pain Points
- **Fragmented Identity:** Patients have different IDs at every hospital.
- **Data Silos:** Medical history, lab results, and prescriptions cannot be securely shared between facilities.
- **Incomplete Visibility:** The Ministry cannot view comprehensive public health data in real time.

### Opportunities
- **National KHIE Integration:** Deploying a central health exchange using the DSAP X-Road layer.
- **Unified Identity:** Leveraging Maisha Namba as the primary health identifier.
- **Shared Health Record (SHR):** Centralized clinical repository for continuity of care.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Kenya Health Information Exchange - KHIE Architecture).*

```mermaid
graph TD
    Start((Start)) --> Scan["Biometric Scan / Maisha Namba Input"]
    
    subgraph Point_Of_Care [Health Facility]
        Scan --> QueryReg["Query Master Patient Index"]
        QueryReg --> Found{"Found?"}
        Found -- "No" --> Enroll["Enroll New Patient"]
        Found -- "Yes" --> Retrieve["Retrieve Existing ID"]
        Enroll --> QuerySHR
        Retrieve --> QuerySHR["Query National Shared Health Record (SHR) via X-Road"]
        QuerySHR --> ViewHist["View Unified History (Meds, Labs)"]
        ViewHist --> Consult["Clinical Consultation"]
        Consult --> Encounter["Record Encounter"]
        Encounter --> eRx["e-Prescribe & Labs"]
    end
    
    subgraph Core_KHIE [National KHIE / Huduma Bridge]
        eRx --> Push["Push Data to KHIE via API Gateway"]
        Push --> Update["Update Central SHR"]
        Update --> Claims["Trigger SHA Claims Processing"]
    end
    
    Claims --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333;
    class Start start;
    class End endNode;
    class Found gateway;
    class Scan,QueryReg,Enroll,Retrieve,ViewHist,Consult,Encounter,eRx userTask;
    class QuerySHR,Push,Update,Claims serviceTask;
```

## Future State Process (TO-BE)
### Narrative
**TO-BE Process: Kenya Health Information Exchange (KHIE)**

**Design Principles:**
- **Patient-Centric Identity:** Relying on IPRS/Maisha Namba via the Huduma Bridge to eliminate duplicate profiles.
- **Data Liquidity:** X-Road-based interoperability to allow secure exchange of clinical summaries, lab results, and prescriptions across all accredited facilities.
- **Automated Claims:** Seamless integration with the Social Health Authority (SHA) for real-time claims and coverage checks.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Health Worker | Inputs Maisha Namba or captures biometrics to identify the patient upon arrival. | Facility EMR |
| 2 | Point of Care System | Queries the central Master Patient Index via X-Road to locate the patient's unified profile. | KHIE MPI / X-Road |
| 3 | Point of Care System | Pulls the patient's Shared Health Record (SHR), giving the clinician instant access to allergies, meds, and recent labs. | KHIE SHR / X-Road |
| 4 | Clinician | Conducts the consultation, records the encounter, and e-prescribes treatments. | Facility EMR |
| 5 | Core System | Pushes the encounter data back to the KHIE to update the SHR immediately. | KHIE API Gateway |
| 6 | Core System | Automatically triggers claims processing to the Social Health Authority (SHA) based on the recorded encounter. | Govt Payment Aggregator / SHA |

---

## References
- Digital Health Act 2023.
- Huduma Bridge DSAP Architecture.