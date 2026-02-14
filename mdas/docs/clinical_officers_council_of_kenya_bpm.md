# STANDARD BPM TEMPLATE – Clinical Officers Council of Kenya

## Cover Page
- **Ministry/Department/Agency (MDA):** Clinical Officers Council of Kenya
- **Process Name:** To advise the government on policy matters concerning clinical medicine practice; to prescribe the minimum educational entry requirements for individuals aspiring to be trained as clinical officers; to approve institutions for the training of clinical officers and establish, approve, and accredit clinical medicine programs and continuing professional education programs; to register and license clinical officers; to maintain a comprehensive register and records of all clinical officers registered by the Council; to publish the names of all registered clinical officers in the Kenya Gazette every calendar year; to promote the development and adoption of codes of practice; to regulate professional conduct and ensure the maintenance and improvement of the standards of practice of clinical medicine; to administer pre-internship/licensure examinations to ensure the competency of clinical officers; to collaborate with other medical professional associations, organizations, and relevant bodies; to assess the qualifications of clinical officers; and to consider and address any other matters related to clinical officers, including prescribing badges, insignia, or uniforms.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Clinical Officers Council of Kenya (COC) is a government agency established under the Clinical Officers (Training, Registration and Licensing) Act No. 20 of 2017. Its primary mandate is to regulate the training, registration, licensing, and practice of Clinical Officers in Kenya. The Council ensures high standards of education, professional competence, and ethical conduct in clinical medicine practice, thereby safeguarding public health and maintaining the integrity of the clinical officer profession in the country.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Professional [Professional]
        S1["Professional registers on the Board's Online Porta..."]
        S2["Applicant uploads academic certificates and profes..."]
        S4["Applicant pays the registration/annual retention f..."]
    end
    subgraph Board [Board]
        S3["Board Secretariat conducts verification and indexi..."]
        S5["Board gazettes the member and issues the Annual Pr..."]
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
To advise the government on policy matters concerning clinical medicine practice; to prescribe the minimum educational entry requirements for individuals aspiring to be trained as clinical officers; to approve institutions for the training of clinical officers and establish, approve, and accredit clinical medicine programs and continuing professional education programs; to register and license clinical officers; to maintain a comprehensive register and records of all clinical officers registered by the Council; to publish the names of all registered clinical officers in the Kenya Gazette every calendar year; to promote the development and adoption of codes of practice; to regulate professional conduct and ensure the maintenance and improvement of the standards of practice of clinical medicine; to administer pre-internship/licensure examinations to ensure the competency of clinical officers; to collaborate with other medical professional associations, organizations, and relevant bodies; to assess the qualifications of clinical officers; and to consider and address any other matters related to clinical officers, including prescribing badges, insignia, or uniforms.

### Service Category
- G2C/G2B

### Process Objective
- To advise the government on policy matters concerning clinical medicine practice; to prescribe the minimum educational entry requirements for individuals aspiring to be trained as clinical officers; to approve institutions for the training of clinical officers and establish, approve, and accredit clinical medicine programs and continuing professional education programs; to register and license clinical officers; to maintain a comprehensive register and records of all clinical officers registered by the Council; to publish the names of all registered clinical officers in the Kenya Gazette every calendar year; to promote the development and adoption of codes of practice; to regulate professional conduct and ensure the maintenance and improvement of the standards of practice of clinical medicine; to administer pre-internship/licensure examinations to ensure the competency of clinical officers; to collaborate with other medical professional associations, organizations, and relevant bodies; to assess the qualifications of clinical officers; and to consider and address any other matters related to clinical officers, including prescribing badges, insignia, or uniforms.

### Scope
- **In Scope:** End-to-end processing within Clinical Officers Council of Kenya.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Professional.

### End States
- **Successful:** Patient File / EMR Record, Diagnostic Lab Reports, Prescription / Medication, Discharge Summary
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Clinical Officers Council of Kenya Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Professional | Process Actor | Performs actions as defined in steps. |
| Board | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Patient Personal/Bio-data, Insurance Card / NHIF Number, Medical History Records, Triage Vitals (BP, Temp, etc.)
- **Outputs:** Patient File / EMR Record, Diagnostic Lab Reports, Prescription / Medication, Discharge Summary

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Professional | Professional registers on the Board's Online Portal. | Digital | |
| 2 | Professional | Applicant uploads academic certificates and professional testimonials. | Manual | |
| 3 | Board | Board Secretariat conducts verification and indexing. | Manual | |
| 4 | Professional | Applicant pays the registration/annual retention fee. | Manual | |
| 5 | Board | Board gazettes the member and issues the Annual Practicing Certificate. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Loss of physical patient files.
- Long patient wait times at triage and pharmacy.
- Lack of interoperability between departments (Lab, Pharmacy, Billing).
- Revenue leakage in cash collections.

### Opportunities
- Comprehensive Electronic Medical Records (EMR).
- Telemedicine for remote consultations.
- AI-assisted diagnostics and radiology.
- Automated inventory management for pharmacy.

---

## KPIs
| KPI | Baseline | Target |
|---|---|---|
| Turnaround Time | 30 Days | 5 Days |
| CSAT | 50% | 90% |
