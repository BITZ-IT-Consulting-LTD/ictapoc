# Kenya Dairy Board – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Dairy Board
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya Dairy Board (KDB) is a parastatal operating under the Ministry of Agriculture, Livestock, Fisheries, and Cooperatives (State Department of Livestock). Its primary mandate is to regulate and promote the dairy sector in Kenya, ensuring the quality and safety of milk and milk products for consumers, and fostering sustainable growth and development within the industry.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To enforce compliance with regulations to ensure the quality and safety of milk and milk products; license participants across the dairy value chain; educate stakeholders on best handling and marketing practices; conduct research to inform policies; collaborate with partners to strengthen milk quality and processing; and promote sustainable dairy development by advancing breeding, farm management, and access to improved technologies.

### Legal Context
- Operates under the authority of the Dairy Industry Act, which provides the legal basis for its regulatory functions. Various regulations have been developed under this Act to guide its work in the dairy sector. It is a parastatal under the Ministry of Agriculture, Livestock, Fisheries, and Cooperatives (State Department of Livestock).

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Trader [Trader]
        S1["Trader applies for license via KDB portal."]
        S3["Upon compliance, trader pays the license fee."]
    end
    subgraph KDBInspector [KDB Inspector]
        S2["KDB inspectors inspect the premises/vehicle/contai..."]
    end
    subgraph KDB [KDB]
        S4["KDB issues the Milk Trader License."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> End((End))
```

---

## Process Overview
### Service Category
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within Kenya Dairy Board.

### Triggers
- Submission of application/request by Trader.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| KDB | Process Actor | Performs actions as defined in steps. |
| Trader | Process Actor | Performs actions as defined in steps. |
| KDB Inspector | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Trader | Trader applies for license via KDB portal. | Digital | |
| 2 | KDB Inspector | KDB inspectors inspect the premises/vehicle/containers. | Manual | |
| 3 | Trader | Upon compliance, trader pays the license fee. | Manual | |
| 4 | KDB | KDB issues the Milk Trader License. | Manual | |

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

- [https://youtube.com/](https://youtube.com/)
- [https://kakamega.go.ke/](https://kakamega.go.ke/)
