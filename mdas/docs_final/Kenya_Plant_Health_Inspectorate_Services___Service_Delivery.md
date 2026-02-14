# Kenya Plant Health Inspectorate Services – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Kenya Plant Health Inspectorate Services
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the AS-IS process flow across different actors.*

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
Service Delivery

### Service Category
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within Kenya Plant Health Inspectorate Services.

### Triggers
- Submission of application/request by Exporter.

### End States
- **Successful:** Patient File / EMR Record, Diagnostic Lab Reports, Prescription / Medication, Discharge Summary

### Policy Context
- The Kenya Plant Health Inspectorate Services Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| KEPHIS Lab | Process Actor | Performs actions as defined in steps. |
| Exporter | Process Actor | Performs actions as defined in steps. |
| KEPHIS | Process Actor | Performs actions as defined in steps. |
| KEPHIS Inspector | Process Actor | Performs actions as defined in steps. |

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
- Integration with IPRS/BRS via Service Bus.
- Adoption of Government Payment Gateway.
- Implementation of Automated Rules Engine.
- Issuance of Digital Verifiable Credentials.

---

## Future State Process (TO-BE)
### Narrative
The To-Be process leverages the Government Service Bus to integrate with IPRS (Identity Registry) and the Payment Gateway. Manual data entry and document uploads are replaced by real-time API validations, enabling a paperless, cashless, and presence-less service experience.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Applicant | Applicant logs in via Single Sign-On (SSO) and selects the service. | Citizen Portal / SSO |
| 2 | System | Applicant enters National ID; System auto-populates details from IPRS (Identity Registry) via the Service Bus. | Service Bus / Registry API |
| 3 | System | System performs auto-validation of compliance (e.g., KRA Tax Status) via Inter-Agency APIs. | Service Bus / Compliance Engine |
| 4 | Applicant | Applicant pays fees via the Government Payment Gateway; System auto-receipts. | Payment Gateway |
| 5 | System | Application is processed by the Rules Engine. (Low-risk cases are Auto-Approved). | Workflow Engine |
| 6 | Officer | Complex cases are routed to the Officer Workbench for digital review and approval. | Officer Workbench |
| 7 | System | System generates a Verifiable Digital Certificate (QR Code) and notifies the applicant. | Output Generator |

---

## References & Evidence
The information in this document was derived from the following official sources:

- Official Mandate and Service Charter (Inferred from Statutory Acts).

---

## Appendices
See attached ERD and System Design.
