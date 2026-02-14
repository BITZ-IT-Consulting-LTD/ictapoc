# STANDARD BPM TEMPLATE – Coast Water Works Development Agency

## Cover Page
- **Ministry/Department/Agency (MDA):** Coast Water Works Development Agency
- **Process Name:** To undertake the development, maintenance, and management of water works in the Coast Region; to operate water works and provide water services until such a time these responsibilities are handed over to respective counties or water service providers; to provide technical services and capacity building to County Governments; to offer reserve capacity for water services when the Water Services Regulatory Board (WASREB) orders the transfer of functions from a defaulting water services provider to another licensee; to provide technical support to the Cabinet Secretary in fulfilling their duties under the Constitution and the Water Act 2016; to own and hold water and sewerage assets and infrastructure on behalf of the National Government; to plan, develop, and expand water and sewerage infrastructure for the National Government; to assist County Governments within its jurisdiction during the transition period in contracting out water and sewerage services provision to Water Services Providers (WSPs) and monitoring these services; to ensure compliance with licensing requirements by WSPs; to assume responsibility as a Water Service Provider as a last resort; and to manage bulk water supply from various sources, including Mzima Springs, Baricho well fields, Marere Springs, Tiwi boreholes, the Hola Water supply project, and Shella wells.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Coast Water Works Development Agency (CWWDA) is a state corporation in Kenya, established under the Water Act of 2016 and transitioning from the Coast Water Services Board (CWSB) in May 2019. Its primary mandate is to develop and maintain sustainable water and sanitation infrastructure within the Coast region of Kenya. This includes undertaking the development, maintenance, and management of national public water works, with the aim of delivering efficient and reliable water and sanitation services to the residents of Mombasa, Kilifi, Kwale, Tana River, Lamu, and Taita Taveta counties.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Agency [Agency]
        S1["Agency advertises tender on Public Procurement Inf..."]
    end
    subgraph Bidder [Bidder]
        S2["Bidder downloads tender documents and prepares bid..."]
        S3["Bidder submits bid via e-Procurement portal or ten..."]
    end
    subgraph EvaluationCommittee [Evaluation Committee]
        S4["Evaluation Committee conducts opening, technical, ..."]
    end
    subgraph AccountingOfficer [Accounting Officer]
        S5["Accounting Officer awards the tender to the lowest..."]
    end
    subgraph AgencyBidder [Agency/Bidder]
        S6["Contract is signed after the 14-day standstill per..."]
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
To undertake the development, maintenance, and management of water works in the Coast Region; to operate water works and provide water services until such a time these responsibilities are handed over to respective counties or water service providers; to provide technical services and capacity building to County Governments; to offer reserve capacity for water services when the Water Services Regulatory Board (WASREB) orders the transfer of functions from a defaulting water services provider to another licensee; to provide technical support to the Cabinet Secretary in fulfilling their duties under the Constitution and the Water Act 2016; to own and hold water and sewerage assets and infrastructure on behalf of the National Government; to plan, develop, and expand water and sewerage infrastructure for the National Government; to assist County Governments within its jurisdiction during the transition period in contracting out water and sewerage services provision to Water Services Providers (WSPs) and monitoring these services; to ensure compliance with licensing requirements by WSPs; to assume responsibility as a Water Service Provider as a last resort; and to manage bulk water supply from various sources, including Mzima Springs, Baricho well fields, Marere Springs, Tiwi boreholes, the Hola Water supply project, and Shella wells.

### Service Category
- G2C/G2B

### Process Objective
- To undertake the development, maintenance, and management of water works in the Coast Region; to operate water works and provide water services until such a time these responsibilities are handed over to respective counties or water service providers; to provide technical services and capacity building to County Governments; to offer reserve capacity for water services when the Water Services Regulatory Board (WASREB) orders the transfer of functions from a defaulting water services provider to another licensee; to provide technical support to the Cabinet Secretary in fulfilling their duties under the Constitution and the Water Act 2016; to own and hold water and sewerage assets and infrastructure on behalf of the National Government; to plan, develop, and expand water and sewerage infrastructure for the National Government; to assist County Governments within its jurisdiction during the transition period in contracting out water and sewerage services provision to Water Services Providers (WSPs) and monitoring these services; to ensure compliance with licensing requirements by WSPs; to assume responsibility as a Water Service Provider as a last resort; and to manage bulk water supply from various sources, including Mzima Springs, Baricho well fields, Marere Springs, Tiwi boreholes, the Hola Water supply project, and Shella wells.

### Scope
- **In Scope:** End-to-end processing within Coast Water Works Development Agency.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Agency.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Coast Water Works Development Agency Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Evaluation Committee | Process Actor | Performs actions as defined in steps. |
| Accounting Officer | Process Actor | Performs actions as defined in steps. |
| Bidder | Process Actor | Performs actions as defined in steps. |
| Agency/Bidder | Process Actor | Performs actions as defined in steps. |
| Agency | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Agency | Agency advertises tender on Public Procurement Information Portal (PPIP) and website. | Digital | |
| 2 | Bidder | Bidder downloads tender documents and prepares bid (Technical & Financial). | Manual | |
| 3 | Bidder | Bidder submits bid via e-Procurement portal or tender box. | Digital | |
| 4 | Evaluation Committee | Evaluation Committee conducts opening, technical, and financial evaluation. | Manual | |
| 5 | Accounting Officer | Accounting Officer awards the tender to the lowest responsive bidder. | Manual | |
| 6 | Agency/Bidder | Contract is signed after the 14-day standstill period. | Manual | |

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
