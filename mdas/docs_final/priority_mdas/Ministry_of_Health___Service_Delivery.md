# MINISTRY OF HEALTH – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** MINISTRY OF HEALTH
- **Process Name:** Health Information Exchange
- **Document Version:** 2.1
- **Date:** 2026-03-04
- **Classification:** Official
- **Strategic Category:** Priority MDA
- **Service Model:** G2C
- **Life-Cycle Group:** Cradle to Death (1. The Cradle)

## Service Mandate
The Ministry of Health’s (MoH) primary mandate is to build a progressive, responsive, and sustainable healthcare system to ensure all Kenyans attain the highest standard of health, as enshrined in the Constitution of Kenya 2010. Following the devolution of government in 2013, the Ministry’s role is structured around four core pillars:
1. **Health Policy:** Formulating national policies, standards, and guidelines.
2. **Health Regulation:** Oversight of health services, professionals, and products.
3. **National Referral Facilities:** Management of tertiary hospitals (e.g., Kenyatta National Hospital, Moi Teaching and Referral Hospital).
4. **Capacity Building & Technical Assistance:** Supporting the 47 County Governments, which are responsible for direct service delivery.
Core Functions include:
* **Preventive & Promotive Health:** Disease surveillance, immunization, and public health education.
* **Curative Services:** Oversight of clinical standards and specialized treatment.
* **Sanitation & Food Safety:** Policy and inspection for environmental health and food handling.
* **Health Research:** Coordinating research through agencies like KEMRI.
* **Universal Health Coverage (UHC):** Implementing reforms such as the Social Health Authority (SHA) to ensure affordable access to care.

---

## Executive Summary
The Ministry of Health plays a foundational role in the citizen lifecycle. Current health systems are highly fragmented, leading to poor patient experiences with multiple hospital-specific IDs and incomplete medical histories. The transition to the Kenya Health Information Exchange (KHIE) Architecture and a Shared Health Record (SHR) aims to unify patient identities and care data across all facilities.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Fragmented Patient Identity based on Deep Dive).*

