# State Department for Broadcasting and Telecommunications
## Business Process Mapping Report

### Ministry of Information, Communications and The Digital Economy
### State Department for Broadcasting and Telecommunications

## 1. Overview

The State Department for Broadcasting and Telecommunications was created through Executive Order No. 1 of 2023. It formulates policy, oversees regulation, and coordinates the broadcasting and telecommunications sectors in Kenya. The Department works with the Communications Authority of Kenya (CA), Kenya Broadcasting Corporation (KBC), Postal Corporation of Kenya (PCK), and the Media Council of Kenya (MCK).

| Attribute | Description |
|-----------|-------------|
| Key Actors | Broadcasters, Telecom Operators, Applicants, Licensing Officers, Spectrum Officers, Public Communication Officers |
| Key Systems | CA Licensing Portal, Spectrum Management System, KBC Content Management, Postal Tracking |
| Semi-Autonomous Agencies | Communications Authority of Kenya (CA), KBC, PCK, MCK |

## 2. Services

### Process 1: Broadcasting Licence Application
- Receive broadcasting licence applications from operators
- Verify documentation and technical specifications
- Conduct frequency spectrum availability check
- Assess compliance with broadcasting regulations
- Issue broadcasting licence and assign frequencies

### Process 2: Spectrum Management and Allocation
- Receive spectrum allocation requests
- Conduct interference analysis and availability check
- Allocate frequency bands per National Frequency Table
- Issue spectrum licence and monitor usage
- Enforce compliance and address interference complaints

### Process 3: Public Communication and Government Messaging
- Receive communication briefs from MDAs
- Develop messaging strategy and content
- Coordinate distribution via KBC and media channels
- Monitor media coverage and public sentiment
- Prepare communication reports

### Process 4: Telecom Operator Compliance Monitoring
- Schedule compliance inspections for licensed operators
- Conduct site inspections and quality of service audits
- Review tariff submissions and consumer complaints
- Issue compliance reports and corrective directives
- Escalate persistent non-compliance to CA

## 3. Diagrams

### 3.1 Broadcasting Licence Application

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["Prepare Application and Technical Docs"]:::task
    T2["Submit Application to CA"]:::task
    T3["Pay Application Fee"]:::task
    T4["Review Documentation"]:::task

    GW1{"× Complete?"}:::gateway
    T5["Return for Corrections"]:::task

    T6["Check Spectrum Availability"]:::task
    T7["Conduct Technical Assessment"]:::task
    T8["Publish in Kenya Gazette"]:::task
    T9["Receive Public Objections"]:::task

    GW2{"× Approved?"}:::gateway
    T10["Reject Application"]:::task

    T11["Allocate Frequency"]:::task
    T12["Generate Licence"]:::task
    T13["Issue to Applicant"]:::task
    T14["Update Licence Registry"]:::task

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> GW1
    GW1 -->|Incomplete| T5
    T5 --> T1
    GW1 -->|Complete| T6
    T6 --> T7
    T7 --> T8
    T8 --> T9
    T9 --> GW2
    GW2 -->|Rejected| T10
    T10 --> ENDEV
    GW2 -->|Approved| T11
    T11 --> T12
    T12 --> T13
    T13 --> T14
    T14 --> ENDEV
```

### 3.2 Spectrum Management and Allocation

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["Receive Spectrum Request"]:::task
    T2["Verify Operator Licence Status"]:::task

    GW1{"× Licensed?"}:::gateway
    T3["Reject - Not Licensed"]:::task

    T4["Check National Frequency Table"]:::task
    T5["Conduct Interference Analysis"]:::task
    T6["Assess Spectrum Availability"]:::task

    GW2{"× Available?"}:::gateway
    T7["Notify No Spectrum Available"]:::task

    T8["Calculate Spectrum Fees"]:::task
    T9["Issue Payment Request"]:::task
    T10["Receive Payment Confirmation"]:::task
    T11["Assign Frequency Band"]:::task
    T12["Issue Spectrum Licence"]:::task
    T13["Register in Spectrum Database"]:::task
    T14["Schedule Monitoring"]:::task

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> GW1
    GW1 -->|No| T3
    T3 --> ENDEV
    GW1 -->|Yes| T4
    T4 --> T5
    T5 --> T6
    T6 --> GW2
    GW2 -->|No| T7
    T7 --> ENDEV
    GW2 -->|Yes| T8
    T8 --> T9
    T9 --> T10
    T10 --> T11
    T11 --> T12
    T12 --> T13
    T13 --> T14
    T14 --> ENDEV
```

### 3.3 Public Communication and Government Messaging

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    GW1{"× Message Source?"}:::gateway
    T1["Presidential Directive"]:::task
    T2["MDA Communication Brief"]:::task
    T3["Emergency or Crisis Alert"]:::task

    GW_MERGE{"× Merge"}:::gateway

    T4["Receive and Log Brief"]:::task
    T5["Develop Messaging Strategy"]:::task
    T6["Draft Content and Key Messages"]:::task
    T7["Obtain Clearance from PS"]:::task

    GW2{"× Approved?"}:::gateway
    T8["Return for Revision"]:::task

    T9["Distribute to KBC for Broadcast"]:::task
    T10["Issue to Print and Digital Media"]:::task
    T11["Monitor Media Coverage"]:::task
    T12["Prepare Coverage Report"]:::task

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
    T9 --> T10
    T10 --> T11
    T11 --> T12
    T12 --> ENDEV
```

### 3.4 Telecom Operator Compliance Monitoring

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["Schedule Compliance Inspection Cycle"]:::task
    T2["Notify Operator of Inspection"]:::task
    T3["Conduct Site Inspection"]:::task
    T4["Review Quality of Service Metrics"]:::task
    T5["Review Consumer Complaint Records"]:::task
    T6["Assess Tariff Compliance"]:::task
    T7["Compile Inspection Report"]:::task

    GW1{"× Compliant?"}:::gateway

    T8["Issue Compliance Certificate"]:::task
    T9["Issue Corrective Directive"]:::task
    T10["Set Remediation Deadline"]:::task
    T11["Track Remediation Progress"]:::task

    GW2{"× Remediated?"}:::gateway
    T12["Escalate to CA for Enforcement"]:::task

    GW_MERGE{"× Merge"}:::gateway

    T13["Update Compliance Registry"]:::task

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

### 3.5 End-to-End Broadcasting and Telecommunications

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    GW1{"× Service Type?"}:::gateway

    T1["Broadcasting Licence Application"]:::task
    T2["Spectrum Management"]:::task
    T3["Public Communication"]:::task
    T4["Compliance Monitoring"]:::task

    T5["Licence Issued"]:::task
    T6["Spectrum Allocated"]:::task
    T7["Message Distributed"]:::task
    T8["Compliance Verified"]:::task

    GW_MERGE{"× Merge"}:::gateway
    T9["Registry Updated"]:::task

    ENDEV(("●")):::startEnd

    START --> GW1
    GW1 -->|Licence| T1
    GW1 -->|Spectrum| T2
    GW1 -->|Communication| T3
    GW1 -->|Compliance| T4

    T1 --> T5
    T2 --> T6
    T3 --> T7
    T4 --> T8

    T5 --> GW_MERGE
    T6 --> GW_MERGE
    T7 --> GW_MERGE
    T8 --> GW_MERGE

    GW_MERGE --> T9
    T9 --> ENDEV
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
