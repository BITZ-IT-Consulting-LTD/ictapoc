# OFFICE OF THE ATTORNEY GENERAL (AG) – Marriages & Divorces

## Cover Page
- **Ministry/Department/Agency (MDA):** OFFICE OF THE ATTORNEY GENERAL (AG) - REGISTRAR OF MARRIAGES
- **Process Name:** Civil Marriages & Divorces Registry
- **Document Version:** 2.0
- **Date:** 2026-03-17
- **Classification:** Official

---

## Executive Summary
The Office of the Attorney General (through the Registrar of Marriages) is mandated to register, solemnize, and maintain records of statutory marriages in Kenya. This includes processing notices of marriage, issuing certificates, conducting civil weddings, and updating the registry following court-ordered divorce decrees. The department plays a critical role in providing secure vital life-event records and family status documentation for citizens.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Manual/Semi-Automated Marriage & Divorce Processing).*

```mermaid
graph TD
    Start((Start)) --> S1

    subgraph Citizen [Citizen]
        S1["Citizen creates eCitizen account & selects Marriage Service"] --> S2
        S2["Applicant fills online Notice of Marriage form & uploads documents (IDs, Photos)"] --> S3
        S3["Applicant pays statutory fee via eCitizen (e.g., KES 600)"] --> S4
        S4["Applicant prints system-generated Notice and books appointment"] --> S5
        S5["Citizen visits Sheria House / Registrar physically for document verification"] --> S14
        
        S20["Citizen receives Divorce Decree Absolute from High Court"] --> S21
        S21["Citizen physically submits Decree to Registrar to update marital status"] --> S22
    end

    subgraph Registrar_of_Marriages [Registrar of Marriages / AG]
        S6["Registrar verifies physical IDs and uploaded documents"] --> S7
        S7["Notice is pinned on the physical Notice Board for 21 days"] --> S8
        S8{"Any Objections raised during 21 days?"}
        
        S8 -- Yes --> S9["Hearing scheduled to resolve objection"]
        S9 --> S10{"Objection Valid?"}
        S10 -- Yes --> S11["Application Rejected / Terminated"]
        S10 -- No --> S12["Proceed to next step"]
        
        S8 -- No --> S12
        
        S12["Registrar issues Registrar's Certificate"] --> S13
        S13["Couple books date for solemnization/wedding at Sheria House"] --> S14
        
        S14["Ceremony conducted by Registrar"] --> S15
        S15["Physical Marriage Register signed by couple & witnesses"] --> S16
        S16["Registrar prints and issues physical Marriage Certificate"]
        
        S22["Registrar manually updates physical registry to reflect divorce"] --> S23
        S23["Registrar issues certified copy of search/update if requested"]
    end
    
    S11 --> End((End))
    S16 --> End
    S23 --> End
```

---

## 2. Weaknesses & Pain Points (The "Why")
- **Manual Physical Presence Required:** Even though eCitizen handles the payment and initial application, couples must physically visit the registry for document verification and the ceremony, creating long queues.
- **Physical Notice Boards:** Relying on physical pin-boards for the 21-day statutory notice is outdated and fails to provide national visibility for objections.
- **Disconnected Divorce Updates:** The Judiciary handles divorces, but there is no automated API linking the High Court's Case Management System to the AG's Marriage Registry. Divorced individuals must manually carry court decrees to update their status.
- **Paper Registers:** The final legal artifact is still a physical signature in a large paper register book, making historical searches and certificate replacements very slow.

---

## 3. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Fully Digitized with Identity Federation).*

```mermaid
graph TD
    Start((Start)) --> S1

    subgraph Citizen [Citizen]
        S1["Citizen logs in via Maisha Namba / eCitizen"] --> S2
        S2["Initiates Marriage Notice (System auto-pulls both partners' details from NRB)"] --> S3
        S3["Completes biometric/facial liveness check for consent"] --> S4
        S4["Pays consolidated fee digitally"]
        
        S12["Couple attends Virtual or Physical Solemnization"] --> S13
        S13["Couple signs digitally via secure portal/biometrics"]
    end

    subgraph Platform_Services [Shared Platform / Integrations]
        S4 --> S5["Payment Gateway processes and splits funds"]
        S5 --> S6["Integration Engine checks marital status in Registry (Prevents Bigamy)"]
        S6 --> S7["Digital Notice published on National e-Gazette/Portal for 21 days"]
        
        S14["Digital e-Certificate generated with QR Code"] --> S15
        S15["National Marriages Registry Database Updated"]
        
        S20["Judiciary API automatically sends Divorce Decree to Registry"] --> S21
        S21["Marital status automatically updated to 'Divorced' in Registry"]
    end

    subgraph Registrar_of_Marriages [Registrar of Marriages / AG]
        S7 --> S8{"Digital Objections raised?"}
        S8 -- Yes --> S9["Online Tribunal/Hearing scheduled"]
        S9 --> S10{"Objection Valid?"}
        S10 -- Yes --> S11["Application Terminated"]
        S10 -- No --> S12
        
        S8 -- No --> S12
    end
    
    S11 --> End((End))
    S15 --> End
    S21 --> End
```

---

## 4. Automation & Digitization Opportunities (The "How")
- **National Population Register (NRB) Integration:** Auto-populate partner details to prevent identity fraud and automatically flag if a partner is already legally married in the system (preventing bigamy).
- **Digital Notice Board (e-Gazette):** Replace physical pin-boards with a centralized, searchable online portal where citizens can view notices and lodge objections digitally.
- **Judiciary API (Divorce decrees):** Establish a system-to-system integration with the Judiciary so that when a divorce is finalized in court, the AG's marriage registry is instantly updated without the citizen needing to act as a courier.
- **E-Certificates:** Issue digitally signed, QR-coded marriage certificates that can be instantly verified by embassies, banks, and other MDAs.

---

## 5. Required Integrations
- **NRB / IPRS:** For citizen identity verification and liveness checks.
- **Judiciary Case Management System (CMS):** To automatically receive and process absolute divorce decrees.
- **eCitizen / PayPay:** For payment processing.
- **Government e-Gazette:** For publishing 21-day marriage notices electronically.
