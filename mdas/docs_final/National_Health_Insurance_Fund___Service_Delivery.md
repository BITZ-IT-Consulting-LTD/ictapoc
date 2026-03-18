# NATIONAL HEALTH INSURANCE FUND (NHIF/SHA) – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** NATIONAL HEALTH INSURANCE FUND (NHIF) / SOCIAL HEALTH AUTHORITY (SHA)
- **Process Name:** Member Registration & Claims (Health Insurance)
- **Document Version:** 1.3
- **Date:** 2026-02-19
- **Classification:** Official

---

## Executive Summary
The National Health Insurance Fund (transitioning to the Social Health Authority - SHA) is mandated to provide health insurance to all Kenyans. Registration is mandatory for all adults. The process involves member registration, monthly contributions, and pre-authorization of medical claims.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (SHA Registration).*

### 1.1 AS-IS Process Flow (BPMN 2.0)
```mermaid
flowchart TD
    subgraph Citizen["Citizen / Applicant"]
        Start(( )) --> A1[Access SHA Registration]
        A1 --> A2[Enter National ID Number]
        A4[Provide Household Details] --> A5[Submit Registration]
        A8[Make Contribution] --> A9[Coverage Activated]
    end

    subgraph System["SHA System"]
        A2 --> B1[Fetch Bio-data from IPRS]
        B1 --> A4
        A5 --> B2[Create Membership Record]
        B2 --> B3[Execute Means Testing Assessment]
        B3 --> A8
    end

    A9 --> End((( )))

    style Start fill:#fff,stroke:#27ae60,stroke-width:2px
    style End fill:#fff,stroke:#e74c3c,stroke-width:4px
```

---

## Process Overview
### Process Name
Member Registration & Benefit Access (UHC)

### Service Category
- G2C (Government to Citizen)

### Scope
- **In Scope:** Registration of Principal Member + Spouse/Children; Collection of Premiums; Pre-Authorization of specialized care (Surgery, MRI, Dialysis); Claims processing.
- **Out of Scope:** Private insurance top-ups.

### Triggers
- Employment (Statutory Deduction).
- Need for medical cover (Voluntary Contributor).

### End States
- **Successful:** Medical bill settled by Fund.

### Policy Context
- Social Health Insurance Act, 2023; NHIF Act (Repealed/Transitional).

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Principal Member | Beneficiary | Registers family, pays premiums, seeks treatment. |
| Employer | Remitter | Deducts and remits contributions by 9th of month. |
| Healthcare Provider | Service | Treats patient, seeks pre-auth, files claims. |
| SHA/NHIF Officer | Adjudicator | Reviews pre-auth requests and audits claims. |

---

## Detailed Process (AS-IS)
**AS-IS Steps: SHA Registration (Current Process)**
*Agency: Social Health Authority*
*System: SHA Portal / USSD / eCitizen / Physical Registration*
*(SHA replaced NHIF under Universal Health Coverage reforms)*

| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Citizen | **Access:** Citizen accesses SHA Registration via Online Portal, eCitizen, USSD, or Registration Center. | SHA Portal/USSD | |
| 2 | Citizen | **Enter ID:** Citizen enters National ID Number. | Digital/Manual | |
| 3 | System | **Retrieve Details:** System automatically fetches Name, Date of Birth, and Gender. | IPRS/System | |
| 4 | Citizen | **Provide Details:** Citizen enters Phone Number, Email, Residence, and Household/Dependants. | Digital/Manual | |
| 5 | Citizen | **Submit:** Citizen confirms and submits registration. | Digital/Manual | |
| 6 | System | **Generate SHA Number:** System creates SHA Membership Record linked to National ID. | SHA System | |
| 7 | System | **Assessment:** System determines contribution amount based on income level / means testing. | SHA System | |
| 8 | Citizen | **Contribution:** Citizen pays via Mobile Money, Bank, or Employer deduction. | Payment Gateway | |
| 9 | System | **Activation:** Coverage Activated. Citizen becomes eligible for healthcare services. | SHA System | |

---

## Pain Points & Opportunities
### Pain Points
- **Card Activation:** 60-day waiting period for voluntary contributors discourages enrollment.
- **Biometric Failure:** Fingerprint scanners at hospitals often fail, forcing manual forms.
- **Pre-Auth Delays:** Critical surgeries delayed waiting for an email/system approval from HQ.
- **Dependent Verification:** Adding a spouse/child is a manual nightmare of uploading documents.
- **Fraud:** "Ghost Procedures" billed by rogue hospitals leading to fund loss.

### Opportunities
- **Instant Activation:** Link with Mobile Money history to score creditworthiness and activate immediately.
- **AI Adjudication:** Use AI to auto-approve standard pre-auth requests (e.g., Malaria, Normal Delivery) instantly.
- **IPRS Link:** Auto-populate dependents from Birth/Marriage records (CRS/AG) to remove document upload burden.
- **Real-Time Settlement:** Pay hospitals within 7 days using automated claim vetting.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
### 2.1 TO-BE Process (BPMN 2.0 - POC v2 Aligned)
```mermaid
flowchart TD
    subgraph Event["Point of Event"]
        Start(( )) --> E1[Life Event: ID Issuance / Birth / Employment]
    end

    subgraph System["SHA Core Engine"]
        E1 --> S1[Query IPRS/CRS for Profile Creation]
        S1 --> S2[Auto-link Dependants]
        S2 --> S3[Intelligent Means Testing]
        S3 --> S4[Calculate Contribution Target]
    end

    subgraph Finance["Payment Gateway / Employer"]
        S4 --> F1[Auto-deduction & API Remittance]
    end

    subgraph Final["Citizen Engagement"]
        F1 --> C1[Coverage Activated Instantly]
        C1 --> End((( )))
    end

    style Start fill:#fff,stroke:#27ae60,stroke-width:2px
    style End fill:#fff,stroke:#e74c3c,stroke-width:4px
```

## Future State Process (TO-BE)
### Narrative
**TO-BE Process: Automated SHA Registration and Means Testing**

**Design Principles:**
- Proactive & Event-Driven Enrollment
- Zero Duplicate Data Entry
- Automated Dependent Verification
- Intelligent Means Testing via Inter-Agency APIs

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | System | **Trigger Event:** Citizen receives National ID (turns 18), gets first employment (KRA PAYE), or registers a birth/marriage. | NRB / KRA / CRS |
| 2 | System | **Profile Creation:** System automatically fetches bio-data from National Population Registry to create/update SHA profile. | SHA System / IPRS |
| 3 | System | **Dependent Linking:** System automatically links spouse and children using data from Civil Registration Services. No manual uploads. | SHA System / CRS |
| 4 | System | **Assessment:** System determines contribution amount by querying KRA for formal income or alternative data (Mobile Money) for informal sector. | SHA System / KRA API |
| 5 | Citizen/Employer | **Contribution:** Employer payroll automatically deducts and remits via API. Informal citizens receive a prompt to authorize recurring Mobile Money payments. | Payroll / Payment Gateway |
| 6 | System | **Activation:** Coverage is activated instantly upon system processing. Citizen is notified via SMS/Email. | SHA System |

---

## 3. Standard Data Inputs
*Required fields for the WoG Digital Service.*

### A. SHA Registration & Assessment
| Field Name | Type | Source | Validation |
|---|---|---|---|
| National ID Number | String | System Fetch (NRB/IPRS) | Match vs IPRS |
| Dependants (Birth/Marriage Certs) | String | System Fetch (CRS) | Verified by CRS |
| Income / Tax Band | Currency | System Fetch (KRA) | API Token |


## References
- Social Health Insurance Act.


---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)
