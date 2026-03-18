# Central Rift Valley Water Works Development Agency – Procurement Process

## Cover Page
- **Ministry/Department/Agency (MDA):** Central Rift Valley Water Works Development Agency
- **Process Name:** Procurement Process
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Central Rift Valley Water Works Development Agency (CRVWWDA) is one of nine Water Works Development Agencies in Kenya, established under Section 65 of the Water Act, 2016, through Kenya Gazette Notice No. 4 on February 7, 2020. Operating as a state corporation under the Ministry of Water & Sanitation and Irrigation, it is responsible for the development, maintenance, and management of national public water works within its jurisdiction, which includes Nakuru, Narok, Laikipia, Baringo, and Nyandarua counties. The Agency aims to plan, develop, and deliver efficient and reliable water and sanitation infrastructure to ensure sustainable access for all stakeholders.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the AS-IS process flow across different actors.*

```mermaid
graph TD
    Start((Start)) --> S1

    subgraph Agency [Agency]
        S1["Agency advertises tender on Public Procurement Informatio..."]
    end

    subgraph Bidder [Bidder]
        S2["Bidder downloads tender documents and prepares bid (Techn..."]
        S3["Bidder submits bid via e-Procurement portal or tender box."]
    end

    subgraph Evaluation_Committee [Evaluation Committee]
        S4["Evaluation Committee conducts opening, technical, and fin..."]
    end

    subgraph Accounting_Officer [Accounting Officer]
        S5["Accounting Officer awards the tender to the lowest respon..."]
    end

    subgraph Agency_Bidder [Agency/Bidder]
        S6["Contract is signed after the 14-day standstill period."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;

    class Start start;
    class End endNode;
    class S1,S2,S3,S4,S5,S6 userTask;
```

---

## Process Overview
### Process Name
Procurement Process

### Service Category
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within Central Rift Valley Water Works Development Agency.

### Triggers
- Submission of application/request by Agency.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

### Policy Context
- The Central Rift Valley Water Works Development Agency Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Bidder | Process Actor | Performs actions as defined in steps. |
| Agency | Process Actor | Performs actions as defined in steps. |
| Agency/Bidder | Process Actor | Performs actions as defined in steps. |
| Accounting Officer | Process Actor | Performs actions as defined in steps. |
| Evaluation Committee | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Agency | Agency advertises tender on Public Procurement Information Portal (PPIP) and website. | Digital | |
| 2 | Bidder | Bidder downloads tender documents and prepares bid (Technical & Financial). | Manual | |
| 3 | Bidder | Bidder submits bid via e-Procurement portal or tender box. | Digital | |
| 4 | Evaluation Committee | Evaluation Committee conducts opening, technical, and financial evaluation. | Manual | |
| 5 | Accounting Officer | Accounting Officer awards the tender to the lowest responsive bidder. | Manual | |
| 6 | Agency/Bidder | Contract is signed after the 14-day standstill period. | Manual | |

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

## References & Evidence
The information in this document was derived from the following official sources:

- [https://www.crvwwda.go.ke/](https://www.crvwwda.go.ke/)
- [https://opportunitiesforyoungkenyans.co.ke/](https://opportunitiesforyoungkenyans.co.ke/)
- [https://mygov.go.ke/](https://mygov.go.ke/)
- [https://tenders.go.ke/](https://tenders.go.ke/)

---

## Appendices
See attached ERD and System Design.


---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)
