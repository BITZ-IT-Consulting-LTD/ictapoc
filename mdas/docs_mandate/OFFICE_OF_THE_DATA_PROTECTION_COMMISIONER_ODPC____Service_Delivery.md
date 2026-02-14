# OFFICE OF THE DATA PROTECTION COMMISIONER (ODPC) – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** OFFICE OF THE DATA PROTECTION COMMISIONER (ODPC)
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Office of the Data Protection Commissioner (ODPC) in Kenya is responsible for regulating the processing of personal data, protecting individual privacy, and ensuring compliance with the Data Protection Act, 2019. It acts as an oversight body, promotes self-regulation, and investigates data protection infringements.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To oversee and enforce the implementation of the Data Protection Act, 2019, ensuring appropriate handling of personal data, protecting the privacy of individuals, and establishing robust legal and institutional mechanisms for data protection in Kenya.

### Legal Context
- Established and mandated under the Data Protection Act, 2019, which provides the legal framework for personal data protection in Kenya.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Customer [Customer]
        S1["Customer/Stakeholder submits request, application,..."]
    end
    subgraph Registry [Registry]
        S2["Registry/Front Office receives, records, and class..."]
    end
    subgraph TechnicalOfficer [Technical Officer]
        S3["Relevant Technical Department reviews the request ..."]
    end
    subgraph Management [Management]
        S4["Management/Accounting Officer approves the appropr..."]
    end
    subgraph CustomerCare [Customer Care]
        S5["Service is delivered or official response is commu..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> End((End))
```

---

## Process Overview
### Service Category
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within OFFICE OF THE DATA PROTECTION COMMISIONER (ODPC).

### Triggers
- Submission of application/request by Customer.

### End States
- **Successful:** Policy Guidelines / Circulars, Official Response Letters, Cabinet Resolutions, Public Service Reports

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Registry | Process Actor | Performs actions as defined in steps. |
| Management | Process Actor | Performs actions as defined in steps. |
| Customer | Process Actor | Performs actions as defined in steps. |
| Customer Care | Process Actor | Performs actions as defined in steps. |
| Technical Officer | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Public Inquiries / Petitions, Policy Proposals / Memos, Inter-agency Correspondence, Cabinet Memos
- **Outputs:** Policy Guidelines / Circulars, Official Response Letters, Cabinet Resolutions, Public Service Reports

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Customer | Customer/Stakeholder submits request, application, or inquiry via official channels (Email, Letter, or Portal). | Digital | |
| 2 | Registry | Registry/Front Office receives, records, and classifies the request. | Manual | |
| 3 | Technical Officer | Relevant Technical Department reviews the request against internal policies and regulations. | Manual | |
| 4 | Management | Management/Accounting Officer approves the appropriate action or service delivery. | Manual | |
| 5 | Customer Care | Service is delivered or official response is communicated to the customer. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Slow movement of physical files (Bureaucracy).
- Loss of institutional memory (Manual registries).
- Difficulty in tracking correspondence status.
- Siloed operations between departments.

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

- [https://odpc.go.ke/](https://odpc.go.ke/)
