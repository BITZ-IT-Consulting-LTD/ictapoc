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

## Service Mandate & Legal Basis
### Statutory Mandate
To undertake the development, maintenance, and management of national public water works within its designated service area (Nakuru, Narok, Laikipia, Baringo, and Nyandarua counties); to operate water works as a water service provider until the responsibility for operation and management is handed over to a designated water services provider, county government, joint committee, or authority of county governments; to provide water services when ordered by the Regulatory Board, particularly in cases where a defaulting water services provider's functions are transferred; to offer technical services and capacity building to county governments and water services providers upon request; and to provide technical support to the Cabinet Secretary in discharging duties under the Constitution and the Water Act, 2016.

### Legal Context
- Established under Section 65 of the Water Act, 2016, through Kenya Gazette Notice No. 4 on February 7, 2020. Its core mandate and functions are further provided by Section 68 of the Water Act, 2016. CRVWWDA operates as a state corporation under the Ministry of Water & Sanitation and Irrigation and aligns its activities with national water sector reforms, policies, and strategies aimed at enhancing access to safe, adequate, and affordable water and sanitation services for all Kenyans.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Agency [Agency]
        S1["Agency advertises tender on Public Procurement Inf..."]
    end
    subgraph Bidder [Bidder]
        S2["Bidder downloads tender documents and prepares bid..."]
        S3["Bidder submits bid via e-Procurement portal or ten..."]
    end
    subgraph EvaluationCommittee [Evaluation Committee]
        S4["Evaluation Committee conducts opening, technical, ..."]
    end
    subgraph AccountingOfficer [Accounting Officer]
        S5["Accounting Officer awards the tender to the lowest..."]
    end
    subgraph AgencyBidder [Agency/Bidder]
        S6["Contract is signed after the 14-day standstill per..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> End((End))
```

---

## Process Overview
### Service Category
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within Central Rift Valley Water Works Development Agency.

### Triggers
- Submission of application/request by Agency.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Bidder | Process Actor | Performs actions as defined in steps. |
| Evaluation Committee | Process Actor | Performs actions as defined in steps. |
| Accounting Officer | Process Actor | Performs actions as defined in steps. |
| Agency/Bidder | Process Actor | Performs actions as defined in steps. |
| Agency | Process Actor | Performs actions as defined in steps. |

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

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Optimized).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant logs in via Single Sign-On (SSO) and sel..."]
        S4["Applicant pays fees via the Government Payment Gat..."]
    end
    subgraph System [System]
        S2["Applicant enters Business Registration Number; Sys..."]
        S3["System performs auto-validation of compliance (e.g..."]
        S5["Application is processed by the Rules Engine. (Low..."]
        S7["System generates a Verifiable Digital Certificate ..."]
    end
    subgraph Officer [Officer]
        S6["Complex cases are routed to the Officer Workbench ..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> End((End))
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

## References & Evidence
The information in this document was derived from the following official sources:

- [https://www.crvwwda.go.ke/](https://www.crvwwda.go.ke/)
- [https://opportunitiesforyoungkenyans.co.ke/](https://opportunitiesforyoungkenyans.co.ke/)
- [https://mygov.go.ke/](https://mygov.go.ke/)
- [https://tenders.go.ke/](https://tenders.go.ke/)
