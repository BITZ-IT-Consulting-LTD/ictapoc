# State Department Civil Registration Services - Business Process Mapping

## 1. Overview
The Department of Civil Registration Services registers vital events including births, deaths, and marriages and maintains the national civil registry for Kenya.

| Attribute | Description |
| :--- | :--- |
| **Mapping Level** | Level 3 - Actor-based Logical Process |
| **Key Actors** | Parents, Informants, Registration Officers, Medical Officers, Chiefs |
| **Key Systems** | CRVS, e-Citizen |
| **Digitisation Priority** | High |

---

## 2. Process Definitions

### Process 1: Birth Registration
1. **Timely Registration:** Receive birth notification from hospital or home, verify details, capture in the register, and issue a certificate.
2. **Late Registration:** Processing applications for events that occurred over 6 months ago, requiring adjudication and additional evidence.

### Process 2: Death Registration
1. **Facility/Community Deaths:** Verify cause of death or chief's report, process registration, and issue burial permits and certificates.

### Process 3: Certificate Services
1. **Retrieval:** Search registry based on request details, verify entitlement, and issue a duplicate or new certificate.

---

## 3. BPMN 2.0 Process Flows

### 3.1 Birth Registration Flow

```mermaid
flowchart TD
    Start((Start)) --> Source{Where?}
    Source -- Hospital --> HospitalNotify[Hospital Notification]
    Source -- Home --> HomeNotify[Notification Form]
    
    HospitalNotify & HomeNotify --> Complete[Complete Form]
    Complete --> Attach[Attach Parent IDs & Marriage Cert]
    Attach --> Submit[Submit to Office]
    
    Submit --> Review{Complete & Verified?}
    Review -- No --> RequestMore[Request Missing Info]
    RequestMore --> Complete
    
    Review -- Yes --> Register[Enter in Registry]
    Register --> Entry[Assign Entry Number]
    Entry --> Payment[Process Payment]
    Payment --> Signing[Registrar Signs]
    Signing --> Print[Print Certificate]
    Print --> Issue[Issue to Applicant]
    Issue --> End((End))
```

### 3.2 Death Registration

```mermaid
flowchart TD
    DStart((Start)) --> Location{Location?}
    Location -- Hospital --> MedCert[Medical Certificate]
    Location -- Home --> ChiefReport[Chief Report]
    
    MedCert & ChiefReport --> DComplete[Complete Form]
    DComplete --> DAttach[Attach ID of Deceased & Informant]
    DAttach --> DSubmit[Submit]
    
    DSubmit --> DReview{Verified?}
    DReview -- No --> DReject[Request More Info]
    DReject --> DComplete
    
    DReview -- Yes --> DRegister[Enter in Register]
    DRegister --> DBurial[Issue Burial Permit]
    DBurial --> DSign[Registrar Signs]
    DSign --> DPrint[Issue Death Certificate]
    DPrint --> DEnd((End))
```

### 3.3 Certificate Retrieval

```mermaid
flowchart TD
    RStart((Start)) --> RRequest[Submit Request & Pay Fee]
    RRequest --> Search[Search Registry]
    
    Search --> Found{Found?}
    Found -- No --> Notify[Notify Not Found]
    Notify --> REnd((End))
    
    Found -- Yes --> Entitled{Entitled?}
    Entitled -- No --> Reject[Reject Request]
    Reject --> REnd
    
    Entitled -- Yes --> Quality[Quality Check]
    Quality --> RPrint[Print & Issue Certificate]
    RPrint --> REnd
```
