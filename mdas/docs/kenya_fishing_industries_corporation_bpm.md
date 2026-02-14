# STANDARD BPM TEMPLATE – Kenya Fishing Industries Corporation

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Fishing Industries Corporation
- **Process Name:** To ensure the sustainable management of fish resources within Kenya's waters and high seas; to engage in fish processing, value addition, and marketing of fish products; to develop and maintain essential fishing infrastructure; to provide training and capacity building programs for fishermen and stakeholders; to support government policies aimed at improving the fishing sector and food security; and to promote the establishment of efficient businesses in fishing and related activities.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya Fishing Industries Corporation (KFIC) is a state-owned enterprise established in 1979, primarily focused on promoting and developing Kenya's fishing industry. Its core mandate includes ensuring the sustainable management of fish resources, enhancing food security, and contributing to economic growth through fish processing, value addition, infrastructure development, and capacity building within the sector.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Customer [Customer]
        S1["Customer submits an order or request for goods/ser..."]
        S3["Customer makes payment via Bank or M-Pesa."]
        S5["Customer signs Delivery Note or Service Acceptance..."]
    end
    subgraph SalesDepartment [Sales Department]
        S2["Corporation processes the request and issues a quo..."]
    end
    subgraph StoresOperations [Stores/Operations]
        S4["Corporation releases the goods or delivers the ser..."]
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
To ensure the sustainable management of fish resources within Kenya's waters and high seas; to engage in fish processing, value addition, and marketing of fish products; to develop and maintain essential fishing infrastructure; to provide training and capacity building programs for fishermen and stakeholders; to support government policies aimed at improving the fishing sector and food security; and to promote the establishment of efficient businesses in fishing and related activities.

### Service Category
- G2B (Government to Business)

### Process Objective
- To ensure the sustainable management of fish resources within Kenya's waters and high seas; to engage in fish processing, value addition, and marketing of fish products; to develop and maintain essential fishing infrastructure; to provide training and capacity building programs for fishermen and stakeholders; to support government policies aimed at improving the fishing sector and food security; and to promote the establishment of efficient businesses in fishing and related activities.

### Scope
- **In Scope:** End-to-end processing within Kenya Fishing Industries Corporation.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Customer.

### End States
- **Successful:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Kenya Fishing Industries Corporation Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Customer | Process Actor | Performs actions as defined in steps. |
| Sales Department | Process Actor | Performs actions as defined in steps. |
| Stores/Operations | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Loan/Service Application Form, Business Proposal / Plan, Financial Statements / Bank Records, Collateral / Security Documents
- **Outputs:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Customer | Customer submits an order or request for goods/services. | Manual | |
| 2 | Sales Department | Corporation processes the request and issues a quotation/proforma invoice. | Manual | |
| 3 | Customer | Customer makes payment via Bank or M-Pesa. | Manual | |
| 4 | Stores/Operations | Corporation releases the goods or delivers the service. | Manual | |
| 5 | Customer | Customer signs Delivery Note or Service Acceptance Form. | Manual | |

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
