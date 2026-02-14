# Pharmacy and Poisons Board – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Pharmacy and Poisons Board
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
    subgraph Importer [Importer]
        S1["Importer logs into the PPB Online Portal."]
        S2["Importer applies for an Import Permit and uploads ..."]
        S4["Importer pays the permit fee (e.g., 2% of FOB valu..."]
    end
    subgraph PPBOfficer [PPB Officer]
        S3["PPB verifies the product registration status and i..."]
    end
    subgraph PPB [PPB]
        S5["PPB approves and issues the electronic Import Perm..."]
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
- **In Scope:** End-to-end processing within Pharmacy and Poisons Board.

### Triggers
- Submission of application/request by Importer.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| PPB Officer | Process Actor | Performs actions as defined in steps. |
| PPB | Process Actor | Performs actions as defined in steps. |
| Importer | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Importer | Importer logs into the PPB Online Portal. | Digital | |
| 2 | Importer | Importer applies for an Import Permit and uploads the Proforma Invoice. | Manual | |
| 3 | PPB Officer | PPB verifies the product registration status and invoice details. | Manual | |
| 4 | Importer | Importer pays the permit fee (e.g., 2% of FOB value). | Manual | |
| 5 | PPB | PPB approves and issues the electronic Import Permit. | Manual | |

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
