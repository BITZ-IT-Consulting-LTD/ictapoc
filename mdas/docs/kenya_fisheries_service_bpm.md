# STANDARD BPM TEMPLATE – Kenya Fisheries Service

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Fisheries Service
- **Process Name:** Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Owner [Owner]
        S1["Vessel owner applies for a fishing license."]
        S3["Owner pays the license fee."]
    end
    subgraph KeFSInspector [KeFS Inspector]
        S2["KeFS conducts vessel inspection for safety and gea..."]
    end
    subgraph KeFS [KeFS]
        S4["KeFS Director General approves and issues the lice..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> End((End))
```

---

## Process Overview
### Process Name
Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Service Category
- G2C/G2B

### Process Objective
- Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Scope
- **In Scope:** End-to-end processing within Kenya Fisheries Service.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Owner.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Kenya Fisheries Service Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| KeFS | Process Actor | Performs actions as defined in steps. |
| KeFS Inspector | Process Actor | Performs actions as defined in steps. |
| Owner | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Owner | Vessel owner applies for a fishing license. | Manual | |
| 2 | KeFS Inspector | KeFS conducts vessel inspection for safety and gear compliance. | Manual | |
| 3 | Owner | Owner pays the license fee. | Manual | |
| 4 | KeFS | KeFS Director General approves and issues the license. | Manual | |

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
