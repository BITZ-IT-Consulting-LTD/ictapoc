# STATE DEPARTMENT FOR IMMIGRATION AND CITIZEN SERVICES – Passport Application

## Cover Page
- **Ministry/Department/Agency (MDA):** STATE DEPARTMENT FOR IMMIGRATION AND CITIZEN SERVICES
- **Process Name:** Passport Application
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official
- **Status:** High Priority (POC List)

---

## Executive Summary
The State Department for Immigration and Citizen Services in Kenya controls and regulates the entry, exit, and residency of individuals, manages citizenship, and provides related services. It is responsible for issuing passports and other travel documents, as well as maintaining population registers for citizens and foreign nationals.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To control and regulate immigration, manage citizenship applications, issue travel and identification documents, and ensure secure and efficient citizen services in accordance with national laws and policies.

### Legal Context
- Mandate derived from Chapter 3 of the Constitution of Kenya 2010, the Kenya Citizenship and Immigration Act, 2011, and the Kenya Citizenship and Immigration Regulations, 2012. Other relevant laws and policies also apply.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant logs into the eCitizen portal and naviga..."]
        S2["Applicant fills the online passport application fo..."]
        S3["Applicant uploads scanned copies of ID, Birth Cert..."]
        S4["Applicant pays the fee via M-Pesa."]
        S5["Applicant downloads application form and receipt."]
        S6["Applicant books appointment for biometrics."]
        S7["Applicant visits Immigration Center for biometrics..."]
        S9["Applicant collects passport."]
    end
    subgraph Immigration [Immigration]
        S8["Passport is processed and printed."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> S9
    S9 --> End((End))
```

---

## Process Overview
### Service Category
- G2C (Government to Citizen)

### Scope
- **In Scope:** End-to-end processing within STATE DEPARTMENT FOR IMMIGRATION AND CITIZEN SERVICES.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** e-Passport, Visa, Work Permit

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| Immigration | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Old Passport/ID, Birth Certificate, Biometrics (Fingerprints, Face)
- **Outputs:** e-Passport, Visa, Work Permit

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant logs into the eCitizen portal and navigates to Immigration Services. | Digital | |
| 2 | Applicant | Applicant fills the online passport application form. | Manual | |
| 3 | Applicant | Applicant uploads scanned copies of ID, Birth Certificate, etc. | Manual | |
| 4 | Applicant | Applicant pays the fee via M-Pesa. | Manual | |
| 5 | Applicant | Applicant downloads application form and receipt. | Manual | |
| 6 | Applicant | Applicant books appointment for biometrics. | Manual | |
| 7 | Applicant | Applicant visits Immigration Center for biometrics. | Manual | |
| 8 | Immigration | Passport is processed and printed. | Manual | |
| 9 | Applicant | Applicant collects passport. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Crowding at Nyayo House
- Delay in printing
- Manual file retrieval

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
        S1["Applicant logs in via Single Sign-On (eCitizen) us..."]
        S3["Applicant selects appointment for biometric captur..."]
    end
    subgraph System [System]
        S2["System retrieves Birth Certificate details automat..."]
        S4["Payment is processed via Government Payment Gatewa..."]
        S6["Passport is printed and applicant notified via SMS..."]
    end
    subgraph Officer [Officer]
        S5["Immigration Officer retrieves verified data; appro..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> End((End))
```

## Future State Process (TO-BE)
### Narrative
The To-Be Passport process integrates directly with the Civil Registration Service (Births) and National ID Registry (IPRS) via the Government Service Bus, eliminating the need for physical document verification. Biometrics are validated in real-time.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Applicant | Applicant logs in via Single Sign-On (eCitizen) using National ID. | SSO / IPRS |
| 2 | System | System retrieves Birth Certificate details automatically from Civil Registration Services via Service Bus. | Service Bus / CRS API |
| 3 | Applicant | Applicant selects appointment for biometric capture (if not already in IPRS). | Booking System |
| 4 | System | Payment is processed via Government Payment Gateway; receipt auto-generated. | Payment Gateway |
| 5 | Officer | Immigration Officer retrieves verified data; approves for printing. | Passport Production System |
| 6 | System | Passport is printed and applicant notified via SMS. | Notification Service |

---

## References & Evidence
The information in this document was derived from the following official sources:

- [https://immigration.go.ke/](https://immigration.go.ke/)
- [https://ecitizen.go.ke/](https://ecitizen.go.ke/)
