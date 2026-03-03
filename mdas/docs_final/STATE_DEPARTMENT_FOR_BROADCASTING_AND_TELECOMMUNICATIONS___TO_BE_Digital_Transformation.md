# State Department for Broadcasting and Telecommunications — TO-BE
## Business Process Mapping Report

### Ministry of Information, Communications and The Digital Economy
### State Department for Broadcasting and Telecommunications

## 1. Overview

| Attribute | Description |
|-----------|-------------|
| Process Scope | Digital transformation of broadcasting licensing, spectrum management, public communication, and compliance monitoring |
| Huduma Bridge Integration | eCitizen Portal, API Gateway (Kong), Camunda Workflow Engine, KeSEL (BRS, KRA, IPRS), GPA, NPKI, Consent Manager |
| GEA Principles | Citizen-Centricity, Standards-Driven, Interoperability by Design, Reuse and Modularity |

## 2. TO-BE Processes

### 2.1 TO-BE: Digital Broadcasting Licence Application

#### Key Transformation

| AS-IS | TO-BE |
|-------|-------|
| Paper application submitted to CA offices | Online application via eCitizen Portal |
| Manual document verification | Automated BRS and KRA compliance checks via KeSEL |
| Manual spectrum check | Automated spectrum availability query to CA database |
| Paper-based Kenya Gazette publication | Digital gazette with online objection portal |
| Manual licence generation | NPKI-signed digital licence with QR verification |
| Manual fee collection | GPA-integrated payment (M-Pesa, bank, card) |

#### Process Diagram

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    T1["Access eCitizen Portal - Broadcasting Services"]:::task
    T2["Dynamic Form Builder - Render Application Form"]:::system
    T3["Upload Technical Specifications and Documents"]:::task
    T4["GPA - Process Application Fee"]:::system
    T5["Kong API Gateway - Validate and Route"]:::system

    PG1{"+ Parallel Verification"}:::gateway
    T6["KeSEL BRS - Verify Business Registration"]:::system
    T7["KeSEL KRA - Verify Tax Compliance"]:::system
    T8["KeSEL IPRS - Verify Director Identities"]:::system
    PG1_END{"+ Sync"}:::gateway

    GW1{"× Verified?"}:::gateway
    T9["Reject - Notify Applicant via SMS and Email"]:::task

    T10["Query CA Spectrum Database - Check Availability"]:::system
    T11["Automated Technical Assessment"]:::system
    T12["Publish Digital Gazette Notice"]:::system
    T13["Open Online Public Objection Window - 30 Days"]:::task

    GW2{"× Objections?"}:::gateway
    T14["Review Objections and Determine Outcome"]:::task

    T15["Camunda - Route for CA Director Approval"]:::system

    GW3{"× Approved?"}:::gateway
    T16["Reject with Reasons - Notify Applicant"]:::task

    T17["Allocate Frequency from Spectrum Database"]:::system
    T18["Generate Digital Licence - NPKI Signed"]:::system
    T19["Issue Licence via eCitizen - QR Verifiable"]:::task
    T20["Update Licence Registry"]:::system

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> T5
    T5 --> PG1
    PG1 --> T6
    PG1 --> T7
    PG1 --> T8
    T6 --> PG1_END
    T7 --> PG1_END
    T8 --> PG1_END
    PG1_END --> GW1
    GW1 -->|Failed| T9
    T9 --> ENDEV
    GW1 -->|Passed| T10
    T10 --> T11
    T11 --> T12
    T12 --> T13
    T13 --> GW2
    GW2 -->|Yes| T14
    T14 --> T15
    GW2 -->|None| T15
    T15 --> GW3
    GW3 -->|Rejected| T16
    T16 --> ENDEV
    GW3 -->|Approved| T17
    T17 --> T18
    T18 --> T19
    T19 --> T20
    T20 --> ENDEV
```

### 2.2 TO-BE: Digital Spectrum Management

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    T1["Access eCitizen - Spectrum Services"]:::task
    T2["Submit Spectrum Request with Technical Parameters"]:::task
    T3["Kong API Gateway - Route to CA Spectrum System"]:::system
    T4["Auto-Verify Operator Licence Status"]:::system

    GW1{"× Licensed?"}:::gateway
    T5["Reject - Operator Not Licensed"]:::task

    T6["Query National Frequency Table - Availability"]:::system
    T7["Run Automated Interference Analysis"]:::system
    T8["Generate Propagation Model"]:::system

    GW2{"× Spectrum Available?"}:::gateway
    T9["Notify - No Spectrum Available - Waitlist Option"]:::task

    T10["Calculate Spectrum Fees"]:::system
    T11["GPA - Process Spectrum Fee Payment"]:::system
    T12["Assign Frequency Band"]:::system
    T13["Generate Spectrum Licence - NPKI Signed"]:::system
    T14["Activate Continuous Monitoring via IoT Sensors"]:::system
    T15["Update Spectrum Registry"]:::system

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> GW1
    GW1 -->|No| T5
    T5 --> ENDEV
    GW1 -->|Yes| T6
    T6 --> T7
    T7 --> T8
    T8 --> GW2
    GW2 -->|No| T9
    T9 --> ENDEV
    GW2 -->|Yes| T10
    T10 --> T11
    T11 --> T12
    T12 --> T13
    T13 --> T14
    T14 --> T15
    T15 --> ENDEV
```

