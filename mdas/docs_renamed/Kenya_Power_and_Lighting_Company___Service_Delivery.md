# Kenya Power and Lighting Company – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Power and Lighting Company
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Energy Infrastructure and ICT' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant applies for new supply via eCitizen, KPL..."]
        S2["Applicant submits ID, PIN, and Wiring Certificates..."]
        S5["Applicant pays the quotation amount."]
    end
    subgraph KPLCStaff [KPLC Staff]
        S3["KPLC staff visits the site for survey and estimati..."]
        S6["KPLC installs the meter and connects power."]
    end
    subgraph KPLC [KPLC]
        S4["KPLC issues a Quotation for the connection costs."]
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
Service Delivery

### Service Category
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within Kenya Power and Lighting Company.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| KPLC | Process Actor | Performs actions as defined in steps. |
| KPLC Staff | Process Actor | Performs actions as defined in steps. |
| Applicant | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Loan/Service Application Form, Business Proposal / Plan, Financial Statements / Bank Records, Collateral / Security Documents
- **Outputs:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant applies for new supply via eCitizen, KPLC Self Service Portal, or physically. | Digital | |
| 2 | Applicant | Applicant submits ID, PIN, and Wiring Certificates. | Manual | |
| 3 | KPLC Staff | KPLC staff visits the site for survey and estimation. | Manual | |
| 4 | KPLC | KPLC issues a Quotation for the connection costs. | Manual | |
| 5 | Applicant | Applicant pays the quotation amount. | Manual | |
| 6 | KPLC Staff | KPLC installs the meter and connects power. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Lengthy credit appraisal processes.
- Manual debt collection and reconciliation.
- High paperwork for loan processing.
- Lack of 360-degree customer view.

### Opportunities
- Automated Credit Scoring and Appraisal.
- Mobile-based loan application and repayment.
- Customer Relationship Management (CRM) systems.
- Data analytics for risk management.

---

## KPIs
| KPI | Baseline | Target |
|---|---|---|
| Turnaround Time | 30 Days | 5 Days |
| CSAT | 50% | 90% |
