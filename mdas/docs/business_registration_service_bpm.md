# STANDARD BPM TEMPLATE – Business Registration Service

## Cover Page
- **Ministry/Department/Agency (MDA):** Business Registration Service
- **Process Name:** To ensure the effective administration of laws concerning the incorporation, registration, operation, and management of companies, partnerships, and firms; to maintain comprehensive registers, data, and records of all registrations; and to provide quality business support services throughout the business lifecycle in Kenya.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Business Registration Service (BRS) in Kenya is a State Corporation established under the Business Registration Service Act, 2015. Its core mandate is to administer policies, laws, and other matters related to business registration, thereby improving the ease of doing business in Kenya and fostering economic growth through effective oversight of companies, partnerships, and firms.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant logs into the eCitizen BRS portal."]
        S2["Applicant conducts a Business Name Search and rese..."]
        S3["Applicant selects 'Business Name Registration' (BN..."]
        S4["Applicant fills the online form (nature of busines..."]
        S5["Applicant uploads scanned IDs and passport photos ..."]
        S6["Applicant pays the registration fee via M-Pesa."]
        S8["Applicant downloads the Certificate of Registratio..."]
    end
    subgraph RegistrarofCompanies [Registrar of Companies]
        S7["Registrar reviews and approves the application."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> End((End))
```

---

## Process Overview
### Process Name
To ensure the effective administration of laws concerning the incorporation, registration, operation, and management of companies, partnerships, and firms; to maintain comprehensive registers, data, and records of all registrations; and to provide quality business support services throughout the business lifecycle in Kenya.

### Service Category
- G2C (Government to Citizen)

### Process Objective
- To ensure the effective administration of laws concerning the incorporation, registration, operation, and management of companies, partnerships, and firms; to maintain comprehensive registers, data, and records of all registrations; and to provide quality business support services throughout the business lifecycle in Kenya.

### Scope
- **In Scope:** End-to-end processing within Business Registration Service.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Business Registration Service Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| Registrar of Companies | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant logs into the eCitizen BRS portal. | Digital | |
| 2 | Applicant | Applicant conducts a Business Name Search and reserves a name. | Manual | |
| 3 | Applicant | Applicant selects 'Business Name Registration' (BN2) once the name is approved. | Manual | |
| 4 | Applicant | Applicant fills the online form (nature of business, address, partners' details). | Manual | |
| 5 | Applicant | Applicant uploads scanned IDs and passport photos of partners. | Manual | |
| 6 | Applicant | Applicant pays the registration fee via M-Pesa. | Manual | |
| 7 | Registrar of Companies | Registrar reviews and approves the application. | Manual | |
| 8 | Applicant | Applicant downloads the Certificate of Registration. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Manual document verification takes time.
- High cost and time for physical inspections.
- Risk of counterfeit licenses/certificates.
- Lack of real-time monitoring of licensees.

### Opportunities
- Online Licensing Management System (LMS).
- Integration with IPRS and BRS for auto-verification.
- Mobile field inspection apps with GIS.
- QR-coded verifiable certificates.

---

## KPIs
| KPI | Baseline | Target |
|---|---|---|
| Turnaround Time | 30 Days | 5 Days |
| CSAT | 50% | 90% |
