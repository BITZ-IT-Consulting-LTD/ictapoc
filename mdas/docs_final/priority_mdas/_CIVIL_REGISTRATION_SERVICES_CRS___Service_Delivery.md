# CIVIL REGISTRATION SERVICES (CRS) – Service Delivery Refactored

## Cover Page
- **Ministry:** Ministry of Interior and National Administration
- **State Department:** State Department for Immigration and Citizen Services
- **Department:** Department of Civil Registration Services (CRS)
- **Document Type:** Business Process Document (Refactored)
- **Document Version:** 3.0 (Government Ready)
- **Date:** 2026-03-24
- **Classification:** Official / Sensitive
- **Strategic Category:** Priority MDA - National Registry
- **Life-Cycle Group:** Cradle to Grave
- **Reviewer:** Lead Government Business Analyst

---

## SECTION 1: CORRECTED SERVICE DEFINITION

The Department of Civil Registration Services (CRS) is mandated by the **Births and Deaths Registration Act (Cap. 149)** and the **Legitimacy Act (Cap. 145)** to provide compulsory and immediate registration of vital life events.

This document formally separates the workflows for Birth and Death registration to reflect distinct legal requirements, evidentiary standards, and system modules within the **Civil Registration and Vital Statistics System (CRVSS)**.

### Expanded Scope of Services
The scope is refactored to include critical but previously omitted services:
1.  **Birth Registration:** Current (under 6 months) and Late (after 6 months).
2.  **Death Registration:** Current (under 6 months) and Late (after 6 months).
3.  **Re-registration:** Legal amendments via Adoption, Recognition, and Legitimacy-bound amendments.
4.  **Foreign Event Registration:** Births and Deaths of Kenyans occurring outside national borders.
5.  **Assumption of Death:** Registration of deaths based on High Court orders for missing persons.

---

## SECTION 2: SERVICE CATALOGUE (COMPLETE)

| Category | Service Name | Target Population |
| :--- | :--- | :--- |
| **Core Services** | Birth Registration (Current) | Children born in Kenya (0-6 months) |
| | Death Registration (Current) | Deaths occurring in Kenya (0-6 months) |
| | Issuance of Certificates | All registered citizens/informants |
| **Extended Services** | Late Birth Registration | Persons over 6 months of age |
| | Late Death Registration | Deaths reported after 6 months |
| | Foreign Event Registration | Kenyan citizens abroad |
| **Special Case Services**| Re-registration (Adoption) | Children legally adopted |
| | Re-registration (Legitimization)| Children of parents who marry after birth |
| | Re-registration (Recognition) | Children where paternity is legally acknowledged |
| | Assumption of Death | Missing persons (Court ordered) |

---

## SECTION 3: AS-IS PROCESS FLOWS (CORRECTED)

Unlike previous versions, these flows distinguish between the manual "Legacy" track and the "CRVSS-enabled" digital track currently in operation.

### 1. Birth Registration – Manual (Paper-Based)
*Used in remote areas or where network/system downtime occurs.*

```mermaid
flowchart TD
    subgraph Facility_Chief["Health Facility / Chief"]
        Start1((" ")) --> A1["Issue Physical Notification"]
    end

    subgraph Informant["Parent / Informant"]
        A1 --> B1["Collect Notification & Documents"]
        B1 --> B2["Visit CRS District Office"]
        B2 --> B3["Submit Physical Forms & ID copies"]
        B7["Pay via eCitizen / Finance"] --> B8["Collect Handwritten Cert"]
        B8 --> End1(((" ")))
    end

    subgraph CRS["CRS District Registry"]
        B3 --> C1["Officer Verifies Paperwork"]
        C1 --> C2["Register in Physical Book A"]
        C2 --> C3["Registrar Signs Register"]
        C3 --> B7
    end
```

**Step-by-Step Structure:**
1. **Notification:** Informant receives a physical notification from the health facility or chief.
2. **Submission:** Informant physically travels to the CRS District Office with original notification and parents' IDs.
3. **Verification:** Registration Officer manually checks ID validity and cross-references physical records.
4. **Registration:** Details are handwritten into the Physical Birth Register (Register A) and assigned an Entry Number.
5. **Approval:** The Registrar reviews and manually signs the register entry.
6. **Payment:** Revenue is collected via manual receipting or semi-automated finance modules.
7. **Issuance:** A handwritten or typed physical certificate is produced and issued.

*   **Actors:** Informant/Parent, Health Worker/Chief, Registration Officer, Registrar.
*   **Systems:** Manual Registers, Finance Module (Partial).
*   **Pain Points:** High travel costs for citizens, risk of data entry errors, slow retrieval for verification, and storage/security risks for physical books.

### 2. Birth Registration – CRVSS-Enabled (Digital Track)
*The primary digital workflow integrated with eCitizen.*

