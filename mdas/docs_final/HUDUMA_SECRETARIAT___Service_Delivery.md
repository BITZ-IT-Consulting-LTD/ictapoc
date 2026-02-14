# HUDUMA SECRETARIAT – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** HUDUMA SECRETARIAT
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Huduma Secretariat Kenya is mandated to transform public service delivery, providing efficient, effective, accessible, and citizen-centric services through integrated 'one-stop-shop' platforms like Huduma Centres and Huduma E-Services. It's a flagship project under Kenya Vision 2030.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the AS-IS process flow across different actors.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Citizen [Citizen]
        S1["Citizen visits Huduma Centre and undergoes securit..."]
        S2["Citizen proceeds to the Information Desk for guida..."]
        S3["Citizen waits in the waiting area until their tick..."]
        S4["Citizen proceeds to the designated counter for ser..."]
        S6["Citizen makes payment via M-Pesa/Posta Pay if appl..."]
        S7["Citizen provides feedback on service quality via t..."]
    end
    subgraph HudumaAgent [Huduma Agent]
        S5["Huduma Agent serves the citizen (verification, pro..."]
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
### Process Name
Service Delivery

### Service Category
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within HUDUMA SECRETARIAT.

### Triggers
- Submission of application/request by Citizen.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

### Policy Context
- The HUDUMA SECRETARIAT Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Citizen | Process Actor | Performs actions as defined in steps. |
| Huduma Agent | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Citizen | Citizen visits Huduma Centre and undergoes security check. | Manual | |
| 2 | Citizen | Citizen proceeds to the Information Desk for guidance and ticket issuance. | Manual | |
| 3 | Citizen | Citizen waits in the waiting area until their ticket number is called/displayed. | Manual | |
| 4 | Citizen | Citizen proceeds to the designated counter for service (e.g., ID replacement, NHIF). | Manual | |
| 5 | Huduma Agent | Huduma Agent serves the citizen (verification, processing, or referral). | Manual | |
| 6 | Citizen | Citizen makes payment via M-Pesa/Posta Pay if applicable. | Manual | |
| 7 | Citizen | Citizen provides feedback on service quality via the terminal. | Manual | |

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

- [https://hudumakenya.go.ke/](https://hudumakenya.go.ke/)

---

## Appendices
See attached ERD and System Design.
