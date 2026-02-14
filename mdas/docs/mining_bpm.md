# STANDARD BPM TEMPLATE – Mining

## Cover Page
- **Ministry/Department/Agency (MDA):** Mining
- **Process Name:** Represents 'Environment Protection Water and Natural Resources' cluster for balanced coverage; entity type: Department. Included as Tier 3 for light‑touch desk review/survey.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Environment Protection Water and Natural Resources' cluster for balanced coverage; entity type: Department. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant registers on the Mining Cadastre Portal."]
        S2["Applicant applies for a Prospecting or Mining Lice..."]
        S4["Applicant pays the application fee."]
    end
    subgraph System [System]
        S3["System checks for overlapping coordinates/rights."]
    end
    subgraph MRB [MRB]
        S5["Mineral Rights Board reviews and recommends approv..."]
    end
    subgraph CSMining [CS Mining]
        S6["Cabinet Secretary grants the license."]
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
### Process Name
Represents 'Environment Protection Water and Natural Resources' cluster for balanced coverage; entity type: Department. Included as Tier 3 for light‑touch desk review/survey.

### Service Category
- G2C/G2B

### Process Objective
- Represents 'Environment Protection Water and Natural Resources' cluster for balanced coverage; entity type: Department. Included as Tier 3 for light‑touch desk review/survey.

### Scope
- **In Scope:** End-to-end processing within Mining.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Mining Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| CS Mining | Process Actor | Performs actions as defined in steps. |
| MRB | Process Actor | Performs actions as defined in steps. |
| System | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant registers on the Mining Cadastre Portal. | Digital | |
| 2 | Applicant | Applicant applies for a Prospecting or Mining License. | Manual | |
| 3 | System | System checks for overlapping coordinates/rights. | Manual | |
| 4 | Applicant | Applicant pays the application fee. | Manual | |
| 5 | MRB | Mineral Rights Board reviews and recommends approval. | Manual | |
| 6 | CS Mining | Cabinet Secretary grants the license. | Manual | |

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
