# Kenya Maritime Authority – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Maritime Authority
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya Maritime Authority (KMA) is a statutory authority established under the Kenya Maritime Authority Act 2006. Its primary mandate is to regulate, coordinate, and oversee maritime affairs in the Republic of Kenya, ensuring shipping safety, promoting seafarer welfare, protecting the marine environment, and facilitating maritime trade and investment in compliance with national and international standards.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To administer and enforce the Merchant Shipping Act, 2009, and other related regulations and international maritime conventions; to manage maritime search and rescue operations; to ensure shipping safety and security; to oversee the training, recruitment, and welfare of seafarers; to investigate maritime casualties; to develop national oil spill contingency plans; to maintain and administer a national ship register; and to advise the government on all matters pertaining to maritime affairs and legislation.

### Legal Context
- Established under the Kenya Maritime Authority Act 2006. Administers and enforces the Merchant Shipping Act, 2009, and other related national laws and international maritime conventions, treaties, and agreements. Operates under the relevant government ministry responsible for maritime affairs.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Seafarer [Seafarer]
        S1["Seafarer undergoes mandatory training at an approv..."]
        S2["Seafarer applies to KMA for Certificate of Compete..."]
        S3["Seafarer undergoes medical fitness examination."]
    end
    subgraph KMA [KMA]
        S4["KMA verifies training and medical records."]
        S5["KMA conducts oral/written examination (for officer..."]
        S6["KMA issues the Seafarer Certificate."]
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
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within Kenya Maritime Authority.

### Triggers
- Submission of application/request by Seafarer.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| KMA | Process Actor | Performs actions as defined in steps. |
| Seafarer | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Seafarer | Seafarer undergoes mandatory training at an approved maritime institution. | Manual | |
| 2 | Seafarer | Seafarer applies to KMA for Certificate of Competency (CoC) or Proficiency. | Manual | |
| 3 | Seafarer | Seafarer undergoes medical fitness examination. | Manual | |
| 4 | KMA | KMA verifies training and medical records. | Manual | |
| 5 | KMA | KMA conducts oral/written examination (for officers). | Manual | |
| 6 | KMA | KMA issues the Seafarer Certificate. | Manual | |

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

- [https://kma.go.ke/](https://kma.go.ke/)
- [https://saraka.info/](https://saraka.info/)
