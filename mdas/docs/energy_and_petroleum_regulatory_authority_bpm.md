# STANDARD BPM TEMPLATE – Energy and Petroleum Regulatory Authority

## Cover Page
- **Ministry/Department/Agency (MDA):** Energy and Petroleum Regulatory Authority
- **Process Name:** To regulate the generation, importation, exportation, transmission, distribution, supply, and use of electrical energy and petroleum products; issue licenses to operators; manage tariffs for electricity and petroleum; protect consumer rights; promote the development and use of renewable energy sources; ensure compliance with energy laws, regulations, and standards; and advise the government on energy sector matters for sustainable development.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Energy and Petroleum Regulatory Authority (EPRA) is a statutory body in Kenya, established under the Energy Act of 2019. It is mandated to regulate the energy and petroleum sectors, encompassing electricity, renewable energy, petroleum (upstream, midstream, and downstream), and coal, with the objective of ensuring fair pricing, efficiency, quality, and sustainability within these vital sectors.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant logs into EPRA License Management System..."]
        S2["Applicant selects license type (e.g., Solar PV T1/..."]
        S3["Applicant pays the application fee."]
        S5["Upon passing, applicant pays grant fee."]
    end
    subgraph EPRA [EPRA]
        S4["EPRA reviews application and invites applicant for..."]
        S6["EPRA issues the License."]
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
To regulate the generation, importation, exportation, transmission, distribution, supply, and use of electrical energy and petroleum products; issue licenses to operators; manage tariffs for electricity and petroleum; protect consumer rights; promote the development and use of renewable energy sources; ensure compliance with energy laws, regulations, and standards; and advise the government on energy sector matters for sustainable development.

### Service Category
- G2B (Government to Business)

### Process Objective
- To regulate the generation, importation, exportation, transmission, distribution, supply, and use of electrical energy and petroleum products; issue licenses to operators; manage tariffs for electricity and petroleum; protect consumer rights; promote the development and use of renewable energy sources; ensure compliance with energy laws, regulations, and standards; and advise the government on energy sector matters for sustainable development.

### Scope
- **In Scope:** End-to-end processing within Energy and Petroleum Regulatory Authority.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Energy and Petroleum Regulatory Authority Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| EPRA | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant logs into EPRA License Management System. | Manual | |
| 2 | Applicant | Applicant selects license type (e.g., Solar PV T1/T2) and uploads academic certs. | Manual | |
| 3 | Applicant | Applicant pays the application fee. | Manual | |
| 4 | EPRA | EPRA reviews application and invites applicant for interview/exam. | Manual | |
| 5 | Applicant | Upon passing, applicant pays grant fee. | Manual | |
| 6 | EPRA | EPRA issues the License. | Manual | |

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
