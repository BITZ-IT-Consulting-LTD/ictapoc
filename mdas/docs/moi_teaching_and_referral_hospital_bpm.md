# STANDARD BPM TEMPLATE – Moi Teaching and Referral Hospital

## Cover Page
- **Ministry/Department/Agency (MDA):** Moi Teaching and Referral Hospital
- **Process Name:** Represents 'Health' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Health' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Patient [Patient]
        S1["Patient registers at the reception desk and pays r..."]
        S4["Patient pays for laboratory/pharmacy services."]
        S5["Patient collects medication or undergoes procedure..."]
    end
    subgraph Nurse [Nurse]
        S2["Nurse conducts triage (vitals check) and records h..."]
    end
    subgraph Doctor [Doctor]
        S3["Doctor consults and prescribes treatment or diagno..."]
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
Represents 'Health' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Service Category
- G2C (Government to Citizen)

### Process Objective
- Represents 'Health' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Scope
- **In Scope:** End-to-end processing within Moi Teaching and Referral Hospital.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Patient.

### End States
- **Successful:** Patient File / EMR Record, Diagnostic Lab Reports, Prescription / Medication, Discharge Summary
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Moi Teaching and Referral Hospital Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Nurse | Process Actor | Performs actions as defined in steps. |
| Patient | Process Actor | Performs actions as defined in steps. |
| Doctor | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Patient Personal/Bio-data, Insurance Card / NHIF Number, Medical History Records, Triage Vitals (BP, Temp, etc.)
- **Outputs:** Patient File / EMR Record, Diagnostic Lab Reports, Prescription / Medication, Discharge Summary

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Patient | Patient registers at the reception desk and pays registration fee. | Manual | |
| 2 | Nurse | Nurse conducts triage (vitals check) and records history. | Manual | |
| 3 | Doctor | Doctor consults and prescribes treatment or diagnostic tests. | Manual | |
| 4 | Patient | Patient pays for laboratory/pharmacy services. | Manual | |
| 5 | Patient | Patient collects medication or undergoes procedures. | Manual | |

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
