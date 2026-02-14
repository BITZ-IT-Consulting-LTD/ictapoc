# STANDARD BPM TEMPLATE – National Social Security Fund

## Cover Page
- **Ministry/Department/Agency (MDA):** National Social Security Fund
- **Process Name:** To register eligible individuals for social security across all sectors; to efficiently receive and manage contributions from its members and their employers; to oversee the funds of the scheme to ensure their sustainability, growth, and proper investment; to process and disburse various benefits, including retirement, survivor, and invalidity benefits, to eligible members or their dependents in a timely manner; to guarantee basic compensation in cases of permanent disability; to provide assistance to needy dependents in the event of a member's death; to offer a monthly life pension upon retirement to ensure income security; to mobilize domestic savings for national development; to aid in poverty reduction by providing a social safety net; to foster financial inclusion by reaching out to the informal sector; and to decrease the dependency ratio by encouraging self-reliance in old age.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The National Social Security Fund (NSSF) is a statutory public institution in Kenya mandated to provide social security protection to all workers, encompassing both the formal and informal sectors. Established initially as a Provident Fund in 1965, NSSF transitioned into a Pension Scheme in 2014 following the enactment of the NSSF Act, No. 45 of 2013. Its core purpose is to guarantee basic compensation in cases of permanent disability, provide assistance to needy dependents in the event of death, and offer a monthly life pension upon retirement. Beyond these direct benefits, NSSF also mobilizes domestic savings, aids in poverty reduction, fosters financial inclusion, and helps decrease the national dependency ratio.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant accesses NSSF Self Service Portal or USS..."]
        S2["Applicant enters National ID/Alien ID number and d..."]
        S5["Applicant prints the NSSF card/membership details."]
    end
    subgraph System [System]
        S3["System validates details from IPRS."]
        S4["System generates NSSF Number immediately."]
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
To register eligible individuals for social security across all sectors; to efficiently receive and manage contributions from its members and their employers; to oversee the funds of the scheme to ensure their sustainability, growth, and proper investment; to process and disburse various benefits, including retirement, survivor, and invalidity benefits, to eligible members or their dependents in a timely manner; to guarantee basic compensation in cases of permanent disability; to provide assistance to needy dependents in the event of a member's death; to offer a monthly life pension upon retirement to ensure income security; to mobilize domestic savings for national development; to aid in poverty reduction by providing a social safety net; to foster financial inclusion by reaching out to the informal sector; and to decrease the dependency ratio by encouraging self-reliance in old age.

### Service Category
- G2C/G2B

### Process Objective
- To register eligible individuals for social security across all sectors; to efficiently receive and manage contributions from its members and their employers; to oversee the funds of the scheme to ensure their sustainability, growth, and proper investment; to process and disburse various benefits, including retirement, survivor, and invalidity benefits, to eligible members or their dependents in a timely manner; to guarantee basic compensation in cases of permanent disability; to provide assistance to needy dependents in the event of a member's death; to offer a monthly life pension upon retirement to ensure income security; to mobilize domestic savings for national development; to aid in poverty reduction by providing a social safety net; to foster financial inclusion by reaching out to the informal sector; and to decrease the dependency ratio by encouraging self-reliance in old age.

### Scope
- **In Scope:** End-to-end processing within National Social Security Fund.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The National Social Security Fund Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| System | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Loan/Service Application Form, Business Proposal / Plan, Financial Statements / Bank Records, Collateral / Security Documents
- **Outputs:** Loan Disbursement / Service Delivery, Statement of Account, Contract / Agreement, Receipt / Invoice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant accesses NSSF Self Service Portal or USSD. | Digital | |
| 2 | Applicant | Applicant enters National ID/Alien ID number and details. | Manual | |
| 3 | System | System validates details from IPRS. | Manual | |
| 4 | System | System generates NSSF Number immediately. | Manual | |
| 5 | Applicant | Applicant prints the NSSF card/membership details. | Manual | |

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