```mermaid
flowchart TD
    subgraph Facility["Health Facility"]
        Start2((" ")) --> D1["Log Birth in CRS Notification App"]
    end

    subgraph CRVSS_System["CRVSS Cloud"]
        D1 --> D2["Sync Notification Metadata"]
        D3["Verify Parent ID via IPRS"] --> D4["Create Digital Entry"]
    end

    subgraph Citizen["Parent / Informant"]
        D2 --> E1["Apply via eCitizen Portal"]
        E1 --> D3
        D4 --> E2["Process Digital GPA Payment"]
        E2 --> E3["Download / Collect Cert"]
        E3 --> End2(((" ")))
    end
```

**Step-by-Step Structure:**
1. **Digital Notification:** Authorized notifier logs the event via the **CRS Notification App** at source.
2. **Synchronization:** Data flows to the central CRVSS database instantly.
3. **Application:** Parent logs into the **eCitizen** portal to submit a certificate request.
4. **Verification:** CRVSS automatically pings **IPRS** to validate the parental identities and Maisha Namba.
5. **Approval:** The Registrar approves the record digitally within the CRVSS workflow engine.
6. **Payment:** Fees are settled via the **Government Payment Aggregator (GPA)** on eCitizen.
7. **Certification:** A digital certificate record is created, available for download or high-security printing.

*   **Actors:** Health Worker, Parent, CRS Registrar, System Interface.
*   **Systems:** CRVSS, CRS Notification App, eCitizen, IPRS, GPA.
*   **Pain Points:** Dependent on internet connectivity in facilities, requires citizen digital literacy, and potential IPRS downtime delays.

### 3. Death Registration – Manual
```mermaid
flowchart TD
    subgraph Authority["Hospital / Police / Chief"]
        Start3((" ")) --> F1["Issue Burial Permit / Notification"]
    end

    subgraph Informant_D["Relative / Informant"]
        F1 --> G1["Collect Original Documents"]
        G1 --> G2["Visit CRS Office"]
        G2 --> G3["Fill Death Registration Forms"]
        G6["Pay Fees"] --> G7["Collect Manual Cert"]
        G7 --> End3(((" ")))
    end

    subgraph CRS_D["CRS Registry"]
        G3 --> H1["Verify Cause of Death Proof"]
        H1 --> H2["Record in Death Register"]
        H2 --> G6
    end
```

**Step-by-Step Structure:**
1. **Notification:** Family obtains a burial permit/manual notification from a hospital or chief.
2. **Registry Visit:** Family presents physical IDs and proof of death at the CRS Registry.
3. **Manual Entry:** Officer records details in the physical Death Register.
4. **Approval:** Registrar validates and signs the entry manually.
5. **Certification:** Manual death certificate is issued.

*   **Actors:** Family Informant, Hospital Staff/Chief, Registration Officer, Registrar.
*   **Systems:** Manual Registers.
*   **Pain Points:** High risk of identity theft/fraud where IPRS verification is missing, physical record deterioration, and delayed vital statistics reporting.

### 4. Death Registration – CRVSS-Enabled
```mermaid
flowchart TD
    subgraph Hospital["Medical Facility"]
        Start4((" ")) --> I1["Digital Death Notification"]
    end

    subgraph Citizen_D["Informant"]
        I1 --> J1["Apply for Death Cert on eCitizen"]
        J1 --> K1["Verify Deceased ID in IPRS"]
        K2["Approval in CRVSS"] --> J2["Pay via GPA"]
        J2 --> J3["Digital Certificate Issued"]
        J3 --> End4(((" ")))
    end

    subgraph CRVSS_D["CRVSS System"]
        K1 --> K2
    end
```

**Step-by-Step Structure:**
1. **Digital Notification:** Death is logged by an authorized clinical officer or pathologist via the **CRS Notification App**.
2. **Application:** Relatives apply for the certificate via the **eCitizen** death registry module.
3. **Verification:** System automatically executes a deceased ID lookup against **IPRS** to lock the identity.
4. **Approval:** Workflow is routed to the Registrar in **CRVSS** for digital approval.
5. **Certificate:** Secure certificate with verified entry number is issued digitally.

*   **Actors:** Hospital Pathologist, Family Informant, CRS Registrar.
*   **Systems:** CRVSS, CRS Notification App, eCitizen, IPRS, GPA.
*   **Pain Points:** Complexity in verifying community-based deaths digitally without immediate Chief intervention.

---

## SECTION 4: MISSING PROCESS FLOWS (NEW)

### Late Registration (Birth/Death)
*   **Trigger:** Application made after 6 months of event occurrence.
*   **Process:** Requires interview of the applicant by the District Coordinator, submission of secondary evidence (Clinic card, School records, Baptismal certificate), and vetting of witnesses.
*   **Approval:** Requires higher-level approval in CRVSS by the District Registrar or County Coordinator.

### Re-registration (Adoption/Legitimization/Recognition)
*   **Trigger:** Court Order (Adoption) or Statutory Declaration (Legitimization).
*   **Process:** The original entry in CRVSS is marked as "Cancelled - Re-registered." A new Entry Number is assigned in the special register.
*   **Output:** A new certificate is issued reflecting the updated parental/legal status while maintaining the original UPI link.

### Foreign Registrations
*   **Process:** Informant presents certified copies of foreign birth/death certificates and proof of Kenyan citizenship to CRS Headquarters. Events are registered in the **Foreign Registry module** of CRVSS.

