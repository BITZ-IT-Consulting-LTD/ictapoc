# National Social Security Fund – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** National Social Security Fund
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The National Social Security Fund (NSSF) is a statutory public institution in Kenya mandated to provide social security protection to all workers, encompassing both the formal and informal sectors. Established initially as a Provident Fund in 1965, NSSF transitioned into a Pension Scheme in 2014 following the enactment of the NSSF Act, No. 45 of 2013. Its core purpose is to guarantee basic compensation in cases of permanent disability, provide assistance to needy dependents in the event of death, and offer a monthly life pension upon retirement. Beyond these direct benefits, NSSF also mobilizes domestic savings, aids in poverty reduction, fosters financial inclusion, and helps decrease the national dependency ratio.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To register eligible individuals for social security across all sectors; to efficiently receive and manage contributions from its members and their employers; to oversee the funds of the scheme to ensure their sustainability, growth, and proper investment; to process and disburse various benefits, including retirement, survivor, and invalidity benefits, to eligible members or their dependents in a timely manner; to guarantee basic compensation in cases of permanent disability; to provide assistance to needy dependents in the event of a member's death; to offer a monthly life pension upon retirement to ensure income security; to mobilize domestic savings for national development; to aid in poverty reduction by providing a social safety net; to foster financial inclusion by reaching out to the informal sector; and to decrease the dependency ratio by encouraging self-reliance in old age.

### Legal Context
- Initially established in 1965 as a Provident Fund, NSSF transitioned into a Pension Scheme in 2014 following the enactment of the NSSF Act, No. 45 of 2013, which provides the current legal framework for its operations. NSSF operates under the Ministry of Labour and Social Protection (or the relevant government ministry responsible for social protection) and is guided by national social security policies and labor laws aimed at expanding social protection coverage and ensuring the well-being of Kenyan workers and their families.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant accesses NSSF Self Service Portal or USS..."]
        S2["Applicant enters National ID/Alien ID number and d..."]
        S5["Applicant prints the NSSF card/membership details."]
    end
    subgraph System [System]
        S3["System validates details from IPRS."]
        S4["System generates NSSF Number immediately."]
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
- **In Scope:** End-to-end processing within National Social Security Fund.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| System | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Loan/Service Application Form, Business Proposal / Plan, Financial Statements / Bank Records, Collateral / Security Documents
- **Outputs:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant accesses NSSF Self Service Portal or USSD. | Digital | |
| 2 | Applicant | Applicant enters National ID/Alien ID number and details. | Manual | |
| 3 | System | System validates details from IPRS. | Manual | |
| 4 | System | System generates NSSF Number immediately. | Manual | |
| 5 | Applicant | Applicant prints the NSSF card/membership details. | Manual | |

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

- [https://www.nssf.or.ke/](https://www.nssf.or.ke/)
- [https://mygov.go.ke/](https://mygov.go.ke/)
- [https://ecitizen.go.ke/](https://ecitizen.go.ke/)
- [https://sokodirectory.com/](https://sokodirectory.com/)
- [https://cytonn.com/](https://cytonn.com/)
