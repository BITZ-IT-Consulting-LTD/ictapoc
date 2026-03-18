# ICT Authority (ICTA)
## Business Process Mapping Report

### Ministry of Information, Communications and The Digital Economy
### ICT Authority

## 1. Overview

The ICT Authority (ICTA) is a State Corporation established under Legal Notice 183 of August 2013 by merging Government Information Technology Services (GITS), Directorate of e-Government (DeG), and Kenya ICT Board (KICTB). ICTA enforces ICT standards in government, manages national digital infrastructure, operates the Government Data Centre, manages NPKI certification, and promotes digital literacy, innovation, and enterprise.

| Attribute | Description |
|-----------|-------------|
| Key Actors | MDAs, County Governments, ICT Officers, Innovators, Citizens, System Administrators |
| Key Systems | Government Data Centre, NOFBI, Government Common Core Network (GCCN), eCitizen (policy oversight), NPKI Government CA |
| Key Programmes | Digital Literacy Programme (DLP), County Connectivity Project, KDEAP (World Bank), Connected Africa Summit |

## 2. Services

### Process 1: Government ICT Standards Enforcement
- Receive MDA ICT project proposals
- Assess compliance with ICTA standards and guidelines
- Issue compliance certificates or corrective directives
- Monitor MDA implementation of ICT standards

### Process 2: Government Data Centre Services
- Receive hosting requests from MDAs
- Assess technical requirements and capacity
- Provision virtual infrastructure and cloud services
- Monitor service availability and performance
- Manage backups and disaster recovery

### Process 3: NPKI Digital Certificate Issuance
- Receive digital certificate application from MDA
- Verify applicant identity and authorization
- Generate and issue digital certificate
- Manage certificate lifecycle (renewal, revocation)

### Process 4: NOFBI Connectivity and Last Mile
- Receive connectivity request from institution
- Assess site location against NOFBI backbone
- Design last mile connection via KPLC infrastructure
- Install and commission fibre link
- Hand over to institution and begin monitoring

### Process 5: ICT Innovation Support
- Receive innovation ideas from public
- Evaluate viability and scalability
- Provide technical assistance and mentorship
- Link to investors, hubs, and accelerators
- Introduce viable innovations to government for adoption

## 3. Diagrams

### 3.1 Government ICT Standards Enforcement

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["MDA Submits ICT Project Proposal"]:::task
    T2["Log Proposal and Assign Reference"]:::task
    T3["Assign Standards Review Officer"]:::task
    T4["Review Against ICTA Standards"]:::task
    T5["Check Infrastructure Alignment with GCCN"]:::task
    T6["Verify Security Compliance"]:::task

    GW1{"× Compliant?"}:::gateway
    T7["Issue Corrective Recommendations"]:::task
    T8["MDA Revises and Resubmits"]:::task
    T9["Issue Compliance Certificate"]:::task
    T10["Register in Standards Registry"]:::task

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> T5
    T5 --> T6
    T6 --> GW1
    GW1 -->|Non-Compliant| T7
    T7 --> T8
    T8 --> T4
    GW1 -->|Compliant| T9
    T9 --> T10
    T10 --> ENDEV
```

### 3.2 Government Data Centre Hosting

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["MDA Submits Hosting Request"]:::task
    T2["Assess Technical Requirements"]:::task
    T3["Check GDC Capacity"]:::task

    GW1{"× Capacity Available?"}:::gateway
    T4["Notify Capacity Unavailable"]:::task

    T5["Prepare Service Level Agreement"]:::task
    T6["MDA Signs SLA"]:::task
    T7["Provision Virtual Infrastructure"]:::task
    T8["Configure Security and Firewall"]:::task
    T9["Deploy MDA Application"]:::task
    T10["Conduct Testing"]:::task

    GW2{"× Tests Passed?"}:::gateway
    T11["Resolve Issues and Retest"]:::task

    T12["Activate Service"]:::task
    T13["Begin Monitoring via NOC"]:::task

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> GW1
    GW1 -->|No| T4
    T4 --> ENDEV
    GW1 -->|Yes| T5
    T5 --> T6
    T6 --> T7
    T7 --> T8
    T8 --> T9
    T9 --> T10
    T10 --> GW2
    GW2 -->|Fail| T11
    T11 --> T10
    GW2 -->|Pass| T12
    T12 --> T13
    T13 --> ENDEV
```

