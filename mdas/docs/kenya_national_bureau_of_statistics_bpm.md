# STANDARD BPM TEMPLATE – Kenya National Bureau of Statistics

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya National Bureau of Statistics
- **Process Name:** To collect, compile, analyze, publish, and disseminate integrated, reliable, and timely statistical information on various socio-economic sectors (e.g., health, economy, poverty, foreign investment); to coordinate, monitor, and supervise the National Statistical System (NSS) to ensure coherence and quality; to establish standards and promote best practices in statistical production and dissemination; to conduct national censuses and surveys, including the Population and Housing Census; to maintain a comprehensive national socio-economic database; and to collaborate with county governments and other institutions in the production of official statistics.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya National Bureau of Statistics (KNBS) is Kenya's principal agency for the collection, compilation, analysis, publication, and dissemination of official statistical data. Established by the Statistics Act of 2006, it plays a critical role in coordinating the National Statistical System (NSS) and ensuring adherence to statistical standards, thereby providing reliable data for evidence-based policy formulation, planning, and decision-making for national development.

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
To collect, compile, analyze, publish, and disseminate integrated, reliable, and timely statistical information on various socio-economic sectors (e.g., health, economy, poverty, foreign investment); to coordinate, monitor, and supervise the National Statistical System (NSS) to ensure coherence and quality; to establish standards and promote best practices in statistical production and dissemination; to conduct national censuses and surveys, including the Population and Housing Census; to maintain a comprehensive national socio-economic database; and to collaborate with county governments and other institutions in the production of official statistics.

### Service Category
- G2C/G2B

### Process Objective
- To collect, compile, analyze, publish, and disseminate integrated, reliable, and timely statistical information on various socio-economic sectors (e.g., health, economy, poverty, foreign investment); to coordinate, monitor, and supervise the National Statistical System (NSS) to ensure coherence and quality; to establish standards and promote best practices in statistical production and dissemination; to conduct national censuses and surveys, including the Population and Housing Census; to maintain a comprehensive national socio-economic database; and to collaborate with county governments and other institutions in the production of official statistics.

### Scope
- **In Scope:** End-to-end processing within Kenya National Bureau of Statistics.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Kenya National Bureau of Statistics Act; The Constitution of Kenya 2010; Data Protection Act 2019.

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
