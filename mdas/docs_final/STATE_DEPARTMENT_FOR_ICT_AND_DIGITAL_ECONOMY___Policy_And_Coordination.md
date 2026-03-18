# State Department for ICT and Digital Economy
## Business Process Mapping Report

### Ministry of Information, Communications and The Digital Economy
### State Department for ICT and Digital Economy

## 1. Overview

The State Department for ICT and Digital Economy was established through Executive Order No. 1 of 2023. It formulates ICT policy, drives digital government services, oversees cybersecurity coordination, promotes digital infrastructure development, and manages the national digital transformation agenda including the Kenya National Digital Master Plan 2022-2032.

| Attribute | Description |
|-----------|-------------|
| Key Actors | PS ICT, Policy Officers, Cybersecurity Coordinators, Digital Economy Officers, MDAs, County Governments |
| Key Systems | eCitizen (policy oversight), Kenya Digital Economy Blueprint, National Digital Master Plan, Cloud Policy Framework |
| Key Agencies | ICTA, Konza Technopolis Development Authority (KoTDA), NC4 (Cybersecurity Coordination) |

## 2. Services

### Process 1: ICT Policy Development
- Identify policy gaps in the ICT sector
- Conduct stakeholder consultations
- Draft policy documents
- Submit for Cabinet approval
- Gazette and communicate approved policies

### Process 2: Digital Economy Programme Coordination
- Define digital economy strategic priorities
- Coordinate implementation across ICTA, KoTDA, and MDAs
- Track programme milestones and KPIs
- Prepare progress reports for Cabinet and development partners
- Facilitate donor-funded projects (KDEAP, HoAGDP)

### Process 3: Cybersecurity Policy Coordination
- Monitor national cybersecurity threat landscape
- Coordinate with NC4 on incident response
- Develop cybersecurity policy and standards
- Issue guidelines to MDAs on data protection compliance
- Report to Cabinet on cybersecurity posture

### Process 4: Cloud and Data Governance
- Develop cloud computing policy framework
- Review MDA cloud migration proposals
- Assess data residency and sovereignty compliance
- Issue cloud adoption guidelines
- Monitor compliance with Data Protection Act 2019

## 3. Diagrams

### 3.1 ICT Policy Development

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["Identify Policy Gap or Directive"]:::task
    T2["Conduct Sector Analysis"]:::task
    T3["Form Multi-Stakeholder Committee"]:::task
    T4["Conduct Public Consultations"]:::task
    T5["Draft Policy Document"]:::task
    T6["Internal Review by PS Office"]:::task

    GW1{"× Approved by PS?"}:::gateway
    T7["Return for Revision"]:::task

    T8["Submit to Cabinet for Approval"]:::task

    GW2{"× Cabinet Decision?"}:::gateway
    T9["Return with Cabinet Feedback"]:::task

    T10["Gazette Approved Policy"]:::task
    T11["Communicate to MDAs and Public"]:::task
    T12["Develop Implementation Plan"]:::task

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> T5
    T5 --> T6
    T6 --> GW1
    GW1 -->|Revise| T7
    T7 --> T5
    GW1 -->|Approve| T8
    T8 --> GW2
    GW2 -->|Revise| T9
    T9 --> T5
    GW2 -->|Approve| T10
    T10 --> T11
    T11 --> T12
    T12 --> ENDEV
```

### 3.2 Digital Economy Programme Coordination

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["Define Strategic Priorities from Digital Master Plan"]:::task
    T2["Assign Implementation Leads to ICTA and KoTDA"]:::task
    T3["Issue Directives to MDAs"]:::task
    T4["Track Milestone Progress Quarterly"]:::task
    T5["Receive Agency Progress Reports"]:::task
    T6["Consolidate Programme Dashboard"]:::task

    GW1{"× On Track?"}:::gateway
    T7["Issue Corrective Directive"]:::task
    T8["Escalate Delays to PS"]:::task

    T9["Prepare Report for Cabinet"]:::task
    T10["Report to Development Partners"]:::task

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> T5
    T5 --> T6
    T6 --> GW1
    GW1 -->|Delayed| T7
    T7 --> T8
    T8 --> T4
    GW1 -->|On Track| T9
    T9 --> T10
    T10 --> ENDEV
```

### 3.3 Cybersecurity Policy Coordination

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    GW1{"× Trigger?"}:::gateway
    T1["Emerging Threat Intelligence"]:::task
    T2["NC4 Incident Report"]:::task
    T3["Policy Review Cycle"]:::task

    GW_MERGE{"× Merge"}:::gateway

    T4["Assess Threat Landscape"]:::task
    T5["Coordinate with NC4 and CA"]:::task
    T6["Draft Cybersecurity Guidelines"]:::task
    T7["Review Against CMCA 2018 and DPA 2019"]:::task

    GW2{"× Requires Cabinet?"}:::gateway
    T8["Submit Policy to Cabinet"]:::task
    T9["Issue Ministerial Directive to MDAs"]:::task

    GW_MERGE2{"× Merge"}:::gateway

    T10["Distribute Guidelines to MDAs"]:::task
    T11["Monitor Compliance"]:::task
    T12["Prepare Cybersecurity Posture Report"]:::task

    ENDEV(("●")):::startEnd

    START --> GW1
    GW1 -->|Threat| T1
    GW1 -->|Incident| T2
    GW1 -->|Cycle| T3
    T1 --> GW_MERGE
    T2 --> GW_MERGE
    T3 --> GW_MERGE

    GW_MERGE --> T4
    T4 --> T5
    T5 --> T6
    T6 --> T7
    T7 --> GW2
    GW2 -->|Yes| T8
    T8 --> GW_MERGE2
    GW2 -->|No| T9
    T9 --> GW_MERGE2

    GW_MERGE2 --> T10
    T10 --> T11
    T11 --> T12
    T12 --> ENDEV
```

### 3.4 Cloud and Data Governance

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    T1["Receive MDA Cloud Migration Proposal"]:::task
    T2["Review Against Kenya Cloud Policy"]:::task
    T3["Assess Data Residency Requirements"]:::task
    T4["Verify Data Protection Act Compliance"]:::task

    GW1{"× Compliant?"}:::gateway
    T5["Issue Corrective Recommendations"]:::task

    T6["Approve Cloud Migration"]:::task
    T7["Coordinate with ICTA GDC for Hosting"]:::task
    T8["Monitor Data Sovereignty Compliance"]:::task
    T9["Update Cloud Governance Registry"]:::task

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> GW1
    GW1 -->|Non-Compliant| T5
    T5 --> T1
    GW1 -->|Compliant| T6
    T6 --> T7
    T7 --> T8
    T8 --> T9
    T9 --> ENDEV
```

### 3.5 End-to-End State Department for ICT

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100

    START(("○")):::startEnd

    GW1{"× Function?"}:::gateway

    T1["ICT Policy Development"]:::task
    T2["Digital Economy Coordination"]:::task
    T3["Cybersecurity Coordination"]:::task
    T4["Cloud and Data Governance"]:::task

    T5["Policy Gazetted"]:::task
    T6["Programme Monitored"]:::task
    T7["Guidelines Issued"]:::task
    T8["Migration Governed"]:::task

    GW_MERGE{"× Merge"}:::gateway
    T9["Report to Cabinet"]:::task

    ENDEV(("●")):::startEnd

    START --> GW1
    GW1 -->|Policy| T1
    GW1 -->|Programmes| T2
    GW1 -->|Cybersecurity| T3
    GW1 -->|Cloud| T4

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
