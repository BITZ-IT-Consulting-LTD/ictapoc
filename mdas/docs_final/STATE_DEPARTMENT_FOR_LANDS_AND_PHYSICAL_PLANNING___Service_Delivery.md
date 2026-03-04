# MINISTRY OF LANDS AND PHYSICAL PLANNING – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** MINISTRY OF LANDS AND PHYSICAL PLANNING
- **Process Names:** Land Registration / Title Deed Issuance, Property Transfer (Change of Ownership)
- **Document Version:** 2.0
- **Date:** 2026-02-24
- **Classification:** Official

---

## Executive Summary
The Ministry of Lands manages land administration, registration, valuation, and physical planning. It operates the **Ardhisasa** digital platform to facilitate secure, transparent, and efficient land transactions, including the registration of new title deeds and the transfer of property ownership between parties.

---

## Process 1: Land Registration / Title Deed Issuance

### 1.1 AS-IS Process Flowchart (BPMN 2.0)
```mermaid
graph TD
    Start((Start)) --> S1
    S1["Create Ardhisasa Account & Login"] --> S2
    S2["Submit Land Registration Application"] --> S3
    S3["Upload Supporting Documents"] --> S4
    S4["Pay Registration Fees & Stamp Duty"] --> S5
    S5["Land Office Verification (Registrar Reviews)"] --> S6
    S6["Approval of Registration"] --> S7
    S7["Title Deed Generated"] --> S8
    S8["Title Deed Issued (Downloaded or Collected)"] --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    class Start start;
    class End endNode;
```

### 1.2 Detailed Process (AS-IS)
| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Citizen/Lawyer | **Account Creation:** Registers on Ardhisasa using ID, KRA PIN, Email, and Phone. | Ardhisasa Portal | |
| 2 | Citizen/Lawyer | **Login:** Logs into the Ardhisasa portal. | Ardhisasa Portal | |
| 3 | Citizen/Lawyer | **Application:** Selects Land Registration Service; Enters Parcel and Owner details. | Ardhisasa Portal | |
| 4 | Citizen/Lawyer | **Uploads:** Uploads Sale Agreement, Transfer Forms, ID, PIN, and Consents. | Ardhisasa Portal | |
| 5 | Citizen/Lawyer | **Payment:** Pays Stamp Duty, Registration Fees, and other charges. | Payment Gateway | |
| 6 | Registrar | **Verification:** Reviews ownership documents, parcel info, and clearance/consent. | Ardhisasa Backend | |
| 7 | Registrar | **Approval:** Approves the land registration. | Ardhisasa Backend | |
| 8 | System | **Generation:** System generates Title Deed registered in the owner's name. | Ardhisasa System | |
| 9 | Owner | **Issuance:** Owner downloads or physically collects the Title Deed. | Ardhisasa/Registry | |

### 1.3 TO-BE Process (Inferred)
**Design Principles:** Inter-agency Auto-Verification, Smart E-Payments, Verifiable Digital Titles.

```mermaid
graph TD
    Start((Start)) --> T1
    T1["Citizen authenticates via eCitizen SSO; System auto-fetches ID & KRA data"] --> T2
    T2["Citizen submits digital application; Smart forms replace manual uploads"] --> T3
    T3["System auto-calculates fees and processes instant payment via Gov Gateway"] --> T4
    T4["Automated Rules Engine verifies encumbrances and inter-agency consents"] --> T5
    T5["Registrar conducts final review on digital dashboard and applies e-Signature"] --> T6
    T6["System issues a Verifiable Digital Title Deed (QR Code/Blockchain) instantly"] --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    class Start start;
    class End endNode;
```

| Step | Role | Action | System |
|---|---|---|---|
| 1 | Citizen | Authenticate via single sign-on; profiles auto-populated. | eCitizen / IPRS / KRA |
| 2 | Citizen | Complete smart-form application. | Land Portal |
| 3 | System | Calculate and process all fees (Stamp Duty, etc.) instantly. | Integrated Payment Gateway |
| 4 | System | Auto-verify land status, liens, and spousal/board consents. | Inter-Agency API / Rules Engine |
| 5 | Registrar | Review flagged items and digitally approve the registration. | Officer Workbench |
| 6 | System | Generate and push Verifiable Digital Title to citizen's digital wallet. | Digital Registry / Wallet |

---

## Process 2: Property Transfer (Change of Ownership)

### 2.1 AS-IS Process Flowchart (BPMN 2.0)
```mermaid
graph TD
    Start((Start)) --> S1
    S1["Initiate Transfer Application on Ardhisasa"] --> S2
    S2["Enter Property, Buyer, and Seller Details"] --> S3
    S3["Upload Transfer Documents (Forms, Agreement, Consents)"] --> S4
    S4["Pay Transfer Fees and Stamp Duty"] --> S5
    S5["Land Registrar Reviews Application"] --> S6
    S6["Transfer Approved"] --> S7
    S7["New Title Deed Issued in Buyer's Name"] --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    class Start start;
    class End endNode;
```

### 2.2 Detailed Process (AS-IS)
| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Buyer/Seller | **Initiate:** Logs into Ardhisasa and selects Property Transfer. | Ardhisasa Portal | |
| 2 | Buyer/Seller | **Details:** Enters Parcel Number, Seller Details, and Buyer Details. | Ardhisasa Portal | |
| 3 | Buyer/Seller | **Uploads:** Uploads Signed Transfer Forms, Sale Agreement, ID Copies, PINs, and Land Control Board Consent. | Ardhisasa Portal | |
| 4 | Buyer/Seller | **Payment:** Pays required transfer fees and Stamp Duty. | Payment Gateway | |
| 5 | Registrar | **Review:** Verifies ownership, payment, and legal compliance. | Ardhisasa Backend | |
| 6 | Registrar | **Approval:** Approves the transfer of property. | Ardhisasa Backend | |
| 7 | System | **Issuance:** Generates the new Title Deed in the Buyer’s name. | Ardhisasa System | |

### 2.3 TO-BE Process (Inferred)
**Design Principles:** Biometric Consents, Smart Contract Execution, Real-time Ledger Updates.

```mermaid
graph TD
    Start((Start)) --> T1
    T1["Parties initiate transfer via Portal; Biometric verification of Buyer & Seller"] --> T2
    T2["System auto-populates property data and verifies lack of encumbrances"] --> T3
    T3["Required consents (Spousal, LCB) obtained digitally via e-Signatures"] --> T4
    T4["Integrated payment of Stamp Duty and fees via Gov Gateway"] --> T5
    T5["Smart Contract executes transfer; Registrar signs digitally"] --> T6
    T6["New Verifiable Digital Title issued to Buyer; old Title is cryptographically retired"] --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    class Start start;
    class End endNode;
```

| Step | Role | Action | System |
|---|---|---|---|
| 1 | Buyer/Seller | Initiate smart transfer; identities confirmed biometrically. | Portal / IPRS (Maisha) |
| 2 | System | Fetch authoritative property data; check for active cautions/liens. | Digital Land Registry |
| 3 | Parties | Provide digital, verifiable consents (e.g., spousal consent via AG link). | e-Signature / API |
| 4 | Buyer | Process Stamp Duty and transfer fees seamlessly. | Payment Gateway |
| 5 | System/Registrar| Execute transfer via rules engine/smart contract; final digital approval. | Smart Contract / Workbench |
| 6 | System | Issue new digital title to buyer; permanently archive previous ownership record. | Blockchain / Immutable Ledger |