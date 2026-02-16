# Ministry of Agriculture and Livestock Development – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Ministry of Agriculture and Livestock Development
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official
- **Status:** High Priority (POC List)

---

## Executive Summary
Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Ministry. Included as Tier 3 for light‑touch desk review/survey.

---

## Service Mandate & Legal Basis
### Statutory Mandate
Represents 'Agriculture Rural and Urban Development' cluster for balanced coverage; entity type: Ministry. Included as Tier 3 for light‑touch desk review/survey.

### Legal Context
- The Ministry of Agriculture and Livestock Development Act (Inferred).

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
- **In Scope:** End-to-end processing within Ministry of Agriculture and Livestock Development.

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
    subgraph Artist [Artist]
        S1["Artist registers on 'Talanta Hela' / Culture Porta..."]
    end
    subgraph System [System]
        S2["System verifies identity via IPRS API."]
        S3["Artist uploads portfolio/work; System checks Copyr..."]
        S4["Artist is issued a 'Creative ID' card."]
        S5["Grants/Royalties are processed automatically based..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> End((End))
```

## Future State Process (TO-BE)
### Narrative
The To-Be process establishes a National Creative Registry. Artists register once, and their work is authenticated against the Copyright Board, enabling access to royalties and government grants.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Artist | Artist registers on 'Talanta Hela' / Culture Portal. | Culture Portal |
| 2 | System | System verifies identity via IPRS API. | Service Bus / IPRS |
| 3 | System | Artist uploads portfolio/work; System checks Copyright Board database for IP ownership. | Service Bus / KECOBO |
| 4 | System | Artist is issued a 'Creative ID' card. | Registry |
| 5 | System | Grants/Royalties are processed automatically based on registered works. | Payment Engine |

---

## References & Evidence
The information in this document was derived from the following official sources:

- Official Mandate and Service Charter (Inferred from Statutory Acts).