```mermaid
%%{init: { 'theme': 'base', 'themeVariables': { 'fontSize': '24px', 'fontFamily': 'Inter, system-ui, sans-serif', 'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#f3f3f3', 'mainBkg': '#ffffff', 'nodeBorder': '#333333' } } }%%
flowchart TD
    %% Events
    Start((Start))
    EndProcess(("End - Fragmented History"))

    subgraph Patient [Patient]
        direction LR
        Arrive1["Patient arrives at facility"]
        Consult1["Attends consultation"]
        Arrive2["Visits another facility"]
    end

    subgraph RegClerk["Registration Clerk"]
        direction TB
        RegPat["Registration occurs"]
        SearchRec["Facility searches local EMR"]
        RecGateway{"Patient record found?"}
        CreateNew["New patient ID created"]
        AssignID["Local facility ID created"]
    end

    subgraph Clinician [Clinician]
        direction TB
        Triage["Triage and consultation"]
        Labs["Lab tests and prescriptions"]
        RecEnc["Record encounter"]
        DupRec["Duplicate clinical records created"]
    end

    subgraph FacEMR["Facility EMR"]
        direction TB
        StoreLoc["Data stored in facility EMR"]
    end

    %% Flow connections
    Start --> Arrive1
    Arrive1 --> RegPat
    RegPat --> AssignID
    AssignID --> Consult1
    Consult1 --> Triage
    Triage --> Labs
    Labs --> RecEnc
    RecEnc --> StoreLoc
    
    StoreLoc --> Arrive2
    Arrive2 --> SearchRec
    SearchRec --> RecGateway
    
    RecGateway -- "Yes" --> Triage
    RecGateway -- "No" --> CreateNew
    CreateNew --> DupRec
    
    DupRec --> EndProcess

    %% Styling
    classDef startEvent fill:#27ae60,stroke:#27ae60,color:#fff,font-size:24px,font-size:24px;;
    classDef endEvent fill:#e74c3c,stroke:#e74c3c,color:#fff,font-size:24px,font-size:24px;;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff,font-size:24px,font-size:24px;;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff,font-size:24px,font-size:24px;;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333,font-size:24px,font-size:24px;;
    
    class Start startEvent;
    class EndProcess endEvent;
    class RecGateway gateway;
    class StoreLoc serviceTask;
    class Arrive1,Consult1,Arrive2,RegPat,SearchRec,CreateNew,AssignID,Triage,Labs,RecEnc,DupRec userTask;
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
| 1 | Patient | Patient arrives at facility. | Physical | |
| 2 | Registration Clerk | Registration occurs and a local facility ID is created. | Paper/Local EMR | |
| 3 | Clinician | Performs triage and consultation, followed by lab tests and prescriptions. | Local EMR | |
| 4 | Clinician | Records the clinical encounter. | Local EMR | |
| 5 | Facility EMR | Data is stored in the facility EMR. | Local EMR | Data remains siloed. |
| 6 | Patient | Patient visits another facility for further care. | Physical | |
| 7 | Registration Clerk | Facility searches local EMR for the patient's record. | Local EMR | |
| 8 | Registration Clerk | No record found. A new patient ID is created at the second facility. | Local EMR | Identity becomes fragmented. |
| 9 | Clinician | Duplicate clinical records created without visibility into previous history. | Local EMR | Results in fragmented medical history and duplicate testing. |

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
%%{init: { 'theme': 'base', 'themeVariables': { 'fontSize': '24px', 'fontFamily': 'Inter, system-ui, sans-serif', 'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#f3f3f3', 'mainBkg': '#ffffff', 'nodeBorder': '#333333' } } }%%
flowchart TD
    %% Events
    Start((Start))
    EndProcess(("End - Claims Processed"))

    subgraph Patient [Patient]
        direction LR
        PresentID["Present ID"]
    end

    subgraph HealthWorker["Health Worker"]
        direction TB
        IdPat["Identify patient"]
        Consult["Clinical consultation"]
        RecEnc["Record encounter"]
    end

    subgraph FacEMR["Facility EMR"]
        direction TB
        QueryMPIReq["Query MPI"]
        PushKHIE["Push encounter to KHIE"]
    end

    subgraph KHIE["KHIE Platform"]
        direction TB
        MPIGateway{"Patient found in MPI?"}
        AuthGateway{"Access authorized?"}
        RetSHR["Retrieve Shared Health Record"]
        UpdateSHR["Update Shared Health Record"]
    end

    subgraph NatReg["National Registries"]
        direction TB
        QueryMPI["Master Patient Index"]
        SHR["Shared Health Record"]
        Claims["Trigger claims processing"]
    end

    %% Flow connections
    Start --> PresentID
    PresentID --> IdPat
    IdPat --> QueryMPIReq
    QueryMPIReq --> QueryMPI
    QueryMPI --> MPIGateway
    
    MPIGateway -- "No" --> IdPat
    MPIGateway -- "Yes" --> AuthGateway
    
    AuthGateway -- "No" --> IdPat
    AuthGateway -- "Yes" --> RetSHR
    
    RetSHR --> SHR
    SHR --> Consult
    Consult --> RecEnc
    RecEnc --> PushKHIE
    PushKHIE --> UpdateSHR
    UpdateSHR --> SHR
    UpdateSHR --> Claims
    
    Claims --> EndProcess

    %% Styling
    classDef startEvent fill:#27ae60,stroke:#27ae60,color:#fff,font-size:24px,font-size:24px;;
    classDef endEvent fill:#e74c3c,stroke:#e74c3c,color:#fff,font-size:24px,font-size:24px;;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff,font-size:24px,font-size:24px;;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff,font-size:24px,font-size:24px;;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333,font-size:24px,font-size:24px;;
    
    class Start startEvent;
    class EndProcess endEvent;
    class MPIGateway,AuthGateway gateway;
    class QueryMPIReq,PushKHIE,RetSHR,UpdateSHR,QueryMPI,SHR,Claims serviceTask;
    class PresentID,IdPat,Consult,RecEnc userTask;
```

## Future State Process (TO-BE)
### Narrative
**TO-BE Process: Kenya Health Information Exchange (KHIE)**

**Design Principles:**
- **Patient-Centric Identity:** Relying on IPRS/Maisha Namba via the Huduma Bridge to eliminate duplicate profiles.
- **Data Liquidity:** X-Road-based interoperability to allow secure exchange of clinical summaries, lab results, and prescriptions across all accredited facilities.
- **Automated Claims:** Seamless integration with the Social Health Authority (SHA) for real-time claims and coverage checks.

**Core National Components:**
- **Master Patient Index (MPI):** Central registry for unique patient identification.
- **Shared Health Record (SHR):** Centralized clinical repository for continuity of care.
- **Health Information Exchange (HIE):** Interoperability layer for secure data sharing.
- **Facility Registry:** Authoritative source for health facilities.
- **Provider Registry:** Authoritative source for healthcare workers.

### Optimized Steps (Digital)

| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Health Worker | Patient identified using Maisha Namba or biometrics. | Facility EMR |
| 2 | Facility EMR | Facility system queries Master Patient Index (MPI) to locate the patient's unified profile. | KHIE MPI / X-Road |
| 3 | KHIE Platform | Patient profile retrieved. System retrieves Shared Health Record (SHR) upon authorization. | KHIE SHR / X-Road |
| 4 | Clinician | Clinician performs consultation with access to unified history, lab results, and medications. | Facility EMR |
| 5 | Clinician | Encounter recorded, including treatments and e-prescriptions. | Facility EMR |
| 6 | Facility EMR | Data shared via HIE (pushed to KHIE platform). | KHIE API Gateway |
| 7 | KHIE Platform | Updates the national Shared Health Record (SHR) immediately with new encounter data. | KHIE SHR |
| 8 | National Registries | Claims triggered for Social Health Authority (SHA) based on the recorded encounter. | Govt Payment Aggregator / SHA |

---

## References
- https://www.health.go.ke
- Digital Health Act 2023
- Desk Review

---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)

