# STANDARD BPM TEMPLATE – Technical and Vocational Education and Training Authority

## Cover Page
- **Ministry/Department/Agency (MDA):** Technical and Vocational Education and Training Authority
- **Process Name:** Represents 'Education' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Education' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Institution [Institution]
        S1["Institution applies for registration/accreditation..."]
        S2["Institution conducts and submits a Self-Assessment..."]
    end
    subgraph TVETA [TVETA]
        S3["TVETA conducts desk review of the application."]
    end
    subgraph TVETAInspectors [TVETA Inspectors]
        S4["TVETA conducts physical inspection of facilities a..."]
    end
    subgraph TVETABoard [TVETA Board]
        S5["TVETA Board approves accreditation and issues Cert..."]
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
Represents 'Education' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Service Category
- G2B (Government to Business)

### Process Objective
- Represents 'Education' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Scope
- **In Scope:** End-to-end processing within Technical and Vocational Education and Training Authority.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Institution.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Technical and Vocational Education and Training Authority Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Institution | Process Actor | Performs actions as defined in steps. |
| TVETA Inspectors | Process Actor | Performs actions as defined in steps. |
| TVETA | Process Actor | Performs actions as defined in steps. |
| TVETA Board | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Institution | Institution applies for registration/accreditation via TVETA MIS. | Manual | |
| 2 | Institution | Institution conducts and submits a Self-Assessment Report. | Manual | |
| 3 | TVETA | TVETA conducts desk review of the application. | Manual | |
| 4 | TVETA Inspectors | TVETA conducts physical inspection of facilities and curriculum. | Manual | |
| 5 | TVETA Board | TVETA Board approves accreditation and issues Certificate. | Manual | |

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
