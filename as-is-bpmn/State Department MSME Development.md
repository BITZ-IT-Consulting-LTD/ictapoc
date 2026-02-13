# State Department for MSME Development - Business Process Mapping

## 1. Overview
The State Department promotes the growth of micro, small, and medium enterprises through credit access (e.g., Hustler Fund, Uwezo Fund), capacity building, and market linkages.

| Attribute | Description |
| :--- | :--- |
| **Mapping Level** | Level 3 - Actor-based Logical Process |
| **Key Actors** | MSME Applicants, Fund Officers, Credit Committees |
| **Key Systems** | Hustler Fund Portal, Uwezo Fund System, IFMIS |
| **Digitisation Priority** | High |

---

## 2. Process Definitions

### Process 1: Hustler Fund (Digital Credit)
1. **Application:** Registration on the platform, automated eligibility verification, and instant disbursement.
2. **Repayment:** Automated tracking of repayments and credit history updates.

### Process 2: Uwezo Fund (Group Loans)
1. **Group Registration:** Verification of group composition and registration approval.
2. **Loan Application:** Eligibility checks, project proposal assessment, and credit committee review.

---

## 3. BPMN 2.0 Process Flows

### 3.1 MSME Credit Access Flow

```mermaid
flowchart TD
    Start((Start)) --> Register[Register on Platform]
    Register --> Verify[Verify Identity & Eligibility]
    
    Verify --> Eligible{Eligible?}
    Eligible -- No --> End((End))
    
    Eligible -- Yes --> Apply[Complete Application]
    Apply --> Submit[Submit Documents]
    
    Submit --> Appraisal[Credit Appraisal]
    Appraisal --> Approval{Approved?}
    
    Approval -- No --> NotifyReject[Notify Applicant]
    NotifyReject --> End
    
    Approval -- Yes --> Sign[Sign Digital Agreement]
    Sign --> Disburse[Disburse Funds]
    
    Disburse --> Monitoring[Track Repayment & Utilization]
    Monitoring --> History[Update Credit History]
    History --> End
```

### 3.2 Uwezo Fund - Group Loan Process

```mermaid
flowchart TD
    GStart((Start)) --> GroupReg[Register Group & Verify Members]
    GroupReg --> ApproveGroup[Approve Group Registration]
    
    ApproveGroup --> LoanReq[Submit Loan Request & Proposal]
    LoanReq --> Review[Review Application & Assess Proposal]
    
    Review --> Committee{Credit Committee}
    Committee -- Reject --> GEnd((End))
    
    Committee -- Approve --> Sign[Sign Agreement]
    Sign --> Disburse[Disburse to Group Account]
    
    Disburse --> Monitor[Track Utilization & Repayment]
    Monitor --> GEnd
```
