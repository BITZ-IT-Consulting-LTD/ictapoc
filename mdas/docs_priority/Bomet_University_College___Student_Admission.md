# Bomet University College – Student Admission

## Cover Page
- **Ministry/Department/Agency (MDA):** Bomet University College
- **Process Name:** Student Admission
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Bomet University (formerly Bomet University College) is a public university in Kenya, established as a Constituent College of Moi University in 2017 and later granted a Charter on February 4, 2026, making it an independent university and the 36th public university in Kenya. It is the first public university in Bomet County. Its vision is to be a premier Green University fostering research excellence in Science, Technology, and Innovation for sustainability, providing quality education, and nurturing critical inquiry, creativity, and engagement for social transformation and the advancement of humanity.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To provide quality education and foster innovation across a diverse range of academic programs, including certificate, diploma, undergraduate, and postgraduate courses, in various schools such as Arts and Social Sciences, Pure & Applied Sciences, Business and Entrepreneurship, and Education; to develop creativity and innovation in students to prepare them for the job market; to adopt a practical learning approach emphasizing attachments and fieldwork, and integrating ICT into student training; to champion quality education, sustainability, and innovation within Kenya's higher education sector; to foster creative and critical thinking, contributing to the discovery, preservation, and dissemination of knowledge; to stimulate students' intellectual engagement in economic, socio-cultural, scientific, and technological development; and to operate with a niche in 'Green Economy for Sustainability' and a motto of 'Green University for Sustainability'.

### Legal Context
- Established as a Constituent College of Moi University under Legal Notice Number 145 of July 27, 2017, and subsequently granted a Charter on February 4, 2026, making it an independent university. Bomet University operates under the Universities Act, 2012, and relevant higher education regulations. It aligns its mandates with Kenya's national development agenda, including Vision 2030 and the Bottom-Up Economic Transformation Agenda (BETA), with a specific focus on contributing to sustainable development through its 'Green Economy for Sustainability' niche.

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
- **In Scope:** End-to-end processing within Bomet University College.

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

- [https://www.bu.ac.ke/](https://www.bu.ac.ke/)
- [https://bomet.co.ke/](https://bomet.co.ke/)
- [https://wikipedia.org/](https://wikipedia.org/)
- [https://somo.co.ke/](https://somo.co.ke/)
