# National Treasury and Economic Planning, The – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** National Treasury and Economic Planning, The
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Public Administration and International Relations' cluster for balanced coverage; entity type: Ministry. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the AS-IS process flow across different actors.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph MDACounty [MDA/County]
        S1["MDA/County submits Cash Flow Plan and Exchequer Re..."]
    end
    subgraph BudgetDept [Budget Dept]
        S2["Treasury Budget Department reviews requisition aga..."]
    end
    subgraph AGSD [AGSD]
        S3["Accountant General Services Department (AGSD) proc..."]
    end
    subgraph COB [COB]
        S4["Controller of Budget (COB) approves the withdrawal..."]
    end
    subgraph Treasury [Treasury]
        S5["Treasury releases funds to the MDA/County Central ..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> End((End))
```

---

## Process Overview
### Process Name
Service Delivery

### Service Category
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within National Treasury and Economic Planning, The.

### Triggers
- Submission of application/request by MDA/County.

### End States
- **Successful:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

### Policy Context
- The National Treasury and Economic Planning, The Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| MDA/County | Process Actor | Performs actions as defined in steps. |
| Treasury | Process Actor | Performs actions as defined in steps. |
| COB | Process Actor | Performs actions as defined in steps. |
| AGSD | Process Actor | Performs actions as defined in steps. |
| Budget Dept | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Loan/Service Application Form, Business Proposal / Plan, Financial Statements / Bank Records, Collateral / Security Documents
- **Outputs:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | MDA/County | MDA/County submits Cash Flow Plan and Exchequer Requisition to Treasury. | Manual | |
| 2 | Budget Dept | Treasury Budget Department reviews requisition against approved estimates. | Manual | |
| 3 | AGSD | Accountant General Services Department (AGSD) processes the payment voucher. | Manual | |
| 4 | COB | Controller of Budget (COB) approves the withdrawal. | Manual | |
| 5 | Treasury | Treasury releases funds to the MDA/County Central Bank account via IFMIS. | Manual | |

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

- Official Mandate and Service Charter (Inferred from Statutory Acts).

---

## Appendices
See attached ERD and System Design.
