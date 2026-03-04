# CIVIL REGISTRATION SERVICES (CRS) – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Ministry of Interior and National Administration
- **Department:** Department of Civil Registration Services (CRS)
- **Process Name:** Birth and Death Registration
- **Document Version:** 2.1
- **Date:** 2026-02-24
- **Classification:** Official

---

## Executive Summary
Civil Registration Services (CRS) is the authoritative custodian of vital life events in Kenya, including births and deaths. These events form the bedrock of a citizen's legal identity (Maisha Namba). The current process relies on semi-digital systems (CRVS) and manual paper notifications from hospitals and administrative chiefs. The transition to the Kenya DSAP Architecture aims to establish real-time, event-driven registration triggered at the point of occurrence.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Birth & Death Registration based on Deep Dive).*

```mermaid
graph TD
    Start((Start)) --> Source{"Event Source?"}
    
    subgraph Capture [Point of Occurrence]
        Source -- "Hospital" --> Notification["Hospital Notification / Medical Cert"]
        Source -- "Home" --> Community["Community Report (Chief/Informant)"]
        Notification --> Form["Complete Form (Birth/Death)"]
        Community --> Form
    end
    
    subgraph Vetting [Verification & Approval]
        Form --> Attach["Attach Parent IDs / Marriage Cert / Evidence"]
        Attach --> Review["Officer Reviews Documents"]
        Review --> Verify["Verify Parents / Cause of Death"]
        Verify --> Complete{"Is Data Complete?"}
        
        Complete -- "No" --> MoreInfo["Request More Info/Docs"]
        MoreInfo --> Form
        
        Complete -- "Yes" --> Register["Enter in Register & Assign Entry Number"]
    end
    
    subgraph Issuance [Payment & Production]
        Register --> Sign["Registrar Signs Record"]
        Sign --> Payment["Process Payment (Manual/eCitizen)"]
        Payment --> Print["Print Certificate / Burial Permit"]
        Print --> Issue["Issue Certificate to Informant"]
    end
    
    Issue --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333;
    class Start start;
    class End endNode;
    class Source,Complete gateway;
    class Notification,Community,Form,Attach,Review,Verify,MoreInfo,Register,Sign,Payment,Print,Issue userTask;
```

---

## Process Overview
### Process Name
Vital Event Registration (Births and Deaths) and Certificate Issuance

### Service Category
- G2C (Government to Citizen)

### Scope
- **In Scope:** Timely and late registration of births and deaths; issuance of birth certificates, death certificates, and burial permits.
- **Out of Scope:** Issuance of National ID cards (handled by NRB).

### Triggers
- Occurrence of a birth or death at a facility or within the community.

### End States
- **Successful:** Vital event registered; Digital record created; Physical/Digital certificate issued.

### Policy Context
- Births and Deaths Registration Act; The Constitution of Kenya; Data Protection Act 2019.

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Informant/Chief | Reports the event at a CRS office or via the eCitizen portal. | Manual/Digital | |
| 2 | Registration Officer | Verifies the supporting documents (ID of parents, notification from hospital). | Manual | |
| 3 | Registration Officer | Manually enters the data into the CRVS system and assigns a serial entry number. | CRVS System | |
| 4 | Registrar | Approves the entry and signs the physical register or digital record. | Physical Register | |
| 5 | Clerk | Processes the payment and triggers the printing of the certificate. | Manual/eCitizen | |

---

## Pain Points & Opportunities
### Pain Points
- **Manual Backlogs:** Physical registers in district offices lead to delays in searching and retrieving records.
- **Identity Fraud:** Difficulty in verifying the identity of parents or informants against IPRS in real-time.
- **Late Registration:** Complexities in "Late Registration" (after 6 months) discourage citizens from formalizing vital events.

### Opportunities
- **Event-Driven Architecture:** Automatic registration triggered when a birth is logged in the MOH **Afya App**.
- **Unified Identity (Maisha Namba):** Instant generation of a Unique Personal Identifier (UPI) upon birth registration.
- **Digital Certificates:** Issuing cryptographically signed digital certificates directly to the citizen's mobile wallet.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Kenya DSAP Architecture - Huduma Bridge).*

```mermaid
graph TD
    Start((Start)) --> Event["Birth/Death Occurs at Facility"]
    
    subgraph Layer1 [Access - Point of Care]
        Event --> MOH["MOH System Logs Event (Afya App)"]
    end
    
    subgraph Layer3 [Huduma Bridge / X-Road]
        MOH --> XRoad["X-Road: Secure Push to CRS Database"]
        XRoad --> IPRS["X-Road: Verify Parent/Deceased via IPRS"]
    end
    
    subgraph Layer4 [Authoritative Registry]
        IPRS --> Mint["CRS: Auto-Mint Maisha Namba / Update Status"]
        Mint --> Vault["Store in Secure Vital Events Vault"]
    end
    
    subgraph Output [Digital Issuance]
        Vault --> Notify["Notify Parents/Kin via eCitizen App"]
        Notify --> Wallet["Issue Verifiable Digital Certificate to Wallet"]
    end
    
    Wallet --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;
    class Start start;
    class End endNode;
    class Event,MOH userTask;
    class XRoad,IPRS,Mint,Vault,Notify,Wallet serviceTask;
```

## Future State Process (TO-BE)
### Narrative
**TO-BE Process: Seamless Vital Event Registration**

**Design Principles:**
- **Zero-Touch Registration:** When a child is born in an accredited hospital, the **MOH system** pushes the record to **CRS** via the **Huduma Bridge**. The registration happens in the background without the parents needing to apply.
- **Instant Identity:** The system automatically pings **IPRS** to verify the parents' identities and then mints a **Maisha Namba (UPI)** for the child instantly.
- **Digital First:** Paper certificates are replaced by **Verifiable Digital Credentials** issued to the parents' eCitizen wallets, which can be presented at schools or for passport applications without needing a physical copy.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Health Worker | Records the birth/death in the facility EMR. | MOH Afya App |
| 2 | System | Automatically verifies the parents' IDs against Maisha Namba via X-Road. | IPRS / KeSEL |
| 3 | CRS Registry | Receives the validated packet and mints a UPI (Maisha Namba) for the child. | CRS / Workflow Engine |
| 4 | System | Notifies the parents/kin via SMS/eCitizen that the registration is complete. | Notification Gateway |
| 5 | Citizen | Accesses the verifiable digital certificate via their mobile phone for use in other government services. | Digital Wallet |

---

## References
- https://www.immigration.go.ke
- Births and Deaths Registration Act
- Desk Review
