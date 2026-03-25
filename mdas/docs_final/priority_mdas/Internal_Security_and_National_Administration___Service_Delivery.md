# INTERNAL SECURITY AND NATIONAL ADMINISTRATION – Business Process Architecture

## Cover Page
- **Ministry:** Ministry of Interior and National Administration
- **State Department:** State Department for Internal Security and National Administration
- **Primary Authority:** National Government Administration Officers (NGAO) / Security Directorate
- **Document Type:** Business Process Architecture (BPA) Standardised
- **Document Version:** 4.1
- **Date:** 2026-03-25
- **Classification:** Official / Restricted
- **Strategic Category:** Priority MDA - National Registry (Tier 1)
- **Service Model:** G2C / G2G
- **Reviewer:** Senior Government Enterprise Architect

---

## SECTION 0: SERVICE PRIORITISATION MAPPING
- **Mapped Priority Service:** National Government Coordination and Public Security Registries
- **Tier Classification:** Tier 1
- **Strategic Category:** Governance / Security (Law & Order)
- **Breakout Room Classification:** Room 1 (High Impact & Large Registries)
- **Lead MDA (Standardised Name):** State Department for Internal Security and National Administration
- **Related Cross-Cutting Services:**
    - National Incident Registry (Unified)
    - Identity Layer (IPRS / Maisha Namba)
    - X-Road (NPS / NIS / NDOC Interop)
    - National EDRMS (Security & Intelligence Files)
    - Government Payment Aggregator (GPA / Licensing Fees)

---

## SECTION 0.1: PRIORITISATION JUSTIFICATION
This service is prioritised because the TO-BE design transforms the State Department from a manual paper-coordinator into a "Digital Hub for National Administration." By integrating with IPRS (Identity) and the National Police Service (Incident Reporting) via X-Road, the design enables real-time field coordination across all 47 counties and 300+ sub-counties. This transformation eliminates the critical "information lag" during national emergencies, automates the issuance of public permits (Baraza, Protest, and Private Security licenses), and provides the Executive with a real-time, data-driven "National Security & Administration Dashboard."

| Criteria | Evidence from TO-BE Design |
| :--- | :--- |
| **Demand / Volume** | Continuous coordination for 30M+ citizens; thousands of weekly administrative reports. |
| **National Priority Alignment** | Constitution Articles 189/238; National Security Strategy; Ease of Doing Business. |
| **Data Reusability** | National coordination data is the primary input for Disaster Response (NDMA/Red Cross). |
| **Interoperability** | Secure data pipelines with IPRS, BRS (Private Security), and NPS via Huduma Bridge. |
| **Revenue / Efficiency Impact** | Automated licensing for Gaming, Private Security, and Public Events via GPA. |
| **Governance / Risk Reduction** | Real-time tracking of administrative field-officer (NGAO) actions ensures accountability. |
| **Inclusivity** | Mobile-first reporting tools for Village Elders and Chiefs to feed into the National Registry. |
| **Readiness** | High; Basic coordination structures exist; G-Cloud infrastructure is available for scaling. |

> [!NOTE]
> “The TO-BE design transforms the State Department from a manual paper-coordinator into a 'Digital Hub for National Administration.' By integrating with IPRS (Identity) and the National Police Service (Incident Reporting) via X-Road, the design enables real-time field coordination for all 47 counties. This eliminates the 'information lag' during national emergencies, automates the issuance of public permits (Baraza/Event permits), and creates a unified national security dashboard for the executive.”

---

# SECTION 1: SERVICE DEFINITION (STANDARDISED)

The State Department for Internal Security and National Administration is mandated to provide internal security oversight and coordinate National Government functions. 

In this refactored BPA, the primary service is the **National Administration Coordination & Regulatory Licensing** lifecycle. The focus shifts from ad-hoc email/letter coordination to a **Unified Administration Engine** where all security incidents, public permits, and field reports are captured in real-time via the **Huduma Bridge**.

