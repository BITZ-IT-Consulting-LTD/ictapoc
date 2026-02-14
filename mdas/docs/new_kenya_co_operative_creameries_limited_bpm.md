# STANDARD BPM TEMPLATE – New Kenya Co-operative Creameries Limited

## Cover Page
- **Ministry/Department/Agency (MDA):** New Kenya Co-operative Creameries Limited
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
    subgraph Farmer [Farmer]
        S1["Farmer delivers milk to New KCC Cooling Plant/Coll..."]
    end
    subgraph QualityClerk [Quality Clerk]
        S2["Milk is tested for quality (lactometer/alcohol tes..."]
    end
    subgraph Clerk [Clerk]
        S3["Delivery slip is issued to the farmer."]
    end
    subgraph Logistics [Logistics]
        S4["Milk is transported to main processing factory."]
    end
    subgraph Finance [Finance]
        S5["Farmer receives monthly payment based on volume an..."]
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
Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Service Category
- G2C/G2B

### Process Objective
- Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Agency. Included as Tier 3 for light‑touch desk review/survey.

### Scope
- **In Scope:** End-to-end processing within New Kenya Co-operative Creameries Limited.
- **Out of Scope:** External agency approvals.

### Triggers
- Submission of application/request by Farmer.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice
- **Unsuccessful:** Application rejected due to non-compliance.

### Policy Context
- The New Kenya Co-operative Creameries Limited Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Quality Clerk | Process Actor | Performs actions as defined in steps. |
| Finance | Process Actor | Performs actions as defined in steps. |
| Farmer | Process Actor | Performs actions as defined in steps. |
| Logistics | Process Actor | Performs actions as defined in steps. |
| Clerk | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Farmer | Farmer delivers milk to New KCC Cooling Plant/Collection Centre. | Manual | |
| 2 | Quality Clerk | Milk is tested for quality (lactometer/alcohol test) and weighed. | Manual | |
| 3 | Clerk | Delivery slip is issued to the farmer. | Manual | |
| 4 | Logistics | Milk is transported to main processing factory. | Manual | |
| 5 | Finance | Farmer receives monthly payment based on volume and quality. | Manual | |

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
