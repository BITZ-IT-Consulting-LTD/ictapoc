# STANDARD BPM TEMPLATE – Kenya Medical Supplies Authority

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Medical Supplies Authority
- **Process Name:** To ensure the availability, accessibility, and affordability of quality Health Products and Technologies (HPTs) for all Kenyans; to procure medical supplies for prescribed public health programs, national strategic stock reserves, and national referral hospitals; to provide efficient and secure warehousing and distribution services for medical commodities; to enforce stringent quality assurance measures for all procured supplies; to offer technical guidance to health management boards and county governments on cost-effective procurement and rational use of medicines; and to support various national health programs (e.g., TB, HIV/AIDS, Malaria Control).
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya Medical Supplies Authority (KEMSA) is a state corporation under the Ministry of Health, established by the KEMSA Act 2013. Its primary mandate is to procure, warehouse, and distribute Health Products and Technologies (HPTs), including drugs, vaccines, and medical equipment, to public health facilities across Kenya. KEMSA plays a crucial role in supporting the implementation of Universal Health Coverage (UHC) by ensuring the availability, accessibility, and affordability of quality medical supplies nationwide.

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
To ensure the availability, accessibility, and affordability of quality Health Products and Technologies (HPTs) for all Kenyans; to procure medical supplies for prescribed public health programs, national strategic stock reserves, and national referral hospitals; to provide efficient and secure warehousing and distribution services for medical commodities; to enforce stringent quality assurance measures for all procured supplies; to offer technical guidance to health management boards and county governments on cost-effective procurement and rational use of medicines; and to support various national health programs (e.g., TB, HIV/AIDS, Malaria Control).

### Service Category
- G2B (Government to Business)

### Process Objective
- To ensure the availability, accessibility, and affordability of quality Health Products and Technologies (HPTs) for all Kenyans; to procure medical supplies for prescribed public health programs, national strategic stock reserves, and national referral hospitals; to provide efficient and secure warehousing and distribution services for medical commodities; to enforce stringent quality assurance measures for all procured supplies; to offer technical guidance to health management boards and county governments on cost-effective procurement and rational use of medicines; and to support various national health programs (e.g., TB, HIV/AIDS, Malaria Control).

### Scope
- **In Scope:** End-to-end processing within Kenya Medical Supplies Authority.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Kenya Medical Supplies Authority Act; The Constitution of Kenya 2010; Data Protection Act 2019.

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
