# SACCO Societies Regulatory Authority – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** SACCO Societies Regulatory Authority
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
    subgraph Sacco [Sacco]
        S1["Proposed Sacco applies for letter of intent."]
        S3["Sacco demonstrates minimum capital compliance."]
    end
    subgraph SASRA [SASRA]
        S2["SASRA conducts pre-licensing inspection of systems..."]
        S4["SASRA reviews policies and governance."]
        S5["SASRA issues the Deposit-Taking License."]
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
- **In Scope:** End-to-end processing within SACCO Societies Regulatory Authority.

### Triggers
- Submission of application/request by Sacco.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Sacco | Process Actor | Performs actions as defined in steps. |
| SASRA | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Sacco | Proposed Sacco applies for letter of intent. | Manual | |
| 2 | SASRA | SASRA conducts pre-licensing inspection of systems and premises. | Manual | |
| 3 | Sacco | Sacco demonstrates minimum capital compliance. | Manual | |
| 4 | SASRA | SASRA reviews policies and governance. | Manual | |
| 5 | SASRA | SASRA issues the Deposit-Taking License. | Manual | |

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
