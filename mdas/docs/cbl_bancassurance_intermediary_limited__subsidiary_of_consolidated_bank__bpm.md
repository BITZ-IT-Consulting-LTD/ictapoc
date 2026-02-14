# STANDARD BPM TEMPLATE – CBL Bancassurance Intermediary Limited( subsidiary of consolidated Bank)

## Cover Page
- **Ministry/Department/Agency (MDA):** CBL Bancassurance Intermediary Limited( subsidiary of consolidated Bank)
- **Process Name:** To formulate and execute the overall strategy for the bank's bancassurance offerings across various insurance products, customer propositions, and distribution channels; to drive growth in business volumes with the goal of making bancassurance a significant contributor to the Consolidated Bank's profitability; to effectively manage bancassurance income and achieve profit and loss targets; to negotiate pricing structures for bancassurance products and services, and serve as a key interface with insurance partners and industry associations; to review bancassurance strategy and performance, providing leadership, and spearheading the implementation of quality operational standards, risk management frameworks, and compliance protocols; to offer professional insurance advisory services to individual, SME, and corporate bank customers; to facilitate access to a comprehensive range of insurance policies, including motor, non-motor, marine, agriculture, medical, life, and pensions; and to provide efficient claims services, risk management solutions, and insurance premium financing.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
CBL Bancassurance Intermediary Limited, a subsidiary of Consolidated Bank of Kenya, operates within the Kenyan financial landscape. Its primary mandate is to distribute a wide array of insurance products through the bank's extensive channels, acting as a crucial intermediary between insurance companies (underwriters) and the bank's diverse clientele. The company aims to provide convenient and accessible insurance services, drive significant business growth and profitability for the Consolidated Bank Group, and offer professional insurance advisory services across various categories, thereby enhancing customer value and financial inclusion.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant submits loan/grant application form with..."]
    end
    subgraph Agency [Agency]
        S2["Agency conducts desk appraisal and credit scoring."]
        S5["Funds are disbursed to the applicant's account."]
    end
    subgraph FieldOfficer [Field Officer]
        S3["Field officer visits for due diligence (if applica..."]
    end
    subgraph Committee [Committee]
        S4["Committee approves the facility/grant."]
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
To formulate and execute the overall strategy for the bank's bancassurance offerings across various insurance products, customer propositions, and distribution channels; to drive growth in business volumes with the goal of making bancassurance a significant contributor to the Consolidated Bank's profitability; to effectively manage bancassurance income and achieve profit and loss targets; to negotiate pricing structures for bancassurance products and services, and serve as a key interface with insurance partners and industry associations; to review bancassurance strategy and performance, providing leadership, and spearheading the implementation of quality operational standards, risk management frameworks, and compliance protocols; to offer professional insurance advisory services to individual, SME, and corporate bank customers; to facilitate access to a comprehensive range of insurance policies, including motor, non-motor, marine, agriculture, medical, life, and pensions; and to provide efficient claims services, risk management solutions, and insurance premium financing.

### Service Category
- G2C/G2B

### Process Objective
- To formulate and execute the overall strategy for the bank's bancassurance offerings across various insurance products, customer propositions, and distribution channels; to drive growth in business volumes with the goal of making bancassurance a significant contributor to the Consolidated Bank's profitability; to effectively manage bancassurance income and achieve profit and loss targets; to negotiate pricing structures for bancassurance products and services, and serve as a key interface with insurance partners and industry associations; to review bancassurance strategy and performance, providing leadership, and spearheading the implementation of quality operational standards, risk management frameworks, and compliance protocols; to offer professional insurance advisory services to individual, SME, and corporate bank customers; to facilitate access to a comprehensive range of insurance policies, including motor, non-motor, marine, agriculture, medical, life, and pensions; and to provide efficient claims services, risk management solutions, and insurance premium financing.

### Scope
- **In Scope:** End-to-end processing within CBL Bancassurance Intermediary Limited( subsidiary of consolidated Bank).
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The CBL Bancassurance Intermediary Limited( subsidiary of consolidated Bank) Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| Field Officer | Process Actor | Performs actions as defined in steps. |
| Committee | Process Actor | Performs actions as defined in steps. |
| Agency | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Loan/Service Application Form, Business Proposal / Plan, Financial Statements / Bank Records, Collateral / Security Documents
- **Outputs:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant submits loan/grant application form with business proposal. | Manual | |
| 2 | Agency | Agency conducts desk appraisal and credit scoring. | Manual | |
| 3 | Field Officer | Field officer visits for due diligence (if applicable). | Manual | |
| 4 | Committee | Committee approves the facility/grant. | Manual | |
| 5 | Agency | Funds are disbursed to the applicant's account. | Manual | |

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