### 2.3 TO-BE: Digital Public Communication

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    GW1{"× Message Source?"}:::gateway
    T1["Presidential Directive via EDRMS"]:::task
    T2["MDA Brief via Officer Workbench"]:::task
    T3["NC4 Emergency Alert"]:::task
    GW_MERGE{"× Merge"}:::gateway

    T4["Camunda - Create Communication Workflow"]:::system
    T5["Develop Messaging Strategy"]:::task
    T6["Draft Content and Key Messages"]:::task
    T7["Camunda - Route for PS Clearance"]:::system

    GW2{"× Approved?"}:::gateway
    T8["Return with Revision Notes"]:::task

    T9["NPKI - Digitally Sign Approved Message"]:::system

    PG1{"+ Parallel Distribution"}:::gateway
    T10["Distribute to KBC for TV and Radio"]:::task
    T11["Push to Digital Media and Social Channels"]:::task
    T12["SMS Blast via GPA Notification Service"]:::system
    T13["Publish on eCitizen Announcements"]:::task
    PG1_END{"+ Sync"}:::gateway

    T14["Real-Time Media Monitoring Dashboard"]:::system
    T15["Generate Coverage and Sentiment Report"]:::system

    ENDEV(("●")):::startEnd

    START --> GW1
    GW1 -->|Presidential| T1
    GW1 -->|MDA Brief| T2
    GW1 -->|Emergency| T3
    T1 --> GW_MERGE
    T2 --> GW_MERGE
    T3 --> GW_MERGE
    GW_MERGE --> T4
    T4 --> T5
    T5 --> T6
    T6 --> T7
    T7 --> GW2
    GW2 -->|Revise| T8
    T8 --> T6
    GW2 -->|Approved| T9
    T9 --> PG1
    PG1 --> T10
    PG1 --> T11
    PG1 --> T12
    PG1 --> T13
    T10 --> PG1_END
    T11 --> PG1_END
    T12 --> PG1_END
    T13 --> PG1_END
    PG1_END --> T14
    T14 --> T15
    T15 --> ENDEV
```

### 2.4 TO-BE: Digital Compliance Monitoring

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c
    classDef timer fill:#fce4ec,stroke:#c62828,stroke-width:2px,color:#b71c1c

    START(("Timer - Scheduled Inspection Cycle")):::timer

    T1["Camunda - Generate Inspection Schedule"]:::system
    T2["Notify Operator via eCitizen and SMS"]:::system
    T3["Conduct Digital Site Inspection - Field App"]:::task
    T4["Auto-Pull QoS Metrics from CA Database"]:::system
    T5["Auto-Pull Consumer Complaints from CA Portal"]:::system
    T6["Review Tariff Data Against Approved Rates"]:::system
    T7["Auto-Generate Inspection Report"]:::system

    GW1{"× Compliant?"}:::gateway

    T8["Issue Digital Compliance Certificate - NPKI"]:::system
    T9["Issue Corrective Directive via eCitizen"]:::task
    T10["Camunda - Set Remediation SLA Timer"]:::system
    T11["Track Remediation via Operator Portal"]:::task

    GW2{"× Remediated?"}:::gateway
    T12["Escalate to CA Director for Enforcement"]:::task

    GW_MERGE{"× Merge"}:::gateway
    T13["Update Compliance Registry"]:::system

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> T5
    T5 --> T6
    T6 --> T7
    T7 --> GW1
    GW1 -->|Compliant| T8
    T8 --> GW_MERGE
    GW1 -->|Non-Compliant| T9
    T9 --> T10
    T10 --> T11
    T11 --> GW2
    GW2 -->|Yes| GW_MERGE
    GW2 -->|No| T12
    T12 --> GW_MERGE
    GW_MERGE --> T13
    T13 --> ENDEV
```

## 3. Integration Points

| System | Integration Method | Data Exchanged |
|--------|--------------------|----------------|
| eCitizen Portal | REST API via Kong | Applications, status, licence delivery |
| BRS | KeSEL X-Road (NPKI signed) | Business registration verification |
| KRA | KeSEL X-Road (NPKI signed) | Tax compliance verification |
| IPRS / Maisha Namba | KeSEL X-Road (NPKI signed) | Director identity verification |
| CA Spectrum Database | Internal API | Frequency availability, interference analysis |
| GPA | Internal API | All fee payments and reconciliation |
| NPKI (ICTA CA) | Certificate Service | Digital signatures on licences |
| Camunda | Internal | Workflow, SLA timers, approval routing |

## 4. BPMN Legend

| Symbol | Meaning |
|--------|---------|
| ((○)) | Start Event |
| ((●)) | End Event |
| ((Timer)) | Timer Start Event |
| [Text] | Task/Activity |
| {×} | Exclusive Gateway |
| {+} | Parallel Gateway |
| --> | Sequence Flow |
