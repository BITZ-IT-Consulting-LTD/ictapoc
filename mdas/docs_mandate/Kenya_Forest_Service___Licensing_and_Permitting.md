# Kenya Forest Service – Licensing and Permitting

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Forest Service
- **Process Name:** Licensing and Permitting
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya Forest Service (KFS) is a state corporation established under the Forests Act of 2005 and formalized by the Forest Conservation and Management Act of 2016. Its mandate is to provide for the development and sustainable management, including conservation and rational utilization, of all forest resources for the socio-economic development of Kenya and for environmental benefits such as water catchment protection and carbon sequestration.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To conserve, protect, and manage all public forests; to prepare and implement management plans for forest resources; to regulate the use of forest resources through licenses and permits; to promote forestry education and training; to manage critical water catchment areas; to rehabilitate degraded forest areas; to increase national forest cover; and to protect and secure forest assets, thereby ensuring sustainable forest management for national development and environmental well-being.

### Legal Context
- Established under the Forests Act of 2005 and subsequently formalized by the Forest Conservation and Management Act of 2016. These Acts provide the comprehensive legal framework for the conservation, management, and sustainable utilization of forest resources in Kenya.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Transporter [Transporter]
        S1["Transporter applies for a Movement Permit at the F..."]
        S3["Transporter pays the movement fees via M-Pesa."]
    end
    subgraph KFSOfficer [KFS Officer]
        S2["Forest Officer inspects the forest produce and ver..."]
        S4["Forest Officer issues the Movement Permit specifyi..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> End((End))
```

---

## Process Overview
### Service Category
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within Kenya Forest Service.

### Triggers
- Submission of application/request by Transporter.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| KFS Officer | Process Actor | Performs actions as defined in steps. |
| Transporter | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Transporter | Transporter applies for a Movement Permit at the Forest Station. | Manual | |
| 2 | KFS Officer | Forest Officer inspects the forest produce and verifies origin. | Manual | |
| 3 | Transporter | Transporter pays the movement fees via M-Pesa. | Manual | |
| 4 | KFS Officer | Forest Officer issues the Movement Permit specifying route and validity. | Manual | |

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

- [https://www.kenyaforestservice.org/](https://www.kenyaforestservice.org/)
- [https://ecitizen.go.ke/](https://ecitizen.go.ke/)
- [https://afro.co.ke/](https://afro.co.ke/)
- [https://chm-cbd.net/](https://chm-cbd.net/)
