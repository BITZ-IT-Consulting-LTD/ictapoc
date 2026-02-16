# CBL Bancassurance Intermediary Limited( subsidiary of consolidated Bank) – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** CBL Bancassurance Intermediary Limited( subsidiary of consolidated Bank)
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
CBL Bancassurance Intermediary Limited, a subsidiary of Consolidated Bank of Kenya, operates within the Kenyan financial landscape. Its primary mandate is to distribute a wide array of insurance products through the bank's extensive channels, acting as a crucial intermediary between insurance companies (underwriters) and the bank's diverse clientele. The company aims to provide convenient and accessible insurance services, drive significant business growth and profitability for the Consolidated Bank Group, and offer professional insurance advisory services across various categories, thereby enhancing customer value and financial inclusion.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To formulate and execute the overall strategy for the bank's bancassurance offerings across various insurance products, customer propositions, and distribution channels; to drive growth in business volumes with the goal of making bancassurance a significant contributor to the Consolidated Bank's profitability; to effectively manage bancassurance income and achieve profit and loss targets; to negotiate pricing structures for bancassurance products and services, and serve as a key interface with insurance partners and industry associations; to review bancassurance strategy and performance, providing leadership, and spearheading the implementation of quality operational standards, risk management frameworks, and compliance protocols; to offer professional insurance advisory services to individual, SME, and corporate bank customers; to facilitate access to a comprehensive range of insurance policies, including motor, non-motor, marine, agriculture, medical, life, and pensions; and to provide efficient claims services, risk management solutions, and insurance premium financing.

### Legal Context
- Operating as a subsidiary of Consolidated Bank of Kenya, CBL Bancassurance Intermediary Limited is regulated by the Insurance Regulatory Authority (IRA) under the Insurance Act (Cap 487) for its intermediary activities. Additionally, its operations are subject to oversight by the Central Bank of Kenya (CBK) through guidelines issued to banks engaging in bancassurance business. This dual regulatory framework ensures compliance, consumer protection, and financial stability within the Kenyan financial and insurance sectors.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant submits loan/grant application form with..."]
    end
    subgraph Agency [Agency]
        S2["Agency conducts desk appraisal and credit scoring."]
        S5["Funds are disbursed to the applicant's account."]
    end
    subgraph FieldOfficer [Field Officer]
        S3["Field officer visits for due diligence (if applica..."]
    end
    subgraph Committee [Committee]
        S4["Committee approves the facility/grant."]
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
- **In Scope:** End-to-end processing within CBL Bancassurance Intermediary Limited( subsidiary of consolidated Bank).

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Committee | Process Actor | Performs actions as defined in steps. |
| Applicant | Process Actor | Performs actions as defined in steps. |
| Field Officer | Process Actor | Performs actions as defined in steps. |
| Agency | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Loan/Service Application Form, Business Proposal / Plan, Financial Statements / Bank Records, Collateral / Security Documents
- **Outputs:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant submits loan/grant application form with business proposal. | Manual | |
| 2 | Agency | Agency conducts desk appraisal and credit scoring. | Manual | |
| 3 | Field Officer | Field officer visits for due diligence (if applicable). | Manual | |
| 4 | Committee | Committee approves the facility/grant. | Manual | |
| 5 | Agency | Funds are disbursed to the applicant's account. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Lengthy credit appraisal processes.
- Manual debt collection and reconciliation.
- High paperwork for loan processing.
- Lack of 360-degree customer view.

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

- [https://www.consolidated-bank.com/](https://www.consolidated-bank.com/)
- [https://kenyainsurers.com/](https://kenyainsurers.com/)
- [https://ncbagroup.com/](https://ncbagroup.com/)
- [https://co-opbank.co.ke/](https://co-opbank.co.ke/)
