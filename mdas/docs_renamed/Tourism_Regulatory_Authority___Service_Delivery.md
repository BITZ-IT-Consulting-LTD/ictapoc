# Tourism Regulatory Authority – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Tourism Regulatory Authority
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'General Economic and Commercial Affairs' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Operator [Operator]
        S1["Operator applies for license via TRA Portal."]
        S2["Operator pays the application fee."]
        S4["Upon compliance, operator pays the license fee."]
    end
    subgraph TRAInspector [TRA Inspector]
        S3["TRA conducts physical inspection of the facility/v..."]
    end
    subgraph TRA [TRA]
        S5["TRA issues the Tourism License."]
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
- **In Scope:** End-to-end processing within Tourism Regulatory Authority.

### Triggers
- Submission of application/request by Operator.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| TRA | Process Actor | Performs actions as defined in steps. |
| TRA Inspector | Process Actor | Performs actions as defined in steps. |
| Operator | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Operator | Operator applies for license via TRA Portal. | Digital | |
| 2 | Operator | Operator pays the application fee. | Manual | |
| 3 | TRA Inspector | TRA conducts physical inspection of the facility/vehicle. | Manual | |
| 4 | Operator | Upon compliance, operator pays the license fee. | Manual | |
| 5 | TRA | TRA issues the Tourism License. | Manual | |

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
