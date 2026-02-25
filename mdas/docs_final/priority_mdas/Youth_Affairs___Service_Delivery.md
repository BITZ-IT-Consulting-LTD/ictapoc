# STATE DEPARTMENT FOR YOUTH AFFAIRS – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Ministry of Public Service, Gender and Affirmative Action
- **Department:** State Department for Youth Affairs
- **Process Name:** Youth Internship Placement & AGPO Registration
- **Document Version:** 2.1
- **Date:** 2026-02-24
- **Classification:** Official

---

## Executive Summary
The State Department for Youth Affairs is responsible for the economic empowerment of Kenyan youth through initiatives like the Public Service Internship Programme (PSIP) and the Access to Government Procurement Opportunities (AGPO) registration for youth-owned enterprises. Currently, these processes rely on manual uploads of academic documents and business certificates. The transition to the Kenya DSAP Architecture aims to automate eligibility verification via IPRS and BRS, enabling instant internship matching and AGPO certification.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Youth Internship & AGPO Registration based on Deep Dive).*

```mermaid
graph TD
    Start((Start)) --> Access["Access eCitizen / Portal"]
    
    subgraph Internship [Youth Internship Placement]
        Access --> Form["Complete Form & Upload Documents"]
        Form --> Review["Officer Reviews Application"]
        Review --> Verify["Verify Eligibility (Academic/Age)"]
        Verify --> Eligible{"Eligible?"}
        
        Eligible -- "Yes" --> Search["Search & Match Skills to Opportunities"]
        Search --> Issue["Issue Letter & Notify Host"]
        Eligible -- "No" --> Reject["Notify Rejection"]
    end
    
    subgraph AGPO [AGPO Registration]
        Access --> AGPO_Form["Complete AGPO Form"]
        AGPO_Form --> Attach["Attach Business & ID Documents"]
        Attach --> Vetting["Manual Vetting: Verify Ownership & Age (18-35)"]
        Vetting --> Appr{"Approve?"}
        
        Appr -- "Yes" --> Cert["Generate Certificate & Update Registry"]
        Appr -- "No" --> Rej_AGPO["Reject Application"]
    end
    
    Issue --> End((End))
    Cert --> End
    Reject --> End
    Rej_AGPO --> End

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333;
    class Start start;
    class End endNode;
    class Eligible,Appr gateway;
    class Access,Form,Review,Verify,Search,Issue,Reject,AGPO_Form,Attach,Vetting,Cert,Rej_AGPO userTask;
```

---

## Process Overview
### Process Name
Youth Internship Placement, AGPO Registration, and Film Production Licensing

### Service Category
- G2C (Government to Citizen) / G2B (Youth-owned MSMEs)

### Scope
- **In Scope:** Internship applications, skill matching, AGPO certification for youth, and film licensing.
- **Out of Scope:** Disbursement of enterprise funds (handled by MSME department).

### Triggers
- A youth applying for an internship or a youth-owned business seeking AGPO certification.

### End States
- **Successful:** Internship placement letter issued; AGPO Certificate generated.

### Policy Context
- The Public Service Commission Internship Policy; The Public Procurement and Asset Disposal Act (AGPO Provisions).

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Applicant | Logs into eCitizen and fills forms for Internship or AGPO. | eCitizen / Portal | |
| 2 | Applicant | Uploads PDF copies of National ID, Academic Certificates, and BRS Business Registrations. | Manual Upload | |
| 3 | Youth Officer | Manually reviews the documents to ensure the applicant is between 18-35 years old. | Manual | High duplication of effort. |
| 4 | Programme Officer | For internships, manually matches the applicant's course of study with available slots in government agencies. | Excel / Manual | |
| 5 | AGPO Officer | Verifies business ownership details against BRS certificates before approving the AGPO status. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- **Document Fatigue:** Youth have to upload the same ID and certificates for every application.
- **Inefficient Matching:** Manual matching of 50,000+ interns to 1,000+ slots is slow and error-prone.
- **Vetting Delays:** AGPO certification takes weeks due to manual business ownership verification.

### Opportunities
- **Once-Only Data Pull:** Fetching ID from **IPRS**, Academic data from **KNEC/KNQA**, and Business data from **BRS** via **X-Road**.
- **AI-Powered Matching:** An automated engine that matches interns to hosts based on GPS location and skill sets.
- **Real-Time AGPO Certification:** Instantly issuing AGPO certificates once the system confirms the directors are 18-35 via IPRS.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Kenya DSAP Architecture - Huduma Bridge).*

```mermaid
graph TD
    Start((Start)) --> Portal["Youth Applicant Logs in via Maisha Namba"]
    
    subgraph Layer2 [Identity & Trust Hub]
        Portal --> Consent["Consent Manager: Access ID, Education & BRS data?"]
        Consent --> XRoad["X-Road: Auto-fetch profile from IPRS, KNQA, BRS"]
    end
    
    subgraph Layer3 [Operations - Workflow Engine]
        XRoad --> Type{"Service Type?"}
        
        Type -- "Internship" --> Match["AI Engine: Instant Skill & Location Match"]
        Type -- "AGPO" --> Vetting["Automated Ownership & Age Validation"]
    end
    
    subgraph Layer4 [Issuance & Settlement]
        Match --> Letter["Generate Digital Placement Letter (QR)"]
        Vetting --> Cert["Generate Verifiable AGPO Certificate"]
    end
    
    Letter --> End((End))
    Cert --> End

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333;
    class Start start;
    class End endNode;
    class Type gateway;
    class Portal,Consent userTask;
    class XRoad,Match,Vetting,Letter,Cert serviceTask;
```

## Future State Process (TO-BE)
### Narrative
**TO-BE Process: Automated Youth Empowerment**

**Design Principles:**
- **Zero Document Uploads:** Academic credentials and business ownership details are fetched directly from authoritative registries via the **Huduma Bridge**.
- **Instant AGPO:** If the system confirms (via BRS and IPRS) that a business is 100% youth-owned, the AGPO certificate is issued instantly.
- **Smart Internships:** The **Workflow Engine** uses AI to place interns in agencies nearest to their residence (verified via GPS/Maisha Namba), reducing transport costs for the youth.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Youth Applicant | Logs into eCitizen using Maisha Namba. All personal and education details are already pre-populated. | eCitizen / SSO |
| 2 | System | For AGPO, the system pings BRS via X-Road to verify the company's "Youth-Owned" status. | KeSEL / X-Road |
| 3 | System | AI matching engine assigns the intern to a government agency based on the applicant's degree and the agency's needs. | Workflow Engine |
| 4 | System | Generates a digital verifiable certificate/letter with a secure QR code for instant authentication. | Output Generator |

---

## References
- Public Service Commission Internship Policy.
- Huduma Bridge DSAP Architecture.