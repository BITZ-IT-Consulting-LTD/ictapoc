# STANDARD BPM TEMPLATE – Kenya Plant Health Inspectorate Services

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Plant Health Inspectorate Services
- **Process Name:** Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Exporter [Exporter]
        S1["Exporter registers as a client on the KEPHIS ECS p..."]
        S2["Exporter applies for Phytosanitary Certificate for..."]
        S5["Upon compliance, Exporter pays inspection fees."]
    end
    subgraph KEPHISInspector [KEPHIS Inspector]
        S3["KEPHIS inspector inspects the consignment at the p..."]
    end
    subgraph KEPHISLab [KEPHIS Lab]
        S4["Samples may be taken for laboratory analysis."]
    end
    subgraph KEPHIS [KEPHIS]
        S6["KEPHIS issues the Phytosanitary Certificate."]
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
Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Service Category
- G2C/G2B

### Process Objective
- Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Scope
- **In Scope:** End-to-end processing within Kenya Plant Health Inspectorate Services.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Exporter.

### End States
- **Successful:** Patient File / EMR Record, Diagnostic Lab Reports, Prescription / Medication, Discharge Summary
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The Kenya Plant Health Inspectorate Services Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| KEPHIS | Process Actor | Performs actions as defined in steps. |
| KEPHIS Inspector | Process Actor | Performs actions as defined in steps. |
| Exporter | Process Actor | Performs actions as defined in steps. |
| KEPHIS Lab | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Patient Personal/Bio-data, Insurance Card / NHIF Number, Medical History Records, Triage Vitals (BP, Temp, etc.)
- **Outputs:** Patient File / EMR Record, Diagnostic Lab Reports, Prescription / Medication, Discharge Summary

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Exporter | Exporter registers as a client on the KEPHIS ECS portal. | Digital | |
| 2 | Exporter | Exporter applies for Phytosanitary Certificate for a specific consignment. | Manual | |
| 3 | KEPHIS Inspector | KEPHIS inspector inspects the consignment at the packhouse/exit point. | Manual | |
| 4 | KEPHIS Lab | Samples may be taken for laboratory analysis. | Manual | |
| 5 | Exporter | Upon compliance, Exporter pays inspection fees. | Manual | |
| 6 | KEPHIS | KEPHIS issues the Phytosanitary Certificate. | Manual | |

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
