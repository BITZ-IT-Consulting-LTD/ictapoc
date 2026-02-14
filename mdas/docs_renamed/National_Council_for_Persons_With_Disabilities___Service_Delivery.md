# National Council for Persons With Disabilities – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** National Council for Persons With Disabilities
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Social Protection Culture and Recreation' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant visits a gazetted Government Hospital fo..."]
        S3["Applicant submits report to NCPWD via eCitizen or ..."]
    end
    subgraph MoH [MoH]
        S2["Director of Medical Services signs the assessment ..."]
    end
    subgraph NCPWD [NCPWD]
        S4["NCPWD Vetting Committee reviews application."]
        S5["NCPWD issues the Disability ID Card."]
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
- G2C (Government to Citizen)

### Scope
- **In Scope:** End-to-end processing within National Council for Persons With Disabilities.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| MoH | Process Actor | Performs actions as defined in steps. |
| NCPWD | Process Actor | Performs actions as defined in steps. |
| Applicant | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant visits a gazetted Government Hospital for assessment. | Manual | |
| 2 | MoH | Director of Medical Services signs the assessment report. | Manual | |
| 3 | Applicant | Applicant submits report to NCPWD via eCitizen or County Office. | Manual | |
| 4 | NCPWD | NCPWD Vetting Committee reviews application. | Manual | |
| 5 | NCPWD | NCPWD issues the Disability ID Card. | Manual | |

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
