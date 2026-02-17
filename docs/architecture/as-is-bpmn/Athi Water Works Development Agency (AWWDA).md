# Athi Water Works Development Agency (AWWDA) - Business Process Mapping

## 1. Overview
AWWDA develops and manages water infrastructure within the Athi River Basin including planning, design, construction, and improvement.

| Attribute | Description |
| :--- | :--- |
| **Mapping Level** | Level 3 - Actor-based Logical Process |
| **Key Actors** | Project Engineers, Design Teams, Contractors, Water Service Providers |
| **Key Systems** | Project Management System, GIS, IFMIS |
| **Digitisation Priority** | High |

---

## 2. Process Definitions

### Process 1: Planning
1. **Demand Assessment:** Conduct studies, analyze projections, assess capacity, identify gaps.
2. **Feasibility Studies:** Technical assessment, Environmental impact, Social impact, Prepare reports.

### Process 2: Design
1. **Concept Design:** Develop concepts, evaluate alternatives, select approach, prepare report.
2. **Detailed Design:** Prepare engineering designs, develop quantities, prepare tenders, obtain approvals.

### Process 3: Build
1. **Procurement:** Issue tenders, evaluate submissions, award contracts, sign agreements.
2. **Construction:** Mobilize supervision, monitor progress, quality assurance, manage variations.
3. **Commissioning:** Testing, documentation, handover, completion certificate.

### Process 4: Improve
1. **Operations Monitoring:** Monitor performance, collect data, identify improvements, plan rehabilitation.

---

## 3. BPMN 2.0 Process Flows

### 3.1 Infrastructure Development Flow (End-to-End)

```mermaid
flowchart TD
    Start((Start)) --> Demand[Demand Assessment]
    Demand --> Feasibility[Feasibility Study]
    Feasibility --> Prioritize[Prioritize Projects]
    Prioritize --> Concept[Concept Design]
    Concept --> Detailed[Detailed Design]
    Detailed --> Review{Design Review OK?}
    
    Review -- No --> Concept
    Review -- Yes --> Procurement[Procurement]
    
    Procurement --> Construction[Construction]
    Construction --> Commissioning[Commissioning]
    Commissioning --> Operations[Monitor Operations]
    Operations --> AssetMgmt[Asset Management]
    AssetMgmt --> End((End))
```

### 3.2 Procurement Process

```mermaid
flowchart TD
    PStart((From Design)) --> Finalize[Finalize Tender Docs]
    Finalize --> Budget{Budget Confirmed?}
    
    Budget -- No --> Adjust[Adjust Scope]
    Adjust --> Finalize
    
    Budget -- Yes --> Publish[Publish Notice]
    Publish --> Queries[Respond to Queries]
    Queries --> Receive[Receive Submissions]
    
    Receive --> Preliminary[Preliminary Evaluation]
    Preliminary --> Technical[Technical Evaluation]
    Technical --> Financial[Financial Evaluation]
    
    Financial --> Report[Prepare Evaluation Report]
    Report --> Committee{Committee Approval?}
    
    Committee -- No --> Re-evaluate[Re-evaluation]
    Re-evaluate --> Preliminary
    
    Committee -- Yes --> Award[Issue Award Letter]
    Award --> Sign[Sign Contract]
    Sign --> Mobilize[Mobilize to Site]
    Mobilize --> PEnd((To Construction))
```

### 3.3 Construction Supervision & Payment

```mermaid
flowchart TD
    CStart((Mobilize Team)) --> SiteSetup[Establish Office]
    SiteSetup --> ReviewProg[Review Programme]
    ReviewProg --> Monitor[Monitor Activities]
    
    Monitor --> Inspection[Site Inspections]
    Inspection --> Testing[Material Testing]
    Testing --> Quality{Work OK?}
    
    Quality -- No --> NonConform[Non-Conformance Issued]
    NonConform --> Monitor
    
    Quality -- Yes --> Measure[Measure Works]
    Measure --> IPC[Prepare IPC]
    IPC --> Certify[Certify Payment]
    Certify --> Payment[Process Payment]
    
    Payment --> Progress[Progress Reports]
    Progress --> Finish{Completion?}
    
    Finish -- No --> Monitor
    Finish -- Yes --> CEnd((Handover))
```
