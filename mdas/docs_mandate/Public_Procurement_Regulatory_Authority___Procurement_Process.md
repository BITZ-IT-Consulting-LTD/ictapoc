# Public Procurement Regulatory Authority – Procurement Process

## Cover Page
- **Ministry/Department/Agency (MDA):** Public Procurement Regulatory Authority
- **Process Name:** Procurement Process
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Public Procurement Regulatory Authority (PPRA) is an autonomous government agency in Kenya established under Section 8 of the Public Procurement and Asset Disposal Act, 2015. Its primary mandate is to monitor, assess, and report on the overall functioning of the public procurement and asset disposal system in Kenya. PPRA ensures that procuring entities adhere to national values, constitutional provisions, and principles of fairness, equity, transparency, competition, and cost-effectiveness, thereby promoting sustainable development and safeguarding public resources.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To monitor, assess, and review the public procurement and asset disposal system to ensure compliance with national values and constitutional provisions, and make recommendations for improvements; to develop procurement policies, regulations, and guidelines; to monitor and evaluate procurement performance to ensure compliance with procurement laws and regulations, and enforce standards by imposing sanctions for non-compliance; to investigate and resolve complaints and disputes related to procurement processes; to develop, promote, and support the training and capacity development of individuals involved in procurement and asset disposal; to provide guidance and technical support to public institutions on procurement matters; to promote the participation of disadvantaged groups (women, youth, and persons with disabilities) in public procurement through preferential policies; to promote the use of technology in procurement processes; to report to Parliament and relevant county assemblies on the functioning of the procurement system; to develop a code of ethics to guide procuring entities and bidders; to collaborate with state and non-state actors to improve public procurement and disposal; to maintain and update supplier and contractor databases, and develop standard procurement documents; and to conduct market research and procurement audits.

### Legal Context
- Established under Section 8 of the Public Procurement and Asset Disposal Act, 2015 (PPAD Act, 2015), which provides the comprehensive legal framework for public procurement and asset disposal in Kenya. PPRA operates under the oversight of the National Treasury and is crucial for upholding Article 227 of the Constitution of Kenya, 2010, which mandates that public procurement systems be fair, equitable, transparent, competitive, and cost-effective. Its functions ensure adherence to international best practices in public procurement.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant registers business on AGPO Portal."]
        S2["Applicant uploads ID, Business Reg Cert, and Tax C..."]
        S5["Applicant downloads the AGPO Certificate."]
    end
    subgraph PPRA [PPRA]
        S3["PPRA/Treasury verifies documents."]
    end
    subgraph System [System]
        S4["System approves application."]
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
- **In Scope:** End-to-end processing within Public Procurement Regulatory Authority.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| System | Process Actor | Performs actions as defined in steps. |
| PPRA | Process Actor | Performs actions as defined in steps. |
| Applicant | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant registers business on AGPO Portal. | Digital | |
| 2 | Applicant | Applicant uploads ID, Business Reg Cert, and Tax Compliance Cert. | Manual | |
| 3 | PPRA | PPRA/Treasury verifies documents. | Manual | |
| 4 | System | System approves application. | Manual | |
| 5 | Applicant | Applicant downloads the AGPO Certificate. | Manual | |

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

- [https://www.ppra.go.ke/](https://www.ppra.go.ke/)
- [https://afro.co.ke/](https://afro.co.ke/)
- [https://majira.co.ke/](https://majira.co.ke/)
