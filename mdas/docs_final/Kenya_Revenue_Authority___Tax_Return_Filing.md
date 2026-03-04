# KENYA REVENUE AUTHORITY (KRA) – Tax Return Filing & PIN Registration

## Cover Page
- **Ministry/Department/Agency (MDA):** KENYA REVENUE AUTHORITY (KRA)
- **Process Names:** KRA PIN Registration, Tax Return Filing
- **Document Version:** 2.0
- **Date:** 2026-02-24
- **Classification:** Official

---

## Executive Summary
The Kenya Revenue Authority (KRA) is the principal government agency responsible for the assessment, collection, and accounting of all government revenues. Utilizing the iTax portal, KRA manages the registration of individuals and businesses into the tax system (PIN Registration) and oversees the mandatory periodic filing of tax returns to ensure national economic compliance.

---

## Process 1: KRA PIN Registration

### 1.1 AS-IS Process Flowchart (BPMN 2.0)
```mermaid
graph TD
    Start((Start)) --> S1
    S1["Determine Eligibility (Citizen, Resident, Business)"] --> S2
    S2["Gather Required Documents (ID, BRS Cert, Utility Bills)"] --> S3
    S3["Log into iTax Portal & Create Account"] --> S4
    S4["Fill PIN Registration Form (Personal or Business details)"] --> S5
    S5["Submit Application Online via iTax & Get Acknowledgement"] --> S6
    S6["KRA Verifies Identity (IPRS/NRB) & Business validity (BRS)"] --> S7
    S7["PIN Issuance (Linked to individual/business profile)"] --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    class Start start;
    class End endNode;
```

### 1.2 Detailed Process (AS-IS)
| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Applicant | **Eligibility Check:** Determines eligibility (citizens, residents, businesses earning taxable income). | Manual | |
| 2 | Applicant | **Documentation:** Gathers National ID / BRS documents and supporting docs (utility bills, leases). | Physical/Scans | |
| 3 | Applicant | **Portal Access:** Logs into iTax, provides details, and links National ID or BRS Number. | iTax Portal | |
| 4 | Applicant | **Form Fill:** Fills KRA PIN application form with full name, ID, contact details (or director details for businesses). | iTax Portal | |
| 5 | Applicant | **Submission:** Submits form online via iTax. System generates Acknowledgement Receipt. | iTax Portal | |
| 6 | KRA | **Verification:** Verifies identity against IPRS/NRB and business validity against BRS. Checks for duplicate PINs. | KRA Backend | |
| 7 | System | **Issuance:** Issues KRA PIN, linking it to the individual or business profile. | iTax Portal | |

### 1.3 TO-BE Process (Inferred)
**Design Principles:** Zero-Registration (Auto-PIN Generation), Real-time Inter-agency Sync.

```mermaid
graph TD
    Start((Start)) --> T1
    T1["Trigger: Citizen turns 18 (NRB) or Business is Registered (BRS)"] --> T2
    T2["System automatically generates KRA PIN via X-Road API"] --> T3
    T3["KRA securely stores PIN linked to Maisha Namba/Business No."] --> T4
    T4["Auto-notification sent to Citizen/Business with digital PIN Certificate"] --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    class Start start;
    class End endNode;
```

| Step | Role | Action | System |
|---|---|---|---|
| 1 | System | **Trigger Event:** Citizen receives ID (NRB) or business is incorporated (BRS). | NRB / BRS APIs |
| 2 | System | **Auto-Generation:** Instantly generates KRA PIN based on the new identity/business record. No manual application needed. | KRA Core Engine |
| 3 | System | **Data Sync:** Syncs the newly generated PIN with the central Golden Record (IPRS). | Inter-Agency Hub |
| 4 | System | **Digital Issuance:** Dispatches the Verifiable Digital PIN Certificate via SMS/eCitizen Wallet. | Notification Gateway |

---

## Process 2: Tax Return Filing

### 2.1 AS-IS Process Flowchart (BPMN 2.0)
```mermaid
graph TD
    Start((Start)) --> S1
    S1["Taxpayer logs into iTax using PIN and Password"] --> S2
    S2["Select Tax Type (PAYE, VAT, Income Tax, Corporate)"] --> S3
    S3["Prepare Tax Return (Enter Income, Expenses, Tax Payable)"] --> S4
    S4["Submit Tax Return online & Get Acknowledgement Receipt"] --> S5
    S5["Pay Tax Due (M-Pesa, Bank Transfer, Card)"] --> S6
    S6["KRA Updates Compliance Records and Tax Return History"] --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    class Start start;
    class End endNode;
```

### 2.2 Detailed Process (AS-IS)
| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Taxpayer | **Login:** Logs into iTax using PIN and password. | iTax Portal | |
| 2 | Taxpayer | **Selection:** Selects Tax Type (PAYE, VAT, Income Tax, Corporation Tax). | iTax Portal | |
| 3 | Taxpayer | **Preparation:** Enters required details: Income, revenue, expenses, deductions, tax payable. | iTax Portal / Excel | Often requires downloading complex Excel sheets. |
| 4 | Taxpayer | **Submission:** Reviews and submits the return online. System generates Acknowledgement Receipt. | iTax Portal | |
| 5 | Taxpayer | **Payment:** Pays tax due via M-Pesa, Bank transfer, or online card payment. | Payment Gateway | |
| 6 | KRA | **Reporting:** Maintains PIN database, tax returns history, and compliance records. | iTax Backend | |

### 2.3 TO-BE Process (Inferred)
**Design Principles:** Auto-Populated Returns, Open Banking Integration, Smart Compliance.

```mermaid
graph TD
    Start((Start)) --> T1
    T1["Taxpayer accesses KRA via eCitizen SSO"] --> T2
    T2["System auto-populates Income/VAT data from eTIMS, IFMIS, and Banks"] --> T3
    T3["Taxpayer reviews auto-calculated draft return and deductions"] --> T4
    T4["Taxpayer digitally signs and submits return with one click"] --> T5
    T5["Instant payment via Gov Gateway & auto-issuance of Compliance Cert"] --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    class Start start;
    class End endNode;
```

| Step | Role | Action | System |
|---|---|---|---|
| 1 | Taxpayer | **SSO Access:** Logs in securely via unified eCitizen Identity. | eCitizen SSO |
| 2 | System | **Auto-Population:** Automatically fetches PAYE data from employers, sales data from eTIMS, and relevant financial data to pre-fill the return. | X-Road (eTIMS/IFMIS) |
| 3 | Taxpayer | **Review:** Reviews the auto-calculated tax liability and verifies applicable deductions. | KRA Portal |
| 4 | Taxpayer | **Submission:** Digitally signs and submits the pre-filled return with a single click. | KRA Portal |
| 5 | System | **Payment & Clearance:** Processes payment seamlessly and instantly issues a Verifiable Tax Compliance Certificate (TCC). | Payment Gateway |

---

## References
- Kenya Revenue Authority Act.
- Income Tax Act.