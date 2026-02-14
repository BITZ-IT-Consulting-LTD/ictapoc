# Kenya Investment Authority – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Investment Authority
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya Investment Authority (KenInvest) is a statutory body established under the Investment Promotion Act No. 6 of 2004. Its core mandate is to promote and facilitate both local and foreign investments in Kenya, acting as a one-stop center for investors, thereby improving the investment climate, fostering economic growth, and contributing to job creation and national development.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To promote Kenya as a competitive investment destination globally; to assist investors with business registration, licensing, and navigating regulatory requirements; to provide comprehensive information on investment opportunities, incentives, and the business climate; to advocate for policy reforms that enhance the investment climate; and to offer investor aftercare services to ensure successful project implementation and retention of investments.

### Legal Context
- Established under the Investment Promotion Act No. 6 of 2004, which provides the legal framework for its investment promotion and facilitation activities. Operates under the relevant government ministry responsible for trade and industry, and aligns with national development blueprints like Vision 2030.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Investor [Investor]
        S1["Investor creates account on e-Investment Portal."]
        S2["Investor submits project proposal and proof of inv..."]
        S4["Investor pays the certificate fee."]
    end
    subgraph KenInvest [KenInvest]
        S3["KenInvest appraises the project."]
        S5["KenInvest issues the Investment Certificate."]
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
- **In Scope:** End-to-end processing within Kenya Investment Authority.

### Triggers
- Submission of application/request by Investor.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| KenInvest | Process Actor | Performs actions as defined in steps. |
| Investor | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Investor | Investor creates account on e-Investment Portal. | Digital | |
| 2 | Investor | Investor submits project proposal and proof of investment (min $100k for foreign, KES 1M for local). | Manual | |
| 3 | KenInvest | KenInvest appraises the project. | Manual | |
| 4 | Investor | Investor pays the certificate fee. | Manual | |
| 5 | KenInvest | KenInvest issues the Investment Certificate. | Manual | |

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

- [https://www.invest.go.ke/](https://www.invest.go.ke/)
- [https://saraka.info/](https://saraka.info/)
- [https://unido.org/](https://unido.org/)
- [https://mfa.ir/](https://mfa.ir/)
- [https://eac.int/](https://eac.int/)
- [https://kenyaembassyparis.fr/](https://kenyaembassyparis.fr/)
- [https://investmentkenya.com/](https://investmentkenya.com/)
- [https://investmentpromotion.go.ke/](https://investmentpromotion.go.ke/)
