# National Authority for the Campaign Against Alcohol And Drug Abuse – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** National Authority for the Campaign Against Alcohol And Drug Abuse
- **Process Name:** Service Delivery
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
    subgraph Applicant [Applicant]
        S1["Importer/Exporter registers on NACADA Portal."]
        S2["Applicant submits dossier (Product sample, KEBS ce..."]
        S4["Applicant pays the licensing fee."]
    end
    subgraph NACADAInspector [NACADA Inspector]
        S3["NACADA conducts physical inspection of storage/pre..."]
    end
    subgraph NACADA [NACADA]
        S5["NACADA issues Import/Export License."]
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
Service Delivery

### Service Category
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within National Authority for the Campaign Against Alcohol And Drug Abuse.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| NACADA Inspector | Process Actor | Performs actions as defined in steps. |
| NACADA | Process Actor | Performs actions as defined in steps. |
| Applicant | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Importer/Exporter registers on NACADA Portal. | Digital | |
| 2 | Applicant | Applicant submits dossier (Product sample, KEBS cert, KRA Tax Compliance). | Manual | |
| 3 | NACADA Inspector | NACADA conducts physical inspection of storage/premises. | Manual | |
| 4 | Applicant | Applicant pays the licensing fee. | Manual | |
| 5 | NACADA | NACADA issues Import/Export License. | Manual | |

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
