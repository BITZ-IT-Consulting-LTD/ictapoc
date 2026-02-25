# Agriculture and Food Authority (AFA) – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Agriculture and Food Authority
- **Process Name:** Farmer Registration & Licensing
- **Document Version:** 2.1
- **Date:** 2026-02-24
- **Classification:** Official

---

## Executive Summary
The Agriculture and Food Authority (AFA) regulates, develops, and promotes scheduled crops (coffee, tea, nuts, etc.). The current manual and fragmented licensing processes lead to delays in export permits, trading licenses, and farmer registration. The transition to the Kenya DSAP Architecture aims to establish KIAMIS as the single source of truth for farmers, while integrating with BRS, KRA, and Kentrade to automate compliance and licensing.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (End-to-End AFA Services based on Deep Dive).*

```mermaid
graph TD
    Start((Start)) --> CompleteForm["Complete Application Form"]
    
    subgraph Applicant [Trader / Farmer]
        CompleteForm --> AttachBRS["Attach Business Registration"]
        AttachBRS --> AttachPremises["Attach Premises Documents"]
        AttachPremises --> Submit["Submit Application"]
    end
    
    subgraph AFA [AFA Directorates]
        Submit --> ReviewDocs["Review Documentation"]
        ReviewDocs --> AssessPrem["Assess Premises (Physical Inspection)"]
        AssessPrem --> VerifyCap["Verify Capacity"]
        VerifyCap --> Decision{"Decision?"}
        
        Decision -- "Info" --> RequestInfo["Request More Info"]
        RequestInfo --> CompleteForm
        
        Decision -- "Reject" --> Reject["Reject Application"]
        
        Decision -- "Approve" --> GenLicense["Generate License / Permit"]
        GenLicense --> Notify["Notify Applicant"]
        Notify --> UpdateReg["Update Manual Registry"]
    end
    
    UpdateReg --> End((End))
    Reject --> End

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333;
    class Start start;
    class End endNode;
    class Decision gateway;
    class CompleteForm,AttachBRS,AttachPremises,Submit,ReviewDocs,AssessPrem,VerifyCap,RequestInfo,Reject,GenLicense,Notify,UpdateReg userTask;
```

---

## Process Overview
### Process Name
End-to-End Farmer Registration, Export Permits, and Trading Licenses

### Service Category
- G2B (Government to Business) / G2C (Government to Citizen)

### Scope
- **In Scope:** Farmer profiling (KIAMIS), issuing trading licenses, and approving export/import permits.
- **Out of Scope:** Customs clearance at the port (handled by KRA/Kentrade).

### Triggers
- A trader applying for a license or a farmer registering to supply scheduled crops.

### End States
- **Successful:** Verifiable Digital Trading License or Export Permit issued.

### Policy Context
- Agriculture and Food Authority Act; Crops Act.

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Applicant | Fills application forms for licenses or permits and attaches paper copies of BRS certificates and land documents. | Paper/Portal | High manual effort. |
| 2 | AFA Clerk | Receives and logs the application, assigning a manual reference number. | Manual Registry | |
| 3 | AFA Inspector | Travels to physically assess the applicant's premises and verify operational capacity. | Manual | Major bottleneck. |
| 4 | AFA Committee | Reviews the inspection report and documentation to make a decision (Approve/Reject/Info). | Committee | |
| 5 | AFA Admin | If approved, manually generates the license/permit and notifies the applicant. | AFA IMIS | |

---

## Pain Points & Opportunities
### Pain Points
- **Manual Verification:** Officers manually verify BRS and KRA documents, leading to fraud risks.
- **Inspection Delays:** Physical premise inspections cause massive backlogs.
- **Siloed Registries:** KIAMIS (farmers), AFA IMIS (licenses), and Kentrade (exports) are not fully integrated.

### Opportunities
- **Automated Validation:** Use KeSEL (X-Road) to validate BRS (ownership) and KRA (tax compliance) instantly.
- **Risk-Based Inspections:** Auto-approve renewals for low-risk applicants without physical visits.
- **Integrated Payments:** Shift all cess and license fees to the Government Payment Aggregator (GPA).

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Kenya DSAP Architecture - Huduma Bridge).*

```mermaid
graph TD
    Start((Start)) --> Portal["Applicant accesses eCitizen Portal"]
    
    subgraph Access [Channels]
        Portal --> Select["Selects License/Permit Type"]
    end
    
    subgraph Interoperability [X-Road & Registries]
        Select --> QueryBRS["X-Road: Validate Company via BRS"]
        QueryBRS --> QueryKRA["X-Road: Validate Tax via KRA iTax"]
        QueryKRA --> AutoPop["Auto-populate Digital Form"]
    end
    
    subgraph Payments [Govt Payment Aggregator]
        AutoPop --> Pay["Initiate Payment via GPA"]
    end
    
    subgraph CorePlatform [Workflow Engine & AFA]
        Pay --> Rules{"Rules Engine"}
        Rules -- "Low Risk/Renewal" --> AutoApprove["Auto-Approve Application"]
        Rules -- "High Risk" --> Officer["Route to Officer Workbench for Review"]
        Officer --> Approve["Officer Approves"]
        
        AutoApprove --> Output["Generate Verifiable Digital License (QR)"]
        Approve --> Output
        Output --> Sync["Sync data to KIAMIS & Kentrade"]
    end
    
    Sync --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333;
    class Start start;
    class End endNode;
    class Rules gateway;
    class Portal,Select,Officer,Approve userTask;
    class QueryBRS,QueryKRA,AutoPop,Pay,AutoApprove,Output,Sync serviceTask;
```

## Future State Process (TO-BE)
### Narrative
**TO-BE Process: Automated Licensing via Huduma Bridge**

**Design Principles:**
- **Once-Only Principle:** BRS and KRA data is fetched automatically via APIs; applicants no longer upload paper certificates.
- **Cashless & Transparent:** All payments are unified under the GPA, ensuring immediate reconciliation and split-billing where necessary.
- **Automated Orchestration:** The Camunda workflow engine applies risk profiles to auto-approve standard renewals, reserving manual inspections only for high-risk or first-time applicants.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Applicant | Logs into eCitizen and selects the required AFA service (e.g., Export Permit). | eCitizen Portal |
| 2 | System | Fetches business details from BRS and tax status from KRA instantly via X-Road. | KeSEL / X-Road |
| 3 | Applicant | Pays the required cess or license fee through unified mobile money or card options. | GPA |
| 4 | System | Rules Engine assesses risk. If low risk (e.g., renewal), it auto-approves. If high risk, routes to an inspector. | Workflow Engine |
| 5 | System | Generates a QR-coded digital license and pushes the approval status directly to the Kentrade Single Window System. | Output Generator |

---

## References
- Agriculture and Food Authority Act.
- Kenya DSAP Architecture.