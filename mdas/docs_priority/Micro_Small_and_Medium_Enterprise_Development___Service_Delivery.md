# Micro, Small and Medium Enterprise Development – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Micro, Small and Medium Enterprise Development
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official
- **Status:** High Priority (POC List)

---

## Executive Summary
Represents 'General Economic and Commercial Affairs' cluster for balanced coverage; entity type: Department. Included as Tier 3 for light‑touch desk review/survey.

---

## Service Mandate & Legal Basis
### Statutory Mandate
Represents 'General Economic and Commercial Affairs' cluster for balanced coverage; entity type: Department. Included as Tier 3 for light‑touch desk review/survey.

### Legal Context
- The Micro, Small and Medium Enterprise Development Act (Inferred).

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Customer [Customer]
        S1["Customer/Stakeholder submits request, application,..."]
    end
    subgraph Registry [Registry]
        S2["Registry/Front Office receives, records, and class..."]
    end
    subgraph TechnicalOfficer [Technical Officer]
        S3["Relevant Technical Department reviews the request ..."]
    end
    subgraph Management [Management]
        S4["Management/Accounting Officer approves the appropr..."]
    end
    subgraph CustomerCare [Customer Care]
        S5["Service is delivered or official response is commu..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> End((End))
```

---

## Process Overview
### Service Category
- G2C/G2B

### Scope
- **In Scope:** End-to-end processing within Micro, Small and Medium Enterprise Development.

### Triggers
- Submission of application/request by Customer.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Technical Officer | Process Actor | Performs actions as defined in steps. |
| Registry | Process Actor | Performs actions as defined in steps. |
| Customer Care | Process Actor | Performs actions as defined in steps. |
| Management | Process Actor | Performs actions as defined in steps. |
| Customer | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Customer | Customer/Stakeholder submits request, application, or inquiry via official channels (Email, Letter, or Portal). | Digital | |
| 2 | Registry | Registry/Front Office receives, records, and classifies the request. | Manual | |
| 3 | Technical Officer | Relevant Technical Department reviews the request against internal policies and regulations. | Manual | |
| 4 | Management | Management/Accounting Officer approves the appropriate action or service delivery. | Manual | |
| 5 | Customer Care | Service is delivered or official response is communicated to the customer. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Manual document verification takes time.
- High cost and time for physical inspections.
- Risk of counterfeit licenses/certificates.
- Lack of real-time monitoring of licensees.

### Opportunities
- Integration with Government Service Bus.
- Real-time API validation with Authoritative Registries.
- Automated Rules Engine for decision making.
- Adoption of 'Once-Only' data principle.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Optimized with Service Bus & Registries).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["MSME Applicant dials USSD or uses App to request f..."]
    end
    subgraph System [System]
        S2["System calls Credit Scoring Engine (using Telco/CR..."]
        S3["System verifies Business Registration status via B..."]
        S4["Loan limit is calculated and presented to user."]
        S5["User accepts terms; Funds disbursed instantly to M..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> End((End))
```

## Future State Process (TO-BE)
### Narrative
The To-Be process is purely algorithmic. It utilizes data from MNOs (Mobile Network Operators) and BRS (Business Registry) to perform instant credit scoring and disbursement without human intervention.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Applicant | MSME Applicant dials USSD or uses App to request fund. | USSD/App |
| 2 | System | System calls Credit Scoring Engine (using Telco/CRB data) via Service Bus. | Credit Algorithm |
| 3 | System | System verifies Business Registration status via BRS API. | Service Bus / BRS |
| 4 | System | Loan limit is calculated and presented to user. | Rule Engine |
| 5 | System | User accepts terms; Funds disbursed instantly to Mobile Money wallet. | Disbursement Engine |

---

## References & Evidence
The information in this document was derived from the following official sources:

- Official Mandate and Service Charter (Inferred from Statutory Acts).
