# Auctioneers Licensing Board – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Auctioneers Licensing Board
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Auctioneers Licensing Board is the primary regulatory body for auctioneers in Kenya, established under Section 3(1) of the Auctioneers Act, Cap 1996 of the Laws of Kenya. Its core mandate is to exercise general supervision and control over the business and practice of auctioneers, ensuring high standards of learning, professional competence, and ethical conduct within the profession. The Board plays a crucial role in maintaining public trust and ensuring fair and transparent practices in the disposal of movable and immovable property.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To set, maintain, and continuously improve the standards of learning, professional competence, and professional conduct for the provision of auctioneering services in Kenya; to determine, maintain, and enhance the standards of professional practice and ethical conduct for the auctioneering profession; to issue licenses to individuals and firms who wish to practice as auctioneers; to regulate the licensing and conduct of auctioneers; and to outline the responsibilities of auctioneers, the application process for licenses, and penalties for non-compliance with the Auctioneers Act and associated regulations.

### Legal Context
- Established under Section 3(1) of the Auctioneers Act, Cap 1996 of the Laws of Kenya, which provides the comprehensive legal framework for the Board's regulatory functions over the auctioneering profession. The Board operates under the Ministry of Lands (or the relevant government ministry responsible for land, property, and justice administration) and is crucial for ensuring integrity, fairness, and transparency in processes involving the valuation and disposal of movable and immovable property through auction, thereby protecting the public interest.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Professional [Professional]
        S1["Professional registers on the Board's Online Porta..."]
        S2["Applicant uploads academic certificates and profes..."]
        S4["Applicant pays the registration/annual retention f..."]
    end
    subgraph Board [Board]
        S3["Board Secretariat conducts verification and indexi..."]
        S5["Board gazettes the member and issues the Annual Pr..."]
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
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within Auctioneers Licensing Board.

### Triggers
- Submission of application/request by Professional.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Professional | Process Actor | Performs actions as defined in steps. |
| Board | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Professional | Professional registers on the Board's Online Portal. | Digital | |
| 2 | Professional | Applicant uploads academic certificates and professional testimonials. | Manual | |
| 3 | Board | Board Secretariat conducts verification and indexing. | Manual | |
| 4 | Professional | Applicant pays the registration/annual retention fee. | Manual | |
| 5 | Board | Board gazettes the member and issues the Annual Practicing Certificate. | Manual | |

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

- [https://parliament.go.ke/](https://parliament.go.ke/)
- [https://zhiyanbao.cn/](https://zhiyanbao.cn/)
- [https://uonbi.ac.ke/](https://uonbi.ac.ke/)
- [https://scribd.com/](https://scribd.com/)