### 3.3 NPKI Digital Certificate Issuance

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["MDA Submits Certificate Application"]:::task
    T2["Verify Applicant Identity"]:::task
    T3["Verify Authorization from MDA Head"]:::task

    GW1{"× Verified?"}:::gateway
    T4["Reject - Return for Verification"]:::task

    T5["Generate Key Pair"]:::task
    T6["Create Digital Certificate"]:::task
    T7["Sign with Government CA Key"]:::task
    T8["Issue Certificate to Applicant"]:::task
    T9["Register in Certificate Registry"]:::task
    T10["Set Renewal Reminder"]:::task

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> GW1
    GW1 -->|No| T4
    T4 --> T1
    GW1 -->|Yes| T5
    T5 --> T6
    T6 --> T7
    T7 --> T8
    T8 --> T9
    T9 --> T10
    T10 --> ENDEV
```

### 3.4 NOFBI Connectivity and Last Mile

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["Receive Connectivity Request"]:::task
    T2["Survey Site Location"]:::task
    T3["Assess Proximity to NOFBI Backbone"]:::task

    GW1{"× Within Reach?"}:::gateway
    T4["Flag for Future Phase"]:::task

    T5["Design Last Mile Route via KPLC"]:::task
    T6["Procure Materials and Equipment"]:::task
    T7["Install Fibre Optic Cable"]:::task
    T8["Install OLT at DCC Location"]:::task
    T9["Commission and Test Link"]:::task

    GW2{"× Tests Passed?"}:::gateway
    T10["Troubleshoot and Retest"]:::task

    T11["Handover to Institution"]:::task
    T12["Begin NOC Monitoring"]:::task

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> GW1
    GW1 -->|No| T4
    T4 --> ENDEV
    GW1 -->|Yes| T5
    T5 --> T6
    T6 --> T7
    T7 --> T8
    T8 --> T9
    T9 --> GW2
    GW2 -->|Fail| T10
    T10 --> T9
    GW2 -->|Pass| T11
    T11 --> T12
    T12 --> ENDEV
```

### 3.5 End-to-End ICTA Services

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    GW1{"× Service?"}:::gateway

    T1["ICT Standards Enforcement"]:::task
    T2["Data Centre Hosting"]:::task
    T3["NPKI Certificate Issuance"]:::task
    T4["NOFBI Connectivity"]:::task
    T5["Innovation Support"]:::task

    T6["Standards Certified"]:::task
    T7["Service Provisioned"]:::task
    T8["Certificate Issued"]:::task
    T9["Site Connected"]:::task
    T10["Innovation Supported"]:::task

    GW_MERGE{"× Merge"}:::gateway
    T11["Registry Updated"]:::task

    ENDEV(("●")):::startEnd

    START --> GW1
    GW1 -->|Standards| T1
    GW1 -->|Hosting| T2
    GW1 -->|NPKI| T3
    GW1 -->|Connectivity| T4
    GW1 -->|Innovation| T5

    T1 --> T6
    T2 --> T7
    T3 --> T8
    T4 --> T9
    T5 --> T10

    T6 --> GW_MERGE
    T7 --> GW_MERGE
    T8 --> GW_MERGE
    T9 --> GW_MERGE
    T10 --> GW_MERGE

    GW_MERGE --> T11
    T11 --> ENDEV
```

## 4. BPMN Legend

| Symbol | Meaning |
|--------|---------|
| ((○)) | Start Event |
| ((●)) | End Event |
| [Text] | Task/Activity |
| {×} | Exclusive Gateway - One path only |
| --> | Sequence Flow |
| -.-> | Loop Back / Return Flow |
