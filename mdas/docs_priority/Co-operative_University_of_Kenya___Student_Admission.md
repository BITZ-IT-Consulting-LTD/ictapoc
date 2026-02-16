# Co-operative University of Kenya – Student Admission

## Cover Page
- **Ministry/Department/Agency (MDA):** Co-operative University of Kenya
- **Process Name:** Student Admission
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Co-operative University of Kenya (CUK) is a premier public university in Kenya, established with a mission to provide quality education, training, research, and consultancy, particularly in co-operative development, business, and related fields. CUK aims to be a leading institution in cooperative training, education, research, and innovation, nurturing an intellectual culture that combines theoretical understanding with practical application, innovation, and entrepreneurship. Through its specialized focus, CUK contributes significantly to national and global development by strengthening the cooperative movement and producing skilled human capital.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To provide quality university education, training, research, and consultancy in co-operative development, business, and related fields; to advance learning and knowledge through rigorous research and innovation; to offer comprehensive academic programs across Diploma, Undergraduate, and Postgraduate levels; to support student services including access to student portals, e-learning platforms, and library resources; to facilitate community engagement and outreach programs, empowering communities through specialized consultancy services; to disseminate knowledge for effective leadership in higher education, training, research, and outreach; and to foster an intellectual culture that combines theoretical understanding with practical application, innovation, and entrepreneurship, contributing to sustainable national and global development.

### Legal Context
- Established as a public university under the Universities Act, 2012, and other relevant higher education regulations, which provide the legal and regulatory framework for its establishment and functions. CUK operates under the Ministry of Education and is crucial for implementing national development agendas, including Vision 2030, and policies aimed at strengthening the cooperative movement, enhancing financial inclusion, and promoting sustainable development in Kenya. The university is governed by its charter and council.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Student [Student]
        S1["Student receives placement notification via KUCCPS..."]
        S2["Student logs into the Institution's Student Portal..."]
        S3["Student pays tuition and statutory fees via Bank o..."]
        S4["Student physically reports to the institution for ..."]
        S6["Student is issued a Student ID card."]
    end
    subgraph Registrar [Registrar]
        S5["Institution registers the student in the ERP syste..."]
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
- G2C (Government to Citizen)

### Scope
- **In Scope:** End-to-end processing within Co-operative University of Kenya.

### Triggers
- Submission of application/request by Student.

### End States
- **Successful:** Admission Letter, Student ID Card, Academic Transcripts, Degree/Diploma Certificate

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Student | Process Actor | Performs actions as defined in steps. |
| Registrar | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** KCSE/Academic Result Slips, National ID / Birth Certificate, Student Personal Details Form, Fee Payment Receipts
- **Outputs:** Admission Letter, Student ID Card, Academic Transcripts, Degree/Diploma Certificate

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Student | Student receives placement notification via KUCCPS or applies directly as Self-Sponsored. | Manual | |
| 2 | Student | Student logs into the Institution's Student Portal to accept admission and download Admission Letter. | Digital | |
| 3 | Student | Student pays tuition and statutory fees via Bank or eCitizen. | Manual | |
| 4 | Student | Student physically reports to the institution for document verification (original slips, certs). | Manual | |
| 5 | Registrar | Institution registers the student in the ERP system. | Manual | |
| 6 | Student | Student is issued a Student ID card. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Long queues during admission and registration.
- Manual reconciliation of fee payments.
- Delays in processing exam results and transcripts.
- Fragmented student data across departments.

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
        S2["Applicant enters National ID; System auto-populate..."]
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
The To-Be process leverages the Government Service Bus to integrate with IPRS (Identity Registry) and the Payment Gateway. Manual data entry and document uploads are replaced by real-time API validations, enabling a paperless, cashless, and presence-less service experience.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Applicant | Applicant logs in via Single Sign-On (SSO) and selects the service. | Citizen Portal / SSO |
| 2 | System | Applicant enters National ID; System auto-populates details from IPRS (Identity Registry) via the Service Bus. | Service Bus / Registry API |
| 3 | System | System performs auto-validation of compliance (e.g., KRA Tax Status) via Inter-Agency APIs. | Service Bus / Compliance Engine |
| 4 | Applicant | Applicant pays fees via the Government Payment Gateway; System auto-receipts. | Payment Gateway |
| 5 | System | Application is processed by the Rules Engine. (Low-risk cases are Auto-Approved). | Workflow Engine |
| 6 | Officer | Complex cases are routed to the Officer Workbench for digital review and approval. | Officer Workbench |
| 7 | System | System generates a Verifiable Digital Certificate (QR Code) and notifies the applicant. | Output Generator |

---

## References & Evidence
The information in this document was derived from the following official sources:

- [https://www.cuk.ac.ke/](https://www.cuk.ac.ke/)
- [https://devex.com/](https://devex.com/)
- [https://youtube.com/](https://youtube.com/)
- [https://studzona.com/](https://studzona.com/)
- [https://unirank.org/](https://unirank.org/)
