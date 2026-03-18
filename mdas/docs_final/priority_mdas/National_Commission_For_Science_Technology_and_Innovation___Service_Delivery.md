# NATIONAL COMMISSION FOR SCIENCE, TECHNOLOGY AND INNOVATION (NACOSTI) – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Ministry of Education
- **Authority:** National Commission for Science, Technology and Innovation (NACOSTI)
- **Process Name:** Research Licensing and Knowledge Management
- **Document Version:** 2.1
- **Date:** 2026-02-24
- **Classification:** Official
- **Strategic Category:** Priority MDA
- **Service Model:** G2B
- **Life-Cycle Group:** Cradle to Death (4. Employment & Business)

---

## Executive Summary
NACOSTI is the primary agency responsible for regulating and assuring quality in the science, technology, and innovation sector. Its key mandate is to license all research activities in Kenya. The current process involves manual document vetting, physical bank payments, and sequential expert reviews. The transition to the Kenya DSAP Architecture aims to establish an automated research portal integrated with KNQA for researcher verification and the Government Payment Aggregator for instant licensing.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (End-to-End Research Licensing based on Deep Dive).*

```mermaid
%%{init: { 'theme': 'base', 'themeVariables': { 'fontSize': '24px', 'fontFamily': 'Inter, system-ui, sans-serif', 'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#f3f3f3', 'mainBkg': '#ffffff', 'nodeBorder': '#333333' } } }%%
graph TD
    Start((Start)) --> Submit["Complete Application & Attach Research Proposal"]
    
    subgraph Intake["Reception & Acknowledgment"]
        Submit --> Comp{"Complete?"}
        Comp -- "No" --> Return["Return for Completion"]
        Return --> Submit
        
        Comp -- "Yes" --> Log["Log in Register & Assign Reference"]
        Log --> Acknowledge["Issue Acknowledgment Letter"]
    end
    
    subgraph Vetting["Technical Review"]
        Acknowledge --> Identify["Identify Subject-Matter Examiner"]
        Identify --> Assess["Assess Research Criteria & Ethical Compliance"]
        Assess --> Verify["Verify Qualifications & Institution"]
        Verify --> Report["Prepare Vetting Report"]
    end
    
    subgraph Approval["Payment & Licensing"]
        Report --> Recommend{"Recommendation?"}
        
        Recommend -- "Revise" --> ReqRev["Request Revision from Researcher"]
        ReqRev --> Submit
        
        Recommend -- "Approve" --> PayReq["Calculate Fees & Issue Payment Request"]
        PayReq --> ResearcherPay["Researcher Pays via Bank & Submits Receipt"]
        
        ResearcherPay --> VerifyPay["Verify Bank Receipt & Issue Official Receipt"]
        VerifyPay --> GenLicense["Generate Research License & Notify Applicant"]
    end
    
    GenLicense --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff,font-size:24px,font-size:24px;;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff,font-size:24px,font-size:24px;;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff,font-size:24px,font-size:24px;;
    classDef gateway fill:#f1c40f,stroke:#f39c12,color:#333,font-size:24px,font-size:24px;;
    class Start start;
    class End endNode;
    class Comp,Recommend gateway;
    class Submit,Return,Log,Acknowledge,Identify,Assess,Verify,Report,ReqRev,PayReq,ResearcherPay,VerifyPay,GenLicense userTask;
```

---

## Process Overview
### Process Name
End-to-End Research Application, Vetting, and Licensing

### Service Category
- G2C (Researchers) / G2B (Institutions)

### Scope
- **In Scope:** Application for research permits, ethical clearance vetting, fee processing, and issuance of licenses.
- **Out of Scope:** Actual funding of research projects.

### Triggers
- A researcher (local or foreign) applying for a permit to conduct a study in Kenya.

### End States
- **Successful:** Research License issued; Study metadata logged in the national repository.

### Policy Context
- Science, Technology and Innovation Act 2013; Data Protection Act 2019.

---

## Detailed Process (AS-IS)

