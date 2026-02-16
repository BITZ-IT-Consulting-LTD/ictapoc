# Kenya Revenue Authority – Tax Return Filing

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Revenue Authority
- **Process Name:** Tax Return Filing
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya Revenue Authority (KRA) is the principal government agency responsible for the assessment, collection, and accounting of all government revenues. Established on July 1, 1995, by an Act of Parliament (Chapter 469 of the laws of Kenya), KRA advises the government on tax policy, enforces compliance with tax and customs laws, and facilitates trade, utilizing digital platforms like iTax for taxpayer services.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To efficiently and effectively mobilize government revenue and facilitate trade by fostering compliance with tax and customs laws in Kenya; to advise the government on tax policy; to provide quality taxpayer services; and to combat tax evasion and illicit trade through robust enforcement measures.

### Legal Context
- Established on July 1, 1995, by an Act of Parliament (Chapter 469 of the laws of Kenya). Operates under the legislative framework of various tax and customs laws, including the Income Tax Act, Value Added Tax Act, and East African Community Customs Management Act. It advises the National Treasury on tax policy and implements government fiscal policies.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Taxpayer [Taxpayer]
        S1["Taxpayer logs into the KRA iTax portal (itax.kra.g..."]
        S2["Taxpayer selects 'Returns' menu and chooses 'File ..."]
        S3["Taxpayer selects the tax obligation (e.g., Income ..."]
        S4["Taxpayer downloads the Excel/ODS return form (or u..."]
        S5["Taxpayer fills the return form offline and uploads..."]
        S7["Taxpayer downloads and prints the Acknowledgement ..."]
    end
    subgraph System [System]
        S6["System validates the return and generates an E-Ret..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> End((End))
```

---

## Process Overview
### Service Category
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within Kenya Revenue Authority.

### Triggers
- Submission of application/request by Taxpayer.

### End States
- **Successful:** Tax Compliance Certificate, Assessment Order, Release Order

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Taxpayer | Process Actor | Performs actions as defined in steps. |
| System | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Tax Return Form, Bank Statements, Import Entry Declaration
- **Outputs:** Tax Compliance Certificate, Assessment Order, Release Order

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Taxpayer | Taxpayer logs into the KRA iTax portal (itax.kra.go.ke) using PIN and password. | Digital | |
| 2 | Taxpayer | Taxpayer selects 'Returns' menu and chooses 'File Return' or 'File Nil Return'. | Manual | |
| 3 | Taxpayer | Taxpayer selects the tax obligation (e.g., Income Tax Resident) and period. | Manual | |
| 4 | Taxpayer | Taxpayer downloads the Excel/ODS return form (or uses the web-based form for simple returns). | Manual | |
| 5 | Taxpayer | Taxpayer fills the return form offline and uploads the generated ZIP file back to the portal. | Digital | |
| 6 | System | System validates the return and generates an E-Return Acknowledgement Receipt. | Manual | |
| 7 | Taxpayer | Taxpayer downloads and prints the Acknowledgement Receipt. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Tax evasion
- Complex filing process
- System downtime

### Opportunities
- Integration with IPRS/BRS via Service Bus.
- Adoption of Government Payment Gateway.
- Implementation of Automated Rules Engine.
- Issuance of Digital Verifiable Credentials.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Optimized with Service Bus & Registries).*

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

- [https://www.kra.go.ke/](https://www.kra.go.ke/)
- [https://pfmr.go.ke/](https://pfmr.go.ke/)
- [https://en.wikipedia.org/wiki/Kenya_Revenue_Authority](https://en.wikipedia.org/wiki/Kenya_Revenue_Authority)
