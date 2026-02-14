# STANDARD BPM TEMPLATE – ENERGY AND PETROLEUM AUTHORITY

## Cover Page
- **Ministry/Department/Agency (MDA):** ENERGY AND PETROLEUM AUTHORITY
- **Process Name:** To establish and enforce regulations for the electricity, petroleum, and renewable energy sectors; issue licenses to operators; set tariffs; safeguard consumer rights; monitor compliance with energy laws and standards; promote renewable energy development and utilization; and advance energy efficiency initiatives across Kenya for a secure, sustainable, and affordable energy supply.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Energy and Petroleum Regulatory Authority (EPRA) is a statutory body in Kenya, established under the Energy Act of 2019. It is responsible for the economic and technical regulation of Kenya's electricity, renewable energy, petroleum, and coal subsectors, ensuring sustainable energy supply, fair pricing, and consumer protection.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant submits application for license, permit,..."]
        S4["Applicant pays the prescribed fees."]
    end
    subgraph Authority [Authority]
        S2["Authority verifies documents and compliance with r..."]
        S5["Authority approves and issues the License/Permit/C..."]
    end
    subgraph TechnicalOfficer [Technical Officer]
        S3["Technical officers conduct assessment or inspectio..."]
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
To establish and enforce regulations for the electricity, petroleum, and renewable energy sectors; issue licenses to operators; set tariffs; safeguard consumer rights; monitor compliance with energy laws and standards; promote renewable energy development and utilization; and advance energy efficiency initiatives across Kenya for a secure, sustainable, and affordable energy supply.

### Service Category
- G2B (Government to Business)

### Process Objective
- To establish and enforce regulations for the electricity, petroleum, and renewable energy sectors; issue licenses to operators; set tariffs; safeguard consumer rights; monitor compliance with energy laws and standards; promote renewable energy development and utilization; and advance energy efficiency initiatives across Kenya for a secure, sustainable, and affordable energy supply.

### Scope
- **In Scope:** End-to-end processing within ENERGY AND PETROLEUM AUTHORITY.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The ENERGY AND PETROLEUM AUTHORITY Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| Authority | Process Actor | Performs actions as defined in steps. |
| Technical Officer | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant submits application for license, permit, or service. | Manual | |
| 2 | Authority | Authority verifies documents and compliance with regulations. | Manual | |
| 3 | Technical Officer | Technical officers conduct assessment or inspection. | Manual | |
| 4 | Applicant | Applicant pays the prescribed fees. | Manual | |
| 5 | Authority | Authority approves and issues the License/Permit/Certificate. | Manual | |

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