| Step | Role | Action | Tool/System | Notes |
|---|---|---|---|---|
| 1 | Researcher | Submits research proposal, ethical clearance, and academic certificates. | Manual/Portal | |
| 2 | NACOSTI Officer | Manually checks if all documents are attached and assigns a physical file reference. | Manual | |
| 3 | Examiner | Reviews the proposal for technical validity and alignment with national priorities. | Manual/Word | |
| 4 | Finance Officer | Issues a payment demand note; waits for the researcher to pay at a bank and upload the slip. | Standalone System | Major delay (2-5 days). |
| 5 | NACOSTI Admin | Manually verifies the bank slip against bank statements before generating the final PDF license. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- **Payment Latency:** Waiting for manual bank reconciliation stalls the process even after technical approval.
- **Manual Verification:** Confirming researcher credentials (from Universities) is done via email/phone.
- **Fragmented Repositories:** Research findings are not automatically captured in a searchable national knowledge base.

### Opportunities
- **Instant GPA Integration:** Using the **Government Payment Aggregator** for real-time mobile/card payments and instant license generation.
- **Automated Credential Vetting:** Integrating with **KNQA** and **CUE** via **X-Road** to verify academic standing instantly.
- **Digital Research Repository:** Automatically archiving the research abstract into a national knowledge lake once the license is issued.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Kenya DSAP Architecture - Huduma Bridge).*

```mermaid
%%{init: { 'theme': 'base', 'themeVariables': { 'fontSize': '24px', 'fontFamily': 'Inter, system-ui, sans-serif', 'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#f3f3f3', 'mainBkg': '#ffffff', 'nodeBorder': '#333333' } } }%%
graph TD
    Start((Start)) --> Portal["Researcher Logs in via eCitizen (SSO)"]
    
    subgraph Layer2["Identity & Trust Hub"]
        Portal --> Verify["X-Road: Verify academic standing via KNQA"]
        Verify --> Workflow["Workflow Engine: Initiate Case File"]
    end
    
    subgraph Layer3["Huduma Bridge / X-Road"]
        Workflow --> EthicCheck["X-Road: Cross-check Ethical Clearance (ERC)"]
        EthicCheck --> Rules["AI Rules Engine: Auto-match Examiner"]
    end
    
    subgraph Layer4["Settlement & Issuance"]
        Rules --> Pay["Initiate Payment via GPA('Real-time')"]
        Pay --> License["Auto-generate Verifiable Digital License (QR)"]
    end
    
    subgraph Knowledge_Lake["Authoritative Registry"]
        License --> Sync["Sync Abstract to National Research Repository"]
    end
    
    Sync --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff,font-size:24px,font-size:24px;;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff,font-size:24px,font-size:24px;;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff,font-size:24px,font-size:24px;;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff,font-size:24px,font-size:24px;;
    class Start start;
    class End endNode;
    class Portal userTask;
    class Verify,Workflow,EthicCheck,Rules,Pay,License,Sync serviceTask;
```

## Future State Process (TO-BE)
### Narrative
**TO-BE Process: Automated Science & Research Vetting**

**Design Principles:**
- **Zero-Touch Licensing:** For standard academic research by recognized students, the system uses **AI Rules** to auto-approve the permit once the fee is paid via **GPA**.
- **Cross-Registry Trust:** Ethical clearance from Institutional Review Boards (IRBs) is pulled via **X-Road APIs**, removing the need for physical letters.
- **Data as a Strategic Asset:** Every license issued automatically populates the national research repository, ensuring the government has visibility into all studies conducted in the country.

### Optimized Steps (Digital)

| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Researcher | Logs into the research portal. Personal and institutional data is pre-populated via IPRS and CUE. | eCitizen / SSO |
| 2 | System | Fetches the researcher's ethical clearance status directly from the Ethics Review Committee (ERC) portal via X-Road. | KeSEL / X-Road |
| 3 | System | Calculates the fee and allows the researcher to pay instantly via M-Pesa or Card. | GPA |
| 4 | System | Upon successful payment, the workflow engine triggers the issuance of a digital verifiable research license. | Output Generator |
| 5 | System | Automatically creates a record in the National Knowledge Repository, tracking the study's start and end dates. | Research Registry |

---

## References
- https://www.nacosti.go.ke
- Science, Technology and Innovation Act 2013
- Desk Review

---

## Feedback
We value your input on this blueprint. Please take a moment to provide your feedback using the link below:

[Provide Feedback](https://ee.kobotoolbox.org/x/4Ls7SlCG)
