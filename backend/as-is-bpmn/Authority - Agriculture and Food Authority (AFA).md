# Authority - Agriculture and Food Authority (AFA) - Business Process Mapping

## 1. Overview
AFA regulates, develops, and promotes scheduled crops in Kenya including coffee, tea, horticulture, sugar, and food crops.

| Attribute | Description |
| :--- | :--- |
| **Mapping Level** | Level 3 - Actor-based Logical Process |
| **Key Actors** | Farmers, Traders, Export Agents, AFA Officers |
| **Key Systems** | KIAMIS, AFA IMIS, KENTRADE |
| **Digitisation Priority** | High |

---

## 2. Process Definitions

### Process 1: Registration
1. **Farmer Registration:** Receive applications, verify identity, capture farm details, register in KIAMIS, issue registration card.
2. **Trader Registration:** Receive applications, verify credentials, assess capacity, register traders.

### Process 2: Licensing
1. **Export Permit:** Receive application, verify origin and quality, check compliance, issue permit, integrate KENTRADE.
2. **Trading License:** Receive application, assess premises, verify capacity, issue license.

### Process 3: Regulation
1. **Inspections:** Receive requests, schedule visits, conduct inspections, issue certificates.

### Process 4: Trade Facilitation
1. **Market Intelligence:** Collect data, analyze trends, disseminate information, support decisions.

---

## 3. BPMN 2.0 Process Flows

### 3.1 AFA Services Flow (End-to-End)

```mermaid
flowchart TD
    Start((Start)) --> Reg[Apply for Registration]
    Reg --> Verify[Verify Details]
    Verify --> IssueReg[Issue Registration]
    
    IssueReg --> License[Apply for License]
    License --> Assess[Assessment]
    Assess --> IssueLic[Issue License]
    
    IssueLic --> Compliance[Compliance Monitoring]
    Compliance --> Inspect[Inspections]
    Inspect --> Cert[Certifications]
    
    Cert --> Intel[Market Intelligence]
    Intel --> Export[Export Facilitation]
    Export --> End((End))
```

### 3.2 Farmer Registration

```mermaid
flowchart TD
    Start((Start)) --> Form[Complete Form]
    Form --> Submission[Submit to County]
    Submission --> Receive[Receive Application]
    Receive --> Assign[Assign Reference]
    
    Assign --> VerifyID[Verify Identity]
    VerifyID --> VerifyLand[Verify Land]
    VerifyLand --> GIS[Capture GIS]
    
    GIS --> Verified{Verified?}
    Verified -- No --> Correction[Return for Correction]
    Correction --> Form
    
    Verified -- Yes --> KIAMIS[Enter in KIAMIS]
    KIAMIS --> GenID[Generate Farmer ID]
    GenID --> PrepCard[Prepare Card]
    PrepCard --> Notify[Notify Farmer]
    Notify --> Issue[Issue Card]
    Issue --> Update[Update Registry]
    Update --> End((End))
```

### 3.3 Export Permit Process

```mermaid
flowchart TD
    Start((Start)) --> Apply[Complete Form]
    Apply --> Attach[Attach License & Certs]
    Attach --> Submit[Submit via IMIS]
    Submit --> SysReceive[System Receives]
    
    SysReceive --> Route[Route to Directorate]
    Route --> VerifyTrader[Verify Trader]
    VerifyTrader --> VerifyOrigin[Verify Origin]
    VerifyOrigin --> Quality[Check Quality]
    
    Quality --> VStat{Verified?}
    VStat -- No --> Reject[Reject Application]
    Reject --> End((End))
    
    VStat -- Yes --> Approve[Approve]
    Approve --> Generate[Generate Permit]
    Generate --> KENTRADE[Transmit to KENTRADE]
    KENTRADE --> Customs[Link Customs]
    Customs --> Notify[Notify Exporter]
    Notify --> End
```
