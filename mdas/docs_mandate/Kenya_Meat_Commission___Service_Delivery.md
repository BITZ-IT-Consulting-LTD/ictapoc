# Kenya Meat Commission – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Meat Commission
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya Meat Commission (KMC) is a state-owned enterprise established in 1950 under the Kenya Meat Commission Act. Its primary mandate is to provide a ready and reliable market for livestock farmers and to process and supply high-quality meat and meat products to consumers both domestically and for export. KMC aims to enhance Kenya's meat industry through efficient operations, quality assurance, and value addition, contributing significantly to national food security and economic development.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To operate modern abattoirs and meat processing facilities for local and export markets; to ensure and maintain high standards of meat quality, safety, and hygiene through rigorous inspection and grading; to purchase livestock from farmers to stabilize market prices and stimulate production; to promote and facilitate the export of processed meat products; to conduct research and development to improve meat production and processing techniques; to provide advisory services and support to livestock farmers; and to act as a buyer of last resort during livestock crises to prevent losses and ensure food security.

### Legal Context
- Established under the Kenya Meat Commission Act (1950), which provides its legal framework. Its mission is aligned with contributing to national food security, improving livelihoods, and achieving financial self-sustainability within the meat sector. Operates under the relevant government ministry responsible for agriculture and livestock development.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Farmer [Farmer]
        S1["Farmer delivers livestock to KMC depot/factory."]
    end
    subgraph KMCVet [KMC Vet]
        S2["KMC Vets inspect animals for health and quality (A..."]
    end
    subgraph KMCWeighbridge [KMC Weighbridge]
        S3["Animals are weighed to determine purchase price."]
    end
    subgraph KMCOperations [KMC Operations]
        S4["Animals are slaughtered and processed."]
    end
    subgraph KMCFinance [KMC Finance]
        S5["Payment is processed to the farmer's bank account."]
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
- **In Scope:** End-to-end processing within Kenya Meat Commission.

### Triggers
- Submission of application/request by Farmer.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| KMC Operations | Process Actor | Performs actions as defined in steps. |
| KMC Vet | Process Actor | Performs actions as defined in steps. |
| Farmer | Process Actor | Performs actions as defined in steps. |
| KMC Weighbridge | Process Actor | Performs actions as defined in steps. |
| KMC Finance | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Farmer | Farmer delivers livestock to KMC depot/factory. | Manual | |
| 2 | KMC Vet | KMC Vets inspect animals for health and quality (Ante-mortem). | Manual | |
| 3 | KMC Weighbridge | Animals are weighed to determine purchase price. | Manual | |
| 4 | KMC Operations | Animals are slaughtered and processed. | Manual | |
| 5 | KMC Finance | Payment is processed to the farmer's bank account. | Manual | |

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

- [https://kenyameat.co.ke/](https://kenyameat.co.ke/)
- [https://saraka.info/](https://saraka.info/)
- [https://agrarian.co.ke/](https://agrarian.co.ke/)
