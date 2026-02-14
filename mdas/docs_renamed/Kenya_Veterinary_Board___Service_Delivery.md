# Kenya Veterinary Board – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Veterinary Board
- **Process Name:** Service Delivery
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
    subgraph VetSurgeon [Vet Surgeon]
        S1["Vet Surgeon logs into the KVB Portal."]
        S2["Applicant uploads proof of CPD points and Good Sta..."]
        S3["Applicant applies for Annual Retention."]
        S4["Applicant pays the retention fee."]
    end
    subgraph KVB [KVB]
        S5["KVB issues the Annual Retention Certificate."]
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
- **In Scope:** End-to-end processing within Kenya Veterinary Board.

### Triggers
- Submission of application/request by Vet Surgeon.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Vet Surgeon | Process Actor | Performs actions as defined in steps. |
| KVB | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Vet Surgeon | Vet Surgeon logs into the KVB Portal. | Digital | |
| 2 | Vet Surgeon | Applicant uploads proof of CPD points and Good Standing. | Manual | |
| 3 | Vet Surgeon | Applicant applies for Annual Retention. | Manual | |
| 4 | Vet Surgeon | Applicant pays the retention fee. | Manual | |
| 5 | KVB | KVB issues the Annual Retention Certificate. | Manual | |

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
