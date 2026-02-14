# Kenya Film Classification Board – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Film Classification Board
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
    subgraph Filmmaker [Filmmaker]
        S1["Filmmaker applies for filming license via KFCB por..."]
        S2["Filmmaker submits script/synopsis for examination."]
        S4["Filmmaker pays the classification and licensing fe..."]
    end
    subgraph KFCB [KFCB]
        S3["KFCB reviews content and assigns age rating/classi..."]
        S5["KFCB issues the Filming License and Classification..."]
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
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within Kenya Film Classification Board.

### Triggers
- Submission of application/request by Filmmaker.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Filmmaker | Process Actor | Performs actions as defined in steps. |
| KFCB | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Filmmaker | Filmmaker applies for filming license via KFCB portal. | Digital | |
| 2 | Filmmaker | Filmmaker submits script/synopsis for examination. | Manual | |
| 3 | KFCB | KFCB reviews content and assigns age rating/classification. | Manual | |
| 4 | Filmmaker | Filmmaker pays the classification and licensing fees. | Manual | |
| 5 | KFCB | KFCB issues the Filming License and Classification Certificate. | Manual | |

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
