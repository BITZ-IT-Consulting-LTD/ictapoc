# State Department for ICT and Digital Economy — TO-BE
## Business Process Mapping Report

### Ministry of Information, Communications and The Digital Economy
### State Department for ICT and Digital Economy

## 1. Overview

| Attribute | Description |
|-----------|-------------|
| Process Scope | Digital transformation of ICT policy development, digital economy coordination, cybersecurity, and cloud governance |
| Huduma Bridge Integration | eCitizen Portal, Kong API Gateway, Camunda Workflow Engine, KeSEL, NPKI, NC4 Integration, GDMIS |
| GEA Principles | Standards-Driven, Security by Design, Data as Strategic Asset, Interoperability by Design |
| Strategic Role | Policy authority over Huduma Bridge architecture, drives National Digital Master Plan 2022-2032 |

## 2. TO-BE Processes

### 2.1 TO-BE: Digital ICT Policy Development

#### Key Transformation

| AS-IS | TO-BE |
|-------|-------|
| Manual policy gap identification | Data-driven gap analysis from MDA digital maturity dashboards |
| Physical stakeholder consultations | Hybrid digital consultation via eCitizen public participation portal |
| Paper policy drafts circulated by mail | Digital drafting with version control and NPKI-signed approvals |
| Manual Cabinet submission | Digital submission via CABMEMO (EDRMS) |
| Paper gazette publication | Digital gazette with eCitizen policy notification |
| No implementation tracking | GDMIS-integrated policy implementation tracking |

#### Process Diagram

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    T1["Data-Driven Policy Gap Analysis from MDA Dashboards"]:::system
    T2["Form Multi-Stakeholder Committee via Workbench"]:::task
    T3["Publish Consultation on eCitizen Public Portal"]:::system
    T4["Collect Digital Submissions and Feedback"]:::system
    T5["Draft Policy Document with Version Control"]:::task
    T6["Camunda - Route for PS Digital Review"]:::system

    GW1{"× PS Approved?"}:::gateway
    T7["Return with Digital Revision Notes"]:::task

    T8["NPKI - PS Digitally Signs Policy Draft"]:::system
    T9["Submit to Cabinet via CABMEMO EDRMS"]:::system

    GW2{"× Cabinet Decision?"}:::gateway
    T10["Return with Cabinet Feedback"]:::task

    T11["Gazette Approved Policy Digitally"]:::system
    T12["Publish on eCitizen - Notify MDAs via SMS"]:::system
    T13["Register in GDMIS for Implementation Tracking"]:::system
    T14["Assign Implementation Leads - ICTA and KoTDA"]:::task

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
    T8 --> T9
    T9 --> GW2
    GW2 -->|Revise| T10
    T10 --> T5
    GW2 -->|Approve| T11
    T11 --> T12
    T12 --> T13
    T13 --> T14
    T14 --> ENDEV
```

### 2.2 TO-BE: Digital Economy Programme Coordination

#### Key Transformation

| AS-IS | TO-BE |
|-------|-------|
| Manual priority definition from documents | Digital Master Plan priorities auto-loaded into GDMIS |
| Manual directive issuance to MDAs | Digital directives via Officer Workbench with read receipts |
| Quarterly paper reports from agencies | Real-time dashboards with automated KPI collection |
| Manual escalation to PS | Camunda SLA timers with auto-escalation on delays |
| Paper reports to Cabinet | Auto-generated reports from GDMIS dashboard data |

#### Process Diagram

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c
    classDef timer fill:#fce4ec,stroke:#c62828,stroke-width:2px,color:#b71c1c

    START(("○")):::startEnd

    T1["Load Digital Master Plan Priorities into GDMIS"]:::system
    T2["Assign Implementation Leads - ICTA KoTDA MDAs"]:::task
    T3["Issue Digital Directives via Officer Workbench"]:::system
    T4["Confirm Receipt from All Agencies"]:::system

    TIMER(("Timer - Quarterly Review Cycle")):::timer

    T5["GDMIS - Auto-Collect KPI Data from Agencies"]:::system
    T6["Generate Programme Dashboard"]:::system

    GW1{"× On Track?"}:::gateway
    T7["Auto-Generate Corrective Directive"]:::system
    T8["Camunda - Escalate Delays to PS"]:::system

    T9["Auto-Generate Cabinet Progress Report"]:::system
    T10["Auto-Generate Donor Report - KDEAP HoAGDP"]:::system

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> TIMER
    TIMER --> T5
    T5 --> T6
    T6 --> GW1
    GW1 -->|Delayed| T7
    T7 --> T8
    T8 --> TIMER
    GW1 -->|On Track| T9
    T9 --> T10
    T10 --> ENDEV
```

### 2.3 TO-BE: Digital Cybersecurity Policy Coordination

#### Key Transformation

| AS-IS | TO-BE |
|-------|-------|
| Manual threat monitoring | Real-time NC4 threat feed integration |
| Manual coordination with NC4 and CA | Automated incident routing via KeSEL and Camunda |
| Paper cybersecurity guidelines | Digital guideline publication via eCitizen with MDA push |
| Manual compliance monitoring | Automated compliance scanning against CMCA 2018 and DPA 2019 |
| Paper reports to Cabinet | Auto-generated cybersecurity posture dashboard |