---

# SECTION 2: SERVICE CATALOGUE (NORMALISED)

| Category | Service Name | Description |
| :--- | :--- | :--- |
| **Core Services** | **Public Event/Baraza Permitting** | Digital application and issuance of permits for public gatherings. |
| | **National Incident Reporting** | Real-time field-to-headquarters security incident logging (NGAO). |
| **Extended Services** | **Private Security Licensing** | Regulatory oversight and licensing of private security firms and guards. |
| | **Gaming & Lotteries Permits** | End-to-end licensing and compliance tracking for gaming operators. |
| **Special Case Services**| **Disaster Response Coordination**| Coordinated dispatch and tracking of emergency assets (G2G). |
| | **Border Management Alerts** | Real-time coordination of border post status and incident tracking. |

---

# SECTION 3: AS-IS PROCESS FLOWS (MANUAL/UNCOORDINATED)

The current state is characterized by manual document verification and physical registries, leading to high turnaround times and risks of fraudulent permits.

### 3.1 AS-IS Visualization
```mermaid
%%{init: { 'theme': 'base', 'themeVariables': { 'fontSize': '24px', 'fontFamily': 'Inter, system-ui, sans-serif', 'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#f3f3f3', 'mainBkg': '#ffffff', 'nodeBorder': '#333333' } } }%%
flowchart TD
    Start((Start)) --> S1[Submit Application/Request via Email/Letter]
    
    subgraph Registry_Silo["Front Office"]
        S1 --> S2[Registry receives & manually classifies]
        S2 --> S3[Physical File Creation]
    end

    subgraph Review_Layer["Technical Review"]
        S3 --> S4[Officer reviews against Manual Policy docs]
        S4 --> S5[Physical Inspection (if required)]
    end

    subgraph Approval_Layer["Management"]
        S5 --> S6[Accounting Officer signs Physical Permit/Approval]
        S6 --> S7[Manual Notification to Customer]
    end

    S7 --> End((End))
```

### 3.2 Operational Reality
- **Actors:** Registry Clerk, Technical Officer, Management, Customer.
- **Systems:** Manual Registers, Physical Files, Standalone Email.
- **Pain Points:** 14-day delay for simple permits; high risk of counterfeit physical licenses; lack of real-time visibility on field officer activity; inconsistent data capture across different sub-counties.

---

# SECTION 4: TO-BE PROCESS INTERPRETATION (NEW LAYER)

### 4.1 TO-BE Process (Digital Administration Engine)
```mermaid
%%{init: { 'theme': 'base', 'themeVariables': { 'fontSize': '20px', 'fontFamily': 'Inter, system-ui, sans-serif', 'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#f3f3f3', 'mainBkg': '#ffffff', 'nodeBorder': '#333333' } } }%%
flowchart TD
    Start((Start)) --> S1[Login via Maisha Namba (SSO)]
    
    subgraph Trust_Hub["Layer 2: X-Road Interop"]
        S1 --> S2[Auto-fetch Identity & BRS details via X-Road]
        S2 --> S3[Auto-validation of Compliance (KRA/NPS)]
    end

    subgraph Intelligence["Layer 2 & 3: Smart Vetting"]
        S3 --> S4[Rules Engine: Risk-based Application Sorting]
        S4 -- "Low Risk" --> S5[Automated Permit Generation (NPKI)]
        S4 -- "High Risk" --> S6[Digital Officer Review Workbench]
    end

    subgraph Settlement["Layer 4: Registries & Issuance"]
        S6 --> S5
        S5 --> S7[Verifiable Digital Permit with Secure QR Code]
        S7 --> S8[Automated Sync to National Incident Registry]
    end

    S8 --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff,font-size:20px;;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff,font-size:20px;;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff,font-size:20px;;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff,font-size:20px;;
    
    class Start start;
    class End endNode;
    class S1,S6 userTask;
    class S2,S3,S4,S5,S7,S8 serviceTask;
```

