# Solicitor General – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Solicitor General
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Governance Justice Law and Order' cluster for balanced coverage; entity type: Department. Included as Tier 3 for light‑touch desk review/survey.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1

    subgraph MDA [MDA]
        S1["MDA submits draft contract/MOU to the Attorney General."]
    end

    subgraph Solicitor_General [Solicitor General]
        S2["Solicitor General assigns State Counsel to review the doc..."]
    end

    subgraph State_Counsel [State Counsel]
        S3["State Counsel reviews for legal compliance and risks."]
    end

    subgraph SG_AG [SG/AG]
        S4["Legal opinion/clearance is drafted and approved."]
    end

    subgraph Attorney_General [Attorney General]
        S5["Advisory opinion/Clearance letter sent back to MDA."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;

    class Start start;
    class End endNode;
    class S1,S2,S3,S4,S5 userTask;
```

---

## Process Overview
### Process Name
Service Delivery

### Service Category
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within Solicitor General.

### Triggers
- Submission of application/request by MDA.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

### Policy Context
- The Solicitor General Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| MDA | Process Actor | Performs actions as defined in steps. |
| Solicitor General | Process Actor | Performs actions as defined in steps. |
| State Counsel | Process Actor | Performs actions as defined in steps. |
| SG/AG | Process Actor | Performs actions as defined in steps. |
| Attorney General | Process Actor | Performs actions as defined in steps. |

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | MDA | MDA submits draft contract/MOU to the Attorney General. | Manual | |
| 2 | Solicitor General | Solicitor General assigns State Counsel to review the document. | Manual | |
| 3 | State Counsel | State Counsel reviews for legal compliance and risks. | Manual | |
| 4 | SG/AG | Legal opinion/clearance is drafted and approved. | Manual | |
| 5 | Attorney General | Advisory opinion/Clearance letter sent back to MDA. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Manual document verification takes time.
- High cost and time for physical inspections.
- Risk of counterfeit licenses/certificates.
- Lack of real-time monitoring of licensees.

### Opportunities
- Integration with IPRS/BRS via Service Bus.
- Adoption of Government Payment Gateway.
- Implementation of Automated Rules Engine.
- Issuance of Digital Verifiable Credentials.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Optimized).*

```mermaid
graph TD
    Start((Start)) --> S1

    subgraph Applicant [Applicant]
        S1["Applicant logs in via Single Sign-On (SSO) and selects th..."]
        S4["Applicant pays fees via the Government Payment Gateway; S..."]
    end

    subgraph System [System]
        S2["Applicant enters Business Registration Number; System aut..."]
        S3["System performs auto-validation of compliance (e.g., KRA ..."]
        S5["Application is processed by the Rules Engine. (Low-risk c..."]
        S7["System generates a Verifiable Digital Certificate (QR Cod..."]
    end

    subgraph Officer [Officer]
        S6["Complex cases are routed to the Officer Workbench for dig..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;

    class Start start;
    class End endNode;
    class S1,S4,S6 userTask;
    class S2,S3,S5,S7 serviceTask;
```

## Future State Process (TO-BE)
### Narrative
The To-Be process leverages the Government Service Bus to integrate with BRS (Business Registry) and the Payment Gateway. Manual data entry and document uploads are replaced by real-time API validations, enabling a paperless, cashless, and presence-less service experience.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Applicant | Applicant logs in via Single Sign-On (SSO) and selects the service. | Citizen Portal / SSO |
| 2 | System | Applicant enters Business Registration Number; System auto-populates details from BRS (Business Registry) via the Service Bus. | Service Bus / Registry API |
| 3 | System | System performs auto-validation of compliance (e.g., KRA Tax Status) via Inter-Agency APIs. | Service Bus / Compliance Engine |
| 4 | Applicant | Applicant pays fees via the Government Payment Gateway; System auto-receipts. | Payment Gateway |
| 5 | System | Application is processed by the Rules Engine. (Low-risk cases are Auto-Approved). | Workflow Engine |
| 6 | Officer | Complex cases are routed to the Officer Workbench for digital review and approval. | Officer Workbench |
| 7 | System | System generates a Verifiable Digital Certificate (QR Code) and notifies the applicant. | Output Generator |

---

## References
Derived from official mandates.


---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)
