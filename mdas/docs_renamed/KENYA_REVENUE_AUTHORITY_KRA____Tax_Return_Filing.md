# KENYA REVENUE AUTHORITY (KRA) – Tax Return Filing

## Cover Page
- **Ministry/Department/Agency (MDA):** KENYA REVENUE AUTHORITY (KRA)
- **Process Name:** Tax Return Filing
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The National Treasury of Kenya is the primary government entity responsible for formulating financial and economic policies, and overseeing the effective coordination of government financial operations. Its mandate includes national budget preparation, public debt management, and resource mobilization.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Taxpayer [Taxpayer]
        S1["Taxpayer logs into the KRA iTax portal (itax.kra.g..."]
        S2["Taxpayer selects 'Returns' menu and chooses 'File ..."]
        S3["Taxpayer selects the tax obligation (e.g., Income ..."]
        S4["Taxpayer downloads the Excel/ODS return form (or u..."]
        S5["Taxpayer fills the return form offline and uploads..."]
        S7["Taxpayer downloads and prints the Acknowledgement ..."]
    end
    subgraph System [System]
        S6["System validates the return and generates an E-Ret..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> End((End))
```

---

## Process Overview
### Process Name
Tax Return Filing

### Service Category
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within KENYA REVENUE AUTHORITY (KRA).

### Triggers
- Submission of application/request by Taxpayer.

### End States
- **Successful:** Tax Compliance Certificate, Assessment Order, Release Order

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| System | Process Actor | Performs actions as defined in steps. |
| Taxpayer | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Tax Return Form, Bank Statements, Import Entry Declaration
- **Outputs:** Tax Compliance Certificate, Assessment Order, Release Order

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Taxpayer | Taxpayer logs into the KRA iTax portal (itax.kra.go.ke) using PIN and password. | Digital | |
| 2 | Taxpayer | Taxpayer selects 'Returns' menu and chooses 'File Return' or 'File Nil Return'. | Manual | |
| 3 | Taxpayer | Taxpayer selects the tax obligation (e.g., Income Tax Resident) and period. | Manual | |
| 4 | Taxpayer | Taxpayer downloads the Excel/ODS return form (or uses the web-based form for simple returns). | Manual | |
| 5 | Taxpayer | Taxpayer fills the return form offline and uploads the generated ZIP file back to the portal. | Digital | |
| 6 | System | System validates the return and generates an E-Return Acknowledgement Receipt. | Manual | |
| 7 | Taxpayer | Taxpayer downloads and prints the Acknowledgement Receipt. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Tax evasion
- Complex filing process
- System downtime

### Opportunities
- Data warehousing/Analytics
- Real-time VAT monitoring (TIMS)
- AI for fraud detection

---

## KPIs
| KPI | Baseline | Target |
|---|---|---|
| Turnaround Time | 30 Days | 5 Days |
| CSAT | 50% | 90% |