### 4.2 Key Capabilities Introduced
*   **Automation:** Automated rules engine for low-risk permit approvals (e.g., standard event permits).
*   **Integration:** Real-time compliance checks against BRS (Business), KRA (Tax), and NPS (Security Clearance) via X-Road.
*   **Real-time Processing:** Instant generation of verifiable digital certificates with NPKI-secured QR codes.
*   **Digital Identity Validation:** Applicant identity and business status verified via **Maisha Namba** identity federation.
*   **Workflow Orchestration:** Orchestrates the complex coordination between field officers (NGAO) and central management.

### 4.3 Transformation Summary
| Dimension | AS-IS | TO-BE |
| :--- | :--- | :--- |
| **Processing** | Manual / Scattered | Digital / Unified Engine |
| **Verification** | Physical Cross-checks | API-based (BRS/IPRS/NPS) |
| **Records** | Regional Paper Files | National Coordination Registry |
| **Tracking** | Post-event status updates | Real-time Incident/License Dashboard |

---

# SECTION 5: SYSTEM LANDSCAPE (ALIGN TO GEA)

| Layer | System / Platform | Role |
| :--- | :--- | :--- |
| **Identity Layer** | Maisha Namba (IPRS) | Identity and bio-login for all field officers and applicants. |
| **Interoperability** | KeSEL (X-Road) | Data link to NPS, BRS, and KRA. |
| **shared Services** | National EDRMS | Secure digital archive for regulatory and security files. |
| **Workflow / BPM** | Administration Workflow Engine | Orchestrates permitting and coordination flows. |
| **Payment Layer** | GPA (Finance Aggregator) | Automated fee reconciliation for licenses and permits. |
| **Trust Hub** | Consent Manager | Citizen control over shared security-clearance data. |

---

# SECTION 6: TRANSFORMATION VALUE (CRITICAL ADDITION)

| Value Type | Explanation |
| :--- | :--- |
| **Efficiency Gain** | Permit turnaround reduced from 14 days to instant (for low-risk) or 24h. |
| **Economic Impact** | Accelerates the licensed events and private security hospitality sectors. |
| **Governance Impact** | Full traceability of field coordinates ensures national government presence everywhere. |
| **Citizen Experience** | Transparent, predictable application process via eCitizen Mobile. |
| **Interoperability Value** | Unified dashboard for "National Security Posture" available to the Cabinet. |

---

# SECTION 7: ALIGNMENT TO WHOLE-OF-GOVERNMENT ARCHITECTURE
- **Shared Platforms:** Uses eCitizen for portal access and NPKI for all official permits.
- **Registry Reuse:** Reuses BRS (Business) and IPRS (Identity) data to avoid redundant data capture.
- **Compliance with GEA / GIF:** Standardizing incident metadata schemas for whole-of-government disaster response.

---

# SECTION 8: IMPLEMENTATION READINESS (NEW)
*   **Data Readiness:** High; Application data for Gaming and Security is already collected.
*   **Legal Readiness:** High; Internal Security Act and Gaming Act support digital transformation.
*   **Institutional Readiness:** High; NGAO network (Chiefs to Regional Commissioners) is ready for tablets.
*   **Technical Readiness:** High; G-Cloud infrastructure is available for the central coordinación hub.

---

# SECTION 9: TRACEABILITY MATRIX (NEW)

| BPA Process | Priority Service | Tier | TO-BE Capability | National Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Permit Issuance** | Licensing | T1 | Rules-based Auto-Approve | Ease of Doing Business |
| **Incident Log** | Coordination | T1 | Real-time X-Road Sync | National Security Response |
| **Officer Track** | Field Mgt | T1 | GPS-stamped Reporting | Administrative Accountability |
| **Verification** | Compliance | T1 | QR-verifiable Permits | Fraud & Impersonation Prevention|

---
**[End of Standardised Business Process Architecture]**
