# Ministry of Children Services - Business Process Mapping

## 1. Overview
The Ministry of Children Services is responsible for child welfare, protection, and development in Kenya. The Ministry coordinates child protection interventions, alternative family care, and child participation programmes through a network of Children Officers at national and county levels.

| Attribute | Description |
| :--- | :--- |
| **Mapping Level** | Level 3 - Actor-based Logical Process |
| **Key Actors** | Reporting Party, Children Officers, Case Committees, Courts, Alternative Care Providers |
| **Current State** | Manual paper-based case management |
| **Digitisation Priority** | High |

---

## 2. Process Definitions

### Process 1: Child Protection
1. **Reporting:** Receive and log reports from multiple channels; assign case reference numbers.
2. **Intake Assessment:** Screening, risk determination, and deciding on immediate protective action.
3. **Investigation:** Home visits, interviews, gathering evidence and documentation.
4. **Case Planning:** Development of care plans and coordination with service providers.
5. **Intervention:** Implementing protective measures (Foster, Institutional, Family Support).
6. **Monitoring:** Tracking progress and periodic reviews.
7. **Closure:** Achievement assessment and archiving.

### Process 2: Alternative Family Care
1. **Foster Care:** Assessment, matching, and monitoring of foster family placements.
2. **Adoption:** Processing applications and conducting suitability assessments.

---

## 3. BPMN 2.0 Process Flows

### 3.1 Child Protection (End-to-End)

```mermaid
flowchart TD
    Start((Start)) --> Report[Log Report]
    Report --> Screening[Initial Screening]
    Screening --> Risk[Risk Assessment]
    
    Risk --> Danger{Immediate Danger?}
    Danger -- Yes --> Emergency[Emergency Removal]
    Emergency --> OpenFile[Open Case File]
    
    Danger -- No --> OpenFile
    
    OpenFile --> Investigation[Home Visit & Evidence Gathering]
    Investigation --> ReportAss[Assessment Report]
    ReportAss --> Plan[Develop Care Plan]
    Plan --> Conference[Case Conference]
    
    Conference --> Approve{Approve Plan?}
    Approve -- No --> Plan
    Approve -- Yes --> Intervention[Intervention Execution]
    
    Intervention --> Type{Intervention Type}
    Type -- Family --> Support[Family Support]
    Type -- Foster --> Foster[Foster Care]
    Type -- Institution --> Inst[Institutional Care]
    Type -- Legal --> Court[Court Process]
    
    Support & Foster & Inst & Court --> Monitoring[Track Progress]
    
    Monitoring --> Review{Goals Met?}
    Review -- No --> Update[Update Plan]
    Update --> Monitoring
    
    Review -- Yes --> Assessment[Final Assessment]
    Assessment --> Archive[Complete Docs & Archive]
    Archive --> End((End))
```

### 3.2 Reporting Process

```mermaid
flowchart TD
    S((Start)) --> Source{Who Reports?}
    Source --> Parent[Parent/Family]
    Source --> Community[Community/Neighbor]
    Source --> Professional[Teacher/Police]
    
    Parent & Community & Professional --> Channel{Channel}
    Channel --> WalkIn[Walk-in]
    Channel --> Phone[Helpline/Hotline]
    Channel --> Written[Referral Form]
    
    WalkIn & Phone & Written --> Doc[Document Child Info]
    Doc --> Location[Note Location & Concern]
    Location --> Assign[Assign Reference & Officer]
    Assign --> File[Create File]
    File --> E((To Intake))
```

### 3.3 Intake & Risk Assessment

```mermaid
flowchart TD
    Start((From Reporting)) --> Review[Review Report]
    Review --> History[Check History]
    History --> Contact[Contact Reporter]
    Contact --> Safety[Assess Safety]
    
    Safety --> RiskLevel{Risk Level}
    RiskLevel -- High --> Action[Police/Medical/Removal]
    RiskLevel -- Medium --> Investigation[To Investigation]
    RiskLevel -- Low --> Next[To Support/Referral]
    
    Action --> Investigation
```
