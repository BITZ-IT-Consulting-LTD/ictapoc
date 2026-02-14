# Kenya Medical Practitioners and Dentists Council – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Medical Practitioners and Dentists Council
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Health' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Practitioner [Practitioner]
        S1["Practitioner logs into the KMPDC Portal (osp.kmpdc..."]
        S2["Practitioner updates CPD (Continuous Professional ..."]
        S3["Practitioner applies for Annual Retention/Practice..."]
        S4["Practitioner pays the annual retention fee via M-P..."]
    end
    subgraph System [System]
        S5["System generates and emails the Annual Practice Li..."]
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
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within Kenya Medical Practitioners and Dentists Council.

### Triggers
- Submission of application/request by Practitioner.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| System | Process Actor | Performs actions as defined in steps. |
| Practitioner | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Practitioner | Practitioner logs into the KMPDC Portal (osp.kmpdc.go.ke). | Digital | |
| 2 | Practitioner | Practitioner updates CPD (Continuous Professional Development) points. | Manual | |
| 3 | Practitioner | Practitioner applies for Annual Retention/Practice License. | Manual | |
| 4 | Practitioner | Practitioner pays the annual retention fee via M-Pesa. | Manual | |
| 5 | System | System generates and emails the Annual Practice License. | Manual | |

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
