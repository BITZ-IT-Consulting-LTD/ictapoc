# Export Processing Zones Authority – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Export Processing Zones Authority
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
    subgraph Investor [Investor]
        S1["Investor submits a project proposal and applicatio..."]
        S4["Investor accepts offer and pays the annual license..."]
    end
    subgraph EPZA [EPZA]
        S2["EPZA appraises the project (investment capital, ex..."]
        S3["Upon approval, EPZA issues a Letter of Offer."]
        S5["EPZA issues the EPZ Enterprise License."]
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
- **In Scope:** End-to-end processing within Export Processing Zones Authority.

### Triggers
- Submission of application/request by Investor.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Investor | Process Actor | Performs actions as defined in steps. |
| EPZA | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Investor | Investor submits a project proposal and application form to EPZA. | Manual | |
| 2 | EPZA | EPZA appraises the project (investment capital, export market, employment creation). | Manual | |
| 3 | EPZA | Upon approval, EPZA issues a Letter of Offer. | Manual | |
| 4 | Investor | Investor accepts offer and pays the annual license fee. | Manual | |
| 5 | EPZA | EPZA issues the EPZ Enterprise License. | Manual | |

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
