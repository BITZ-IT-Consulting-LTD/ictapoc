# ICT Authority (ICTA) — TO-BE
## Business Process Mapping Report

### Ministry of Information, Communications and The Digital Economy
### ICT Authority

## 1. Overview

| Attribute | Description |
|-----------|-------------|
| Process Scope | Digital transformation of ICT standards enforcement, Government Data Centre, NPKI, NOFBI connectivity, and innovation support |
| Huduma Bridge Integration | eCitizen Portal, Kong API Gateway, Camunda Workflow Engine, KeSEL, GPA, NPKI, Government Data Centre |
| GEA Principles | Standards-Driven, Reuse and Modularity, Data as Strategic Asset, Security by Design |
| ICTA Role in Huduma Bridge | Operates Government CA (NPKI), manages GDC hosting, enforces ICT standards, operates NOFBI/GCCN backbone |

## 2. TO-BE Processes

### 2.1 TO-BE: Digital ICT Standards Enforcement

#### Key Transformation

| AS-IS | TO-BE |
|-------|-------|
| Paper-based MDA project proposals | Digital submission via Officer Workbench |
| Manual standards review | Automated compliance checks against ICTA standards registry |
| No GCCN alignment verification | Automated GCCN architecture alignment check |
| Paper compliance certificates | NPKI-signed digital compliance certificates |
| No post-issuance monitoring | Camunda-scheduled periodic compliance reviews |

#### Process Diagram

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    T1["MDA Submits ICT Project via Officer Workbench"]:::task
    T2["Kong API Gateway - Route to Standards Engine"]:::system
    T3["Assign Reference and Log in Registry"]:::system

    PG1{"+ Parallel Compliance Checks"}:::gateway
    T4["Auto-Check Against ICTA Standards Database"]:::system
    T5["Verify GCCN Architecture Alignment"]:::system
    T6["Verify Security Standards - ISO 27001"]:::system
    T7["Check Cloud Policy Compliance"]:::system
    PG1_END{"+ Sync"}:::gateway

    T8["Generate Compliance Score Report"]:::system

    GW1{"× Compliant?"}:::gateway
    T9["Issue Digital Corrective Recommendations"]:::task
    T10["MDA Revises and Resubmits"]:::task

    T11["Issue Compliance Certificate - NPKI Signed"]:::system
    T12["Register in Standards Registry"]:::system
    T13["Camunda - Schedule Periodic Review Timer"]:::system

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> PG1
    PG1 --> T4
    PG1 --> T5
    PG1 --> T6
    PG1 --> T7
    T4 --> PG1_END
    T5 --> PG1_END
    T6 --> PG1_END
    T7 --> PG1_END
    PG1_END --> T8
    T8 --> GW1
    GW1 -->|Non-Compliant| T9
    T9 --> T10
    T10 --> T3
    GW1 -->|Compliant| T11
    T11 --> T12
    T12 --> T13
    T13 --> ENDEV
```

### 2.2 TO-BE: Digital Government Data Centre Services

#### Key Transformation

| AS-IS | TO-BE |
|-------|-------|
| Manual hosting request by letter | Digital request via MDA Service Portal |
| Manual capacity assessment | Automated capacity dashboard with real-time metrics |
| Paper SLA signing | Digital SLA with NPKI signatures |
| Manual VM provisioning | Self-service VM provisioning with automated security config |
| Periodic manual monitoring | 24-7 NOC with automated alerting and incident management |

#### Process Diagram

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    T1["MDA Submits Hosting Request via Service Portal"]:::task
    T2["Auto-Assess Technical Requirements"]:::system
    T3["Check Real-Time GDC Capacity Dashboard"]:::system

    GW1{"× Capacity?"}:::gateway
    T4["Notify - Capacity Unavailable - Queue Request"]:::task

    T5["Generate Digital SLA"]:::system
    T6["MDA Signs SLA via NPKI"]:::system
    T7["Auto-Provision Virtual Infrastructure"]:::system
    T8["Auto-Configure Security and Firewall Rules"]:::system
    T9["Deploy MDA Application"]:::task
    T10["Run Automated Test Suite"]:::system

    GW2{"× Tests Passed?"}:::gateway
    T11["Auto-Generate Issue Report - Resolve and Retest"]:::task

    T12["Activate Service"]:::system
    T13["NOC Begins 24-7 Automated Monitoring"]:::system
    T14["GPA - Process Hosting Fee"]:::system

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> GW1
    GW1 -->|Unavailable| T4
    T4 --> ENDEV
    GW1 -->|Available| T5
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
    T13 --> T14
    T14 --> ENDEV
```

### 2.3 TO-BE: Digital NPKI Certificate Lifecycle

#### Key Transformation

| AS-IS | TO-BE |
|-------|-------|
| Paper certificate application | Digital application via secure MDA portal |
| Manual identity verification | KeSEL IPRS query for applicant identity |
| Manual key generation | Automated HSM-based key pair generation |
| Paper certificate delivery | Digital certificate delivery with secure download |
| Manual renewal tracking | Camunda timer events for auto-renewal reminders |