#### Process Diagram

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    GW1{"× Trigger?"}:::gateway
    T1["NC4 Real-Time Threat Feed Alert"]:::system
    T2["NC4 Incident Report via KeSEL"]:::system
    T3["Scheduled Policy Review Cycle"]:::task
    GW_MERGE{"× Merge"}:::gateway

    T4["Auto-Assess Threat Against National Infrastructure"]:::system

    PG1{"+ Parallel Coordination"}:::gateway
    T5["KeSEL NC4 - Coordinate Incident Response"]:::system
    T6["KeSEL CA - Check Affected Licensees"]:::system
    T7["Query ICTA GDC - Check Government Systems"]:::system
    PG1_END{"+ Sync"}:::gateway

    T8["Draft Cybersecurity Guidelines"]:::task
    T9["Auto-Verify Against CMCA 2018 and DPA 2019"]:::system

    GW2{"× Requires Cabinet?"}:::gateway
    T10["Submit Policy to Cabinet via CABMEMO"]:::system
    T11["NPKI - PS Signs Ministerial Directive"]:::system
    GW_MERGE2{"× Merge"}:::gateway

    T12["Publish Guidelines on eCitizen"]:::system
    T13["Push to All MDAs via Officer Workbench"]:::system
    T14["Auto-Scan MDA Compliance Quarterly"]:::system
    T15["Generate Cybersecurity Posture Dashboard"]:::system

    ENDEV(("●")):::startEnd

    START --> GW1
    GW1 -->|Threat| T1
    GW1 -->|Incident| T2
    GW1 -->|Cycle| T3
    T1 --> GW_MERGE
    T2 --> GW_MERGE
    T3 --> GW_MERGE
    GW_MERGE --> T4
    T4 --> PG1
    PG1 --> T5
    PG1 --> T6
    PG1 --> T7
    T5 --> PG1_END
    T6 --> PG1_END
    T7 --> PG1_END
    PG1_END --> T8
    T8 --> T9
    T9 --> GW2
    GW2 -->|Yes| T10
    T10 --> GW_MERGE2
    GW2 -->|No| T11
    T11 --> GW_MERGE2
    GW_MERGE2 --> T12
    T12 --> T13
    T13 --> T14
    T14 --> T15
    T15 --> ENDEV
```

### 2.4 TO-BE: Digital Cloud and Data Governance

```mermaid
flowchart TD
    classDef startEnd fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef task fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#0d47a1
    classDef gateway fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#e65100
    classDef system fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1px,color:#4a148c

    START(("○")):::startEnd

    T1["MDA Submits Cloud Migration Proposal via Portal"]:::task
    T2["Auto-Check Against Kenya Cloud Policy"]:::system

    PG1{"+ Parallel Governance Checks"}:::gateway
    T3["Verify Data Residency - Kenya Sovereign Hosting"]:::system
    T4["Verify DPA 2019 Compliance - DPIA Required"]:::system
    T5["Verify Security Standards - ISO 27001"]:::system
    T6["Check ICTA GDC Capacity for Govt Cloud"]:::system
    PG1_END{"+ Sync"}:::gateway

    T7["Generate Governance Assessment Report"]:::system

    GW1{"× Compliant?"}:::gateway
    T8["Issue Digital Corrective Requirements"]:::task

    GW2{"× Hosting Location?"}:::gateway
    T9["Route to ICTA GDC for Government Cloud"]:::system
    T10["Approve Third-Party Cloud with Conditions"]:::task

    GW_MERGE{"× Merge"}:::gateway

    T11["Register in Cloud Governance Registry"]:::system
    T12["Camunda - Schedule Ongoing Compliance Reviews"]:::system

    ENDEV(("●")):::startEnd

    START --> T1
    T1 --> T2
    T2 --> PG1
    PG1 --> T3
    PG1 --> T4
    PG1 --> T5
    PG1 --> T6
    T3 --> PG1_END
    T4 --> PG1_END
    T5 --> PG1_END
    T6 --> PG1_END
    PG1_END --> T7
    T7 --> GW1
    GW1 -->|Non-Compliant| T8
    T8 --> T1
    GW1 -->|Compliant| GW2
    GW2 -->|Government Cloud| T9
    GW2 -->|Third-Party| T10
    T9 --> GW_MERGE
    T10 --> GW_MERGE
    GW_MERGE --> T11
    T11 --> T12
    T12 --> ENDEV
```

## 3. Integration Points

| System | Integration Method | Data Exchanged |
|--------|--------------------|----------------|
| eCitizen Portal | REST API via Kong | Public consultations, policy publications, notifications |
| CABMEMO / EDRMS | Internal API | Cabinet memoranda submission and tracking |
| GDMIS | Internal API | Priority registration, KPI tracking, programme dashboards |
| NC4 | KeSEL X-Road | Threat intelligence, incident reports, response coordination |
| CA | KeSEL X-Road | Licensee data, spectrum monitoring, compliance status |
| ICTA GDC | Internal API | System health checks, cloud capacity, hosting status |
| NPKI (ICTA CA) | Certificate Service | Digital signatures for policy approvals and directives |
| Camunda | Internal | Workflow orchestration, SLA timers, escalation |
| Officer Workbench | WebSocket | MDA directive distribution, compliance monitoring |

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
