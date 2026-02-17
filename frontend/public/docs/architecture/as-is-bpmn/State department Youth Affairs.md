# State Department for Youth Affairs and Creative Economy - Business Process Mapping

## 1. Overview
The State Department for Youth Affairs and Creative Economy is responsible for youth development, employment facilitation (e.g., NYOTA Apprenticeship), and the promotion of Kenya's creative industries, including film licensing and AGPO registration.

| Attribute | Description |
| :--- | :--- |
| **Mapping Level** | Level 3 - Actor-based Logical Process |
| **Key Actors** | Youth Applicants, Programme Officers, NYOTA Coordinators, Film Officers |
| **Key Systems** | e-Citizen, IFMIS, NYOTA Portal |
| **Digitisation Priority** | High |

---

## 2. Process Definitions

### Process 1: Youth Employment Facilitation
1. **Internship Placement:** Receive applications, verify eligibility, and match candidates to host opportunities.
2. **NYOTA Apprenticeship:** Portal registration, skills assessment, matching with master craftspersons, and certification.

### Process 2: Creative Economy Support
1. **Film Licensing:** Reviewing production requirements and coordinating with the Film Commission to issue permits.

### Process 3: AGPO Registration
1. **Youth Enterprise Registration:** Verifying ownership and age (18-35) to issue AGPO certificates for government procurement.

---

## 3. BPMN 2.0 Process Flows

### 3.1 Youth Employment & Internship Flow

```mermaid
flowchart TD
    Start((Start)) --> Apply[Submit Application]
    Apply --> Attach[Attach Documents]
    Attach --> Eligibility{Eligible?}
    
    Eligibility -- No --> NotifyReject[Notify Rejection]
    NotifyReject --> End((End))
    
    Eligibility -- Yes --> Match[Match Skills to Opportunities]
    Match --> IssueLetter[Issue Placement Letter]
    IssueLetter --> NotifyHost[Notify Host Organization]
    
    NotifyHost --> Reports[Youth Reports & Progress Tracking]
    Reports --> Feedback[Collect Feedback]
    Feedback --> Certificate[Issue Completion Certificate]
    Certificate --> End
```

### 3.2 NYOTA Apprenticeship Lifecycle

```mermaid
flowchart TD
    Start((Start)) --> Access[Access NYOTA Portal]
    Access --> Account[Create Account & Upload Docs]
    Account --> Review[Review Application & Assess Skills]
    
    Review --> Matching[Match Apprentice with Master]
    Matching --> Agreement[Sign Training Agreement]
    
    Agreement --> Training[Start Training & Track Progress]
    Training --> Periodical[Assess Periodically]
    
    Periodical --> Final[Final Assessment]
    Final --> IssueCert[Issue Certificate]
    IssueCert --> Update[Update Registry]
    Update --> End((End))
```

### 3.3 AGPO Registration

```mermaid
flowchart TD
    Start((Start)) --> Form[Complete Form & Attach ID/Reg]
    Form --> Review[Review Docs]
    Review --> Verify{Ownership & Age 18-35?}
    
    Verify -- No --> Reject[Reject Application]
    Reject --> End((End))
    
    Verify -- Yes --> Approve[Approve Registration]
    Approve --> Generate[Generate AGPO Certificate]
    Generate --> Notify[Notify Applicant]
    Notify --> Issue[Issue Certificate & Update Registry]
    Issue --> End
```
