# Directorate of Immigration Services (Passport Division) - Business Process Mapping

## 1. Overview
The Passport Division of the Directorate of Immigration Services is responsible for processing and issuing Kenyan passports, including first-time applications, renewals, and replacements.

| Attribute | Description |
| :--- | :--- |
| **Mapping Level** | Level 3 - Actor-based Logical Process |
| **Key Actors** | Applicants, Immigration Officers, Verification Officers, Production Unit |
| **Key Systems** | e-Citizen, IPRS, Passport Production System |
| **Digitisation Priority** | High |

---

## 2. Process Definitions

### Process 1: First-Time Passport Application
1. **Online Submission:** Application and document upload via e-Citizen.
2. **Identity Verification:** Real-time query against the IPRS database.
3. **Biometrics:** Physical visit for photo and fingerprint capture.
4. **Production:** Quality checks, queue management, and printing.

### Process 2: Passport Renewal
1. **Verification:** Checking eligibility based on existing passport records.
2. **Updates:** Updating biometric data and processing the new booklet.

### Process 3: Replacement (Lost/Mutilated)
1. **Reporting:** Processing police abstracts and verifying original records before re-issuance.

---

## 3. BPMN 2.0 Process Flows

### 3.1 First-Time Passport Application Lifecycle

```mermaid
flowchart TD
    Start((Start)) --> ECitizen[Access e-Citizen Portal]
    ECitizen --> Form[Complete Form & Upload Docs]
    Form --> Payment[Pay Processing Fee]
    
    Payment --> Validate[System Validation]
    Validate --> IPRS{Query IPRS: Verified?}
    
    IPRS -- No --> Flag[Flag for Manual Review]
    Flag --> VerifyManual[Officer Verification]
    VerifyManual --> Appointment
    
    IPRS -- Yes --> Appointment[Schedule Biometric Appointment]
    
    Appointment --> Visit[Visit Immigration Office]
    Visit --> Photo[Capture Digital Photo]
    Photo --> Fingerprints[Capture Fingerprints]
    
    Fingerprints --> Quality{Quality Check OK?}
    Quality -- No --> Photo
    
    Quality -- Yes --> Approval[Approval Queue]
    Approval --> Print[Print Passport]
    Print --> QualityVerify[Verify Print Quality]
    
    QualityVerify --> Notify[Notify Applicant for Collection]
    Notify --> Collection[Collect Passport & Verify Identity]
    Collection --> End((End))
```

### 3.2 Passport Renewal Process

```mermaid
flowchart TD
    RStart((Start)) --> RPortal[Access e-Citizen Renewal]
    RPortal --> RDetails[Enter Old Passport & Info]
    RDetails --> RPay[Pay Fee]
    
    RPay --> RCheck{Old Passport Valid?}
    RCheck -- No --> Reject[Reject & Refer to Replacement]
    Reject --> End((End))
    
    RCheck -- Yes --> RVisit[Visit Office for New Biometrics]
    RVisit --> RUpdate[Update Photo & Prints]
    
    RUpdate --> RQueue[Production Queue]
    RQueue --> RPrint[Print New Passport]
    
    RPrint --> RNotify[Notify for Collection]
    RNotify --> RIssue[Surrender Old & Issue New]
    RIssue --> End
```