#### Process Diagram

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    T1["MDA Submits Certificate Request via Secure Portal"]:::task
    T2["KeSEL IPRS - Verify Applicant Identity"]:::system
    T3["Verify MDA Head Authorization - NPKI Signed"]:::system

    GW1{"× Verified?"}:::gateway
    T4["Reject - Return with Verification Requirements"]:::task

    T5["HSM - Generate Cryptographic Key Pair"]:::system
    T6["Create X.509 Digital Certificate"]:::system
    T7["Sign with Government CA Root Key"]:::system
    T8["Publish to Certificate Registry - OCSP Enabled"]:::system
    T9["Deliver Certificate via Secure Download"]:::system
    T10["Camunda - Set Renewal Timer 90 Days Before Expiry"]:::system

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

### 2.4 TO-BE: Digital NOFBI Connectivity

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    T1["Institution Submits Request via eCitizen"]:::task
    T2["GIS System - Auto-Survey Site Location"]:::system
    T3["Calculate Distance to Nearest NOFBI POP"]:::system

    GW1{"× Within Phase Coverage?"}:::gateway
    T4["Add to Future Phase Priority Queue"]:::task

    T5["Auto-Design Last Mile Route via KPLC GIS"]:::system
    T6["Generate Bill of Materials"]:::system
    T7["GPA - Process Connection Fee"]:::system
    T8["Dispatch Installation Team"]:::task
    T9["Install Fibre and OLT Equipment"]:::task
    T10["Run Automated Link Tests"]:::system

    GW2{"× Tests Passed?"}:::gateway
    T11["Troubleshoot and Retest"]:::task

    T12["Commission and Handover to Institution"]:::task
    T13["NOC - Activate Automated Monitoring"]:::system
    T14["Update National Connectivity Map"]:::system

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
    T13 --> T14
    T14 --> ENDEV
```

### 2.5 End-to-End ICTA Services

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    T_PORTAL["MDA Service Portal or eCitizen"]:::task
    T_KONG["Kong API Gateway - Route Request"]:::system

    GW1{"× Service?"}:::gateway

    T1["ICT Standards Enforcement"]:::task
    T2["GDC Hosting Services"]:::task
    T3["NPKI Certificate Lifecycle"]:::task
    T4["NOFBI Connectivity"]:::task
    T5["Innovation Support"]:::task

    T6["Parallel Compliance Checks"]:::system
    T7["Auto-Provision Infrastructure"]:::system
    T8["HSM Key Generation and Signing"]:::system
    T9["GIS Route Design and Install"]:::system
    T10["Evaluate and Link to Investors"]:::task

    T11["NPKI-Signed Certificate Issued"]:::system
    T12["Service Activated with NOC Monitoring"]:::system
    T13["Digital Certificate Delivered"]:::system
    T14["Site Connected and Monitored"]:::system
    T15["Innovation Adopted by Government"]:::task

    GW_MERGE{"× Merge"}:::gateway
    T16["Registry Updated - GPA Payment Reconciled"]:::system

    ENDEV(("●")):::startEnd

    START --> T_PORTAL
    T_PORTAL --> T_KONG
    T_KONG --> GW1
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
    T6 --> T11
    T7 --> T12
    T8 --> T13
    T9 --> T14
    T10 --> T15
    T11 --> GW_MERGE
    T12 --> GW_MERGE
    T13 --> GW_MERGE
    T14 --> GW_MERGE
    T15 --> GW_MERGE
    GW_MERGE --> T16
    T16 --> ENDEV
```

## 3. Integration Points

| System | Integration Method | Data Exchanged |
|--------|--------------------|----------------|
| eCitizen Portal | REST API via Kong | Connectivity requests, innovation submissions |
| MDA Service Portal | REST API via Kong | Standards proposals, hosting requests, NPKI applications |
| IPRS / Maisha Namba | KeSEL X-Road (NPKI signed) | Applicant identity verification for NPKI certificates |
| GDC Infrastructure | Internal VMware API | VM provisioning, firewall config, monitoring |
| NPKI HSM | Hardware Security Module | Cryptographic key generation and certificate signing |
| CA Root Certificate | Certificate chain | Root trust anchor for Government CA |
| NOFBI / GCCN | Network management | Backbone connectivity, last mile routing |
| GPA | Internal API | Hosting fees, connection fees |
| Camunda | Internal | Workflow, SLA timers, renewal reminders |
| GIS System | Internal API | Site surveys, route planning, coverage mapping |

## 4. BPMN Legend

| Symbol | Meaning |
|--------|---------|
| ((○)) | Start Event |
| ((●)) | End Event |
| [Text] | Task/Activity |
| {×} | Exclusive Gateway |
| {+} | Parallel Gateway |
| --> | Sequence Flow |