### Assumption of Death
*   **Requirement:** Declaratory judgment from the High Court (typically after 7 years of disappearance).
*   **Process:** CRS registers the entry based on the court decree as a "Special Entry" to allow the estate to be processed.

---

## SECTION 5: SYSTEM LANDSCAPE (AS-IS REALITY)

The CRS technical architecture is NOT "future state" only; it is an active ecosystem managed by the department:

1.  **CRVSS (Core System):** The central database for all vital events. It manages the lifecycle from notification to certification.
2.  **CRS Notification App:** A mobile/web interface used by **Authorized Notifiers** (Nurses, Clinical Officers, and Chiefs) to capture events at source.
3.  **eCitizen Front-end:** The citizen-facing portal for applications, status tracking, and payments.
4.  **IPRS Integration:** Mandatory real-time link used by CRVSS to verify identities of informants and the deceased/parents.
5.  **GPA (Government Payment Aggregator):** The unified engine for all revenue collection.

---

## SECTION 6: CORRECTED PAIN POINTS

1.  **Historical Backlog:** Approximately **10 million** birth and death records exist only in physical paper registers across the country, invisible to real-time verification.
2.  **Registry Congestion:** Centralized registries (Kabarnet Gardens) and regional vaults are at maximum physical capacity, increasing the risk of record deterioration.
3.  **Double Entry Risks:** Where manual notifications are used, there is a delay between the physical paper and the system entry, leading to potential data inconsistency.
4.  **Identity Vulnerabilities:** Fraudulent registration of deaths to claim insurance is a risk where IPRS verification is bypassed in manual workflows.

---

## SECTION 7: TO-BE (ALIGNED WITH REALITY)

*The TO-BE state focuses on optimizing existing infrastructure rather than introducing hypothetical third-party apps.*

```mermaid
flowchart TD
    subgraph Source["Facility / Community"]
        Start_T((" ")) --> L1["Event Captured via CRS Notification App"]
    end

    subgraph Backend["CRVSS Core / Huduma Bridge"]
        L1 --> L2["Verify Identity via IPRS / Maisha"]
        L2 --> L3["Auto-Mint UPI for Births"]
        L3 --> L4["Digitally Sign Record (NPKI)"]
    end

    subgraph Finance_GPA["GPA Payment"]
        L4 --> M1["Process Fee & Revenue Split"]
    end

    subgraph Delivery["Civil Wallet / eCitizen"]
        M1 --> N1["Issue Verifiable Digital Credential"]
        N1 --> End_T(((" ")))
    end

    style Start_T fill:#fff,stroke:#27ae60,stroke-width:2px
    style End_T fill:#fff,stroke:#e74c3c,stroke-width:4px
```

*   **Primary Trigger:** Direct API integration between the **CRS Notification App** and hospital EMRs (where applicable).
*   **Identity Minting:** Automatic assignment of **Maisha Namba (UPI)** at the point of birth registration within CRVSS, linked to the IPRS master index.
*   **Verifiable Credentials:** Transition from paper certificates to **Digitally Signed Verifiable Credentials** stored in the eCitizen mobile wallet.
*   **NPKI Integration:** Every certificate issued will be digitally sealed using the **National Public Key Infrastructure (NPKI)** to prevent forgery.

---

## SECTION 8: DIGITIZATION STRATEGY (10M RECORDS)

To address the 10 million record backlog, a phased approach is mandated:
1.  **Phase 1: Metadata Indexing:** Scanning registers and capturing key indices (Name, Year, Entry No) to allow for digital searching.
2.  **Phase 2: On-Demand Full Digitization:** Full transcription of records when a citizen applies for a digital copy of a legacy manual certificate.
3.  **Phase 3: Back-File Conversion:** Systematic high-speed scanning and OCR processing of all remaining registers, starting from the most recent (last 10 years).
4.  **Cut-off Strategy:** As of a designated date, all manual registers are retired, and only CRVSS-generated entries are recognized as legal proof of status.

---

## SECTION 9: CHANGE LOG

| Area | Before (Incorrect/Old) | After (Corrected) | Reason |
| :--- | :--- | :--- | :--- |
| **Process Structure** | Merged Birth & Death | **Separated into two distinct tracks** | Legal and operational distinctness (Cap 149). |
| **System Trigger** | Afya App (MOH) | **CRS Notification App** | Ensures CRS maintains ownership and data integrity. |
| **Service Scope** | Basic Registration only | **Added Late, Foreign, Re-reg, Assumption** | Reflects the full statutory mandate of CRS. |
| **Flow Modeling** | Single mixed flow | **Dual (Manual vs CRVSS-enabled)** | Accurately describes the current hybrid reality. |
| **Identity Flow** | Generic Maisha Namba | **UPI/Maisha Namba via IPRS Link** | Technical accuracy of identity minting. |
| **Pain Points** | Generic "Slow services" | **10M Record Backlog & Registry Capacity** | Specific, measurable institutional challenges. |

---
**[End of Document]**
