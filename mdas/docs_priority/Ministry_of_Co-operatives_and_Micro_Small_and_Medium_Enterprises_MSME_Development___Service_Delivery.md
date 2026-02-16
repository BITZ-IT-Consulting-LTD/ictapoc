# Ministry of Co-operatives and Micro, Small and Medium Enterprises (MSME) Development – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Ministry of Co-operatives and Micro, Small and Medium Enterprises (MSME) Development
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official
- **Status:** High Priority (POC List)

---

## Executive Summary
Represents 'General Economic and Commercial Affairs' cluster for balanced coverage; entity type: Ministry. Included as Tier 3 for light‑touch desk review/survey.

---

## Service Mandate & Legal Basis
### Statutory Mandate
Represents 'General Economic and Commercial Affairs' cluster for balanced coverage; entity type: Ministry. Included as Tier 3 for light‑touch desk review/survey.

### Legal Context
- The Ministry of Co-operatives and Micro, Small and Medium Enterprises (MSME) Development Act (Inferred).

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Citizen [Citizen]
        S1["Citizen/Stakeholder submits inquiry, complaint, or..."]
    end
    subgraph Registry [Registry]
        S2["Central Registry receives and tags the corresponde..."]
    end
    subgraph Directorate [Directorate]
        S3["Relevant Technical Directorate reviews and drafts ..."]
    end
    subgraph PSDirector [PS/Director]
        S4["Principal Secretary/Director approves the response..."]
    end
    subgraph Ministry [Ministry]
        S5["Ministry issues official response or policy guidel..."]
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
- **In Scope:** End-to-end processing within Ministry of Co-operatives and Micro, Small and Medium Enterprises (MSME) Development.

### Triggers
- Submission of application/request by Citizen.

### End States
- **Successful:** Policy Guidelines / Circulars, Official Response Letters, Cabinet Resolutions, Public Service Reports

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Citizen | Process Actor | Performs actions as defined in steps. |
| Registry | Process Actor | Performs actions as defined in steps. |
| PS/Director | Process Actor | Performs actions as defined in steps. |
| Directorate | Process Actor | Performs actions as defined in steps. |
| Ministry | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Public Inquiries / Petitions, Policy Proposals / Memos, Inter-agency Correspondence, Cabinet Memos
- **Outputs:** Policy Guidelines / Circulars, Official Response Letters, Cabinet Resolutions, Public Service Reports

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Citizen | Citizen/Stakeholder submits inquiry, complaint, or policy proposal via email or office. | Manual | |
| 2 | Registry | Central Registry receives and tags the correspondence. | Manual | |
| 3 | Directorate | Relevant Technical Directorate reviews and drafts response/action. | Manual | |
| 4 | PS/Director | Principal Secretary/Director approves the response. | Manual | |
| 5 | Ministry | Ministry issues official response or policy guideline. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Slow movement of physical files (Bureaucracy).
- Loss of institutional memory (Manual registries).
- Difficulty in tracking correspondence status.
- Siloed operations between departments.

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
