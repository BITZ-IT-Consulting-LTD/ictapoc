# Anti-Female Genital Mutilation Board – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Anti-Female Genital Mutilation Board
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Anti-Female Genital Mutilation Board is a semi-autonomous government agency in Kenya, established in December 2013 under the Prohibition of Female Genital Mutilation Act, 2011. Its core mandate is to design, supervise, and coordinate public awareness programs against the practice of Female Genital Mutilation (FGM), advise the Government on FGM matters, and lead national efforts to eradicate FGM. The Board plays a crucial role in upholding the dignity and empowerment of girls and women by ensuring the effective implementation of anti-FGM legislation and promoting alternative rites of passage.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1

    subgraph Reporter [Reporter]
        S1["Member of public reports FGM incident/threat via Hotline/..."]
    end

    subgraph Board_Police [Board/Police]
        S2["Anti-FGM Board coordinates with Police/Chief for interven..."]
    end

    subgraph Rescue_Team [Rescue Team]
        S3["Victim is rescued and taken to a safe house/medical facil..."]
    end

    subgraph Police [Police]
        S4["Suspects are arrested and statements recorded."]
    end

    subgraph Board_Legal_Team [Board Legal Team]
        S5["Board provides legal support for prosecution."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;

    class Start start;
    class End endNode;
    class S1,S2,S3,S4,S5 userTask;
```

---

## Process Overview
### Process Name
Service Delivery

### Service Category
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within Anti-Female Genital Mutilation Board.

### Triggers
- Submission of application/request by Reporter.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

### Policy Context
- The Anti-Female Genital Mutilation Board Act; The Constitution of Kenya 2010; Data Protection Act 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Reporter | Process Actor | Performs actions as defined in steps. |
| Board/Police | Process Actor | Performs actions as defined in steps. |
| Rescue Team | Process Actor | Performs actions as defined in steps. |
| Board Legal Team | Process Actor | Performs actions as defined in steps. |
| Police | Process Actor | Performs actions as defined in steps. |

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Reporter | Member of public reports FGM incident/threat via Hotline/Chief. | Manual | |
| 2 | Board/Police | Anti-FGM Board coordinates with Police/Chief for intervention. | Manual | |
| 3 | Rescue Team | Victim is rescued and taken to a safe house/medical facility. | Manual | |
| 4 | Police | Suspects are arrested and statements recorded. | Manual | |
| 5 | Board Legal Team | Board provides legal support for prosecution. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Manual document verification takes time.
- High cost and time for physical inspections.
- Risk of counterfeit licenses/certificates.
- Lack of real-time monitoring of licensees.

### Opportunities
- Integration with IPRS/BRS via Service Bus.
- Adoption of Government Payment Gateway.
- Implementation of Automated Rules Engine.
- Issuance of Digital Verifiable Credentials.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Optimized).*

```mermaid
graph TD
    Start((Start)) --> S1

    subgraph Applicant [Applicant]
        S1["Applicant logs in via Single Sign-On (SSO) and selects th..."]
        S4["Applicant pays fees via the Government Payment Gateway; S..."]
    end

    subgraph System [System]
        S2["Applicant enters Business Registration Number; System aut..."]
        S3["System performs auto-validation of compliance (e.g., KRA ..."]
        S5["Application is processed by the Rules Engine. (Low-risk c..."]
        S7["System generates a Verifiable Digital Certificate (QR Cod..."]
    end

    subgraph Officer [Officer]
        S6["Complex cases are routed to the Officer Workbench for dig..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;

    class Start start;
    class End endNode;
    class S1,S4,S6 userTask;
    class S2,S3,S5,S7 serviceTask;
```

## Future State Process (TO-BE)
### Narrative
The To-Be process leverages the Government Service Bus to integrate with BRS (Business Registry) and the Payment Gateway. Manual data entry and document uploads are replaced by real-time API validations, enabling a paperless, cashless, and presence-less service experience.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Applicant | Applicant logs in via Single Sign-On (SSO) and selects the service. | Citizen Portal / SSO |
| 2 | System | Applicant enters Business Registration Number; System auto-populates details from BRS (Business Registry) via the Service Bus. | Service Bus / Registry API |
| 3 | System | System performs auto-validation of compliance (e.g., KRA Tax Status) via Inter-Agency APIs. | Service Bus / Compliance Engine |
| 4 | Applicant | Applicant pays fees via the Government Payment Gateway; System auto-receipts. | Payment Gateway |
| 5 | System | Application is processed by the Rules Engine. (Low-risk cases are Auto-Approved). | Workflow Engine |
| 6 | Officer | Complex cases are routed to the Officer Workbench for digital review and approval. | Officer Workbench |
| 7 | System | System generates a Verifiable Digital Certificate (QR Code) and notifies the applicant. | Output Generator |

---

## References
Derived from official mandates.


---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)
