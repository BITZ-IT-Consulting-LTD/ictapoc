# STANDARD BPM TEMPLATE – Kenya National Examinations Council

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya National Examinations Council
- **Process Name:** To develop and implement robust examination policies, procedures, and regulations; to effectively conduct national examinations across various educational levels; to register candidates efficiently for all KNEC examinations; to process and disseminate examination results accurately and in a timely manner; to award credible certificates and diplomas to successful candidates; to confirm the authenticity of credentials issued by the Council; to undertake research on educational assessment to inform best practices; to carry out the equation of foreign qualifications; and to advise the Government on matters pertaining to examinations and certification policies.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Kenya National Examinations Council (KNEC) is a statutory body mandated by Section 10 of the KNEC Act No. 29 of 2012. Its core responsibility is to set and maintain examination standards, and to develop and conduct public academic, technical, and other national examinations at basic and tertiary levels within Kenya. KNEC also awards certificates or diplomas to successful candidates, thereby playing a critical role in evaluating educational achievement and facilitating progression in education and employment.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant registers on KNEC QMIS portal."]
        S2["Applicant selects 'Lost Certificate' or 'Confirmat..."]
        S3["Applicant uploads ID, Police Abstract, and pays th..."]
        S5["Applicant collects the document from KNEC offices."]
    end
    subgraph KNEC [KNEC]
        S4["KNEC processes the request (retrieval from archive..."]
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
To develop and implement robust examination policies, procedures, and regulations; to effectively conduct national examinations across various educational levels; to register candidates efficiently for all KNEC examinations; to process and disseminate examination results accurately and in a timely manner; to award credible certificates and diplomas to successful candidates; to confirm the authenticity of credentials issued by the Council; to undertake research on educational assessment to inform best practices; to carry out the equation of foreign qualifications; and to advise the Government on matters pertaining to examinations and certification policies.

### Service Category
- G2C/G2B

### Process Objective
- To develop and implement robust examination policies, procedures, and regulations; to effectively conduct national examinations across various educational levels; to register candidates efficiently for all KNEC examinations; to process and disseminate examination results accurately and in a timely manner; to award credible certificates and diplomas to successful candidates; to confirm the authenticity of credentials issued by the Council; to undertake research on educational assessment to inform best practices; to carry out the equation of foreign qualifications; and to advise the Government on matters pertaining to examinations and certification policies.

### Scope
- **In Scope:** End-to-end processing within Kenya National Examinations Council.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Kenya National Examinations Council Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| KNEC | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant registers on KNEC QMIS portal. | Digital | |
| 2 | Applicant | Applicant selects 'Lost Certificate' or 'Confirmation' service. | Manual | |
| 3 | Applicant | Applicant uploads ID, Police Abstract, and pays the fee. | Manual | |
| 4 | KNEC | KNEC processes the request (retrieval from archives). | Manual | |
| 5 | Applicant | Applicant collects the document from KNEC offices. | Manual | |

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
