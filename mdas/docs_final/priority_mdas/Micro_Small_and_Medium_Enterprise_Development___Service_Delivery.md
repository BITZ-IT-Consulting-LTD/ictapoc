# STATE DEPARTMENT FOR MSME DEVELOPMENT – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Ministry of Co-operatives and MSMEs
- **Department:** State Department for MSME Development
- **Process Name:** MSME Credit, Fund Management & Apprenticeship
- **Document Version:** 2.1
- **Date:** 2026-02-24
- **Classification:** Official

---

## Executive Summary
The State Department for MSME Development is mandated to support the growth of small businesses through access to affordable credit (Hustler Fund, Uwezo Fund), capacity building, and apprenticeships (NYOTA). While the Hustler Fund is highly digitized, other funds like Uwezo still rely on manual group registrations and physical bank accounts. The transition to the Kenya DSAP Architecture aims to unify all MSME support into a single digital ecosystem integrated with BRS and the national identity system.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Hustler Fund & Uwezo Fund based on Deep Dive).*

```mermaid
graph TD
    Start((Start)) --> Access["Access Portal / Mobile App"]
    
    subgraph Individual_Credit [Hustler Fund Application]
        Access --> KYC["Complete KYC & Register Account"]
        KYC --> VerifyID["Verify National ID (IPRS Lookup)"]
        VerifyID --> CreditScore["Check Credit Score (Internal/CRB)"]
        CreditScore --> Eligible{"Eligible?"}
        
        Eligible -- "Yes" --> Terms["Calculate Terms & Disburse to Mobile Money"]
        Eligible -- "No" --> Review["Flag for Manual Review / Reject"]
    end
    
    subgraph Group_Credit [Uwezo Fund Loan]
        Access --> Form_Group["Form Group (10-15 Members) & Elect Officials"]
        Form_Group --> Bank["Open Group Bank Account"]
        Bank --> Reg_Form["Complete Registration & Attach Member IDs/Constitution"]
        Reg_Form --> SubCounty["Submit to Sub-County for Verification"]
        SubCounty --> Approved{"Approved?"}
        
        Approved -- "Yes" --> Cert["Issue Certificate & Disburse Loan"]
        Approved -- "No" --> Corrections["Return for Corrections"]
    end
    
    Terms --> End((End))
    Cert --> End
    Review --> End

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333;
    class Start start;
    class End endNode;
    class Eligible,Approved gateway;
    class Access,KYC,VerifyID,CreditScore,Terms,Review,Form_Group,Bank,Reg_Form,SubCounty,Cert,Corrections userTask;
```

---

## Process Overview
### Process Name
MSME Credit Access (Hustler/Uwezo), Repayment, and NYOTA Apprenticeship

### Service Category
- G2C (Government to Citizen) / G2B (Government to Business)

### Scope
- **In Scope:** Application, KYC verification, credit scoring, disbursement, and tracking of repayments.
- **Out of Scope:** Commercial bank lending outside government-sponsored funds.

### Triggers
- Citizen/MSME applying for credit or an apprenticeship opportunity.

### End States
- **Successful:** Credit disbursed; Apprenticeship matched; Credit history updated.

### Policy Context
- The Micro and Small Enterprises Act; Public Finance Management (Hustler Fund) Regulations.

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Applicant | Accesses the fund portal (USSD/Web) and registers using their National ID. | USSD / Web Portal | |
| 2 | System | Performs KYC by querying IPRS to verify identity and age eligibility. | IPRS API | |
| 3 | System | Checks internal credit history and external CRB scores to determine the loan limit. | Credit Engine | |
| 4 | Applicant | For Uwezo/NYOTA, attaches scanned copies of business registrations or ID documents. | Manual Upload | |
| 5 | Fund Officer | For group loans, verifies group composition and bank details manually at the Sub-County level. | Standalone System | |

---

## Pain Points & Opportunities
### Pain Points
- **Fragmented Portals:** Hustler, Uwezo, and Women Enterprise Fund (WEF) have different entry points and rules.
- **Manual Group Registration:** Opening physical bank accounts and submitting paper constitutions for Uwezo is a significant barrier.
- **Limited Business Data:** Reliance on ID data alone; lack of integration with BRS for business performance metrics.

### Opportunities
- **Unified MSME Portal:** A single "eCitizen for Business" entry point for all government credit and support programs.
- **Digital Group Wallets:** Replacing physical bank accounts for groups with digital wallets integrated into the **Government Payment Aggregator**.
- **Alternative Credit Scoring:** Using BRS data and transaction history from the **GPA** to provide better credit limits.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Kenya DSAP Architecture - Huduma Bridge).*

```mermaid
graph TD
    Start((Start)) --> Portal["Applicant Accesses Unified MSME Portal (SSO)"]
    
    subgraph Layer2 [Workflow & Identity]
        Portal --> Verify["X-Road: Validate Identity & Business (BRS)"]
        Verify --> Score["AI Credit Engine: Score based on GPA & BRS Data"]
    end
    
    subgraph Layer3 [Huduma Bridge / X-Road]
        Score --> GroupCheck["X-Road: Auto-verify Group Members via IPRS"]
    end
    
    subgraph Layer4 [Payments & Disbursement]
        GroupCheck --> Wallet["System Creates Digital Group Wallet (GPA)"]
        Wallet --> Disburse["Instant Disbursement via Payment Aggregator"]
    end
    
    subgraph Monitoring [Impact Tracking]
        Disburse --> Track["Real-time Repayment & Performance Tracking"]
        Track --> History["Auto-update National Credit Registry"]
    end
    
    History --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;
    class Start start;
    class End endNode;
    class Portal userTask;
    class Verify,Score,GroupCheck,Wallet,Disburse,Track,History serviceTask;
```

## Future State Process (TO-BE)
### Narrative
**TO-BE Process: Integrated Digital MSME Ecosystem**

**Design Principles:**
- **Unified Entry:** A single-window portal (integrated with eCitizen) for all MSME funds, reducing confusion.
- **Automated Trust:** Using **X-Road** to verify business ownership via **BRS** and group member identities via **IPRS**, removing the need for manual document uploads.
- **Instant Inclusion:** Replacing physical bank accounts with **GPA-linked Digital Wallets**, allowing for instant disbursement and automated split-repayments (e.g., a portion of daily sales goes back to the loan).

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Applicant | Logs in via eCitizen SSO and selects the appropriate MSME fund or support program. | Unified MSME Portal |
| 2 | System | Fetches business history from BRS and tax compliance from KRA via X-Road to assess eligibility. | KeSEL / X-Road |
| 3 | System | For group applications, the system pings the members' phones for digital consent and verifies their "Maisha Namba" status. | Consent Manager |
| 4 | System | Instantly disburses the loan to a digital wallet managed by the Government Payment Aggregator. | GPA / Mobile Money |
| 5 | System | Monitors sales and transactions via the GPA to provide real-time credit score updates and nudge for repayments. | Analytics Engine |

---

## References
- The Micro and Small Enterprises Act.
- Huduma Bridge DSAP Architecture.