# Kenya DSAP Architecture – Huduma Bridge (GEA Compliant)
## (with NPKI, Decentralized Mediation, and Payment Aggregation)

### System Architecture Overview
```mermaid
---
title: Kenya Huduma Ecosystem - High-Level Architecture
---
graph TD
    %% Styling
    classDef access fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#01579b
    classDef core fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#e65100
    classDef trust fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#4a148c
    classDef bridge fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#1b5e20
    classDef registry fill:#ffebee,stroke:#b71c1c,stroke-width:2px,color:#b71c1c
    classDef payment fill:#fffde7,stroke:#f57f17,stroke-width:2px,color:#f57f17

    %% Layer 1: Access Channels
    subgraph Layer1["🌐 Layer 1: Access Channels (Citizen-Centric)"]
        direction TB
        CP["💻 Citizen/Business Portals (eCitizen)"]:::access
        MA["📱 Mobile App / USSD"]:::access
        OW["👤 Officer Workbench"]:::access
        SC["🏢 Huduma Centers"]:::access
    end

    %% Layer 2: Core Platform
    subgraph Layer2["⚙️ Layer 2: Core Platform (Security & Orchestration)"]
        direction TB
        
        AG["🔌 API Gateway (Kong)"]:::core
        WE["⚙️ Workflow Engine (Camunda)"]:::core
        FS["📋 Dynamic Form Builder"]:::core
        
        subgraph TrustHub["🔐 Trust Hub"]
            direction LR
            CM["✓ Consent Manager"]:::trust
            IDP["🆔 Identity Federation (Maisha Namba)"]:::trust
            NPKI["🔑 National PKI (Root + Govt CA)"]:::trust
        end
        
        %% Internal connections
        AG --> WE
        WE --> FS
        WE --> CM
        CM --> IDP
        IDP --> NPKI
    end

    %% Layer 3: Interoperability
    subgraph Layer3["🔄 Layer 3: Interoperability (Huduma Bridge)"]
        direction TB
        KeSEL["🌉 Kenya Secure Exchange Layer (X-Road)"]:::bridge
        CSC["📚 Central Service Catalogue"]:::bridge
        Adapters["🔧 Legacy System Adapters"]:::bridge
        
        KeSEL --> CSC
        KeSEL --> Adapters
    end

    %% Layer 4: Registries & Payments
    subgraph Layer4["🏛️ Layer 4: Foundational Registries & Payments"]
        direction TB
        
        subgraph Registries["📋 Authoritative Registries"]
            direction TB
            R1[IPRS / Maisha Namba / CRS<br/>Person & Civil Registries]:::registry
            R2[BRS / LMS / NTSA / KRA<br/>Business & Revenue Registries]:::registry
            R3[NEMIS / HRMIS / IFMIS<br/>Education & Public Service]:::registry
            R4[Immigration / Judiciary / SP / Health<br/>Social & Legal Registries]:::registry
        end
        
        subgraph Payments["💰 Financial Ecosystem"]
            direction LR
            GPA["💳 Govt Payment Aggregator"]:::payment
            Banks["🏦 Banks & M-Pesa"]:::payment
            Treasury["📊 National Treasury"]:::payment
            Counties["🏛️ County Revenue Systems"]:::payment
        end
        
        %% Payment internal connections
        GPA <--> Banks
        GPA --> Treasury
        GPA --> Counties
    end

    %% Main Flow - Top to Bottom
    Layer1 ==> AG
    
    WE ==> KeSEL
    
    KeSEL ==> R1
    KeSEL ==> R2
    KeSEL ==> R3
    KeSEL ==> R4
    KeSEL ==> GPA

    %% Connect Trust Hub to Layer 3 (showing it's part of Layer 2 but feeds into bridge)
    TrustHub -.- KeSEL
```
### Data Flow Pattern (Decentralized Exchange with Consent)

```mermaid
sequenceDiagram
    participant Citizen
    participant Portal as eCitizen Portal
    participant CM as Consent Manager
    participant SSA as Agency Security Server
    participant SSB as Registry Security Server
    participant GPA as Payment Aggregator

    Citizen->>Portal: Request Service (e.g., Business Permit)
    Portal->>CM: Check Consent for IPRS Data?
    alt No Consent
        CM-->>Portal: Request User Consent
        Portal->>Citizen: "Allow access to ID data?"
        Citizen->>Portal: Yes
        Portal->>CM: Log Consent (Immutable Audit)
    end
    CM-->>Portal: Consent Validated
    Portal->>SSA: Initiate Request
    SSA->>SSB: X-Road Query (Signed via NPKI)
    SSB->>SSB: Verify Signature & Consent Token
    SSB-->>SSA: Data Response (Encrypted)
    SSA->>GPA: Initiate Payment Request
    GPA->>Citizen: Push STK / Payment Prompt
    Citizen->>GPA: Authorize Payment
    GPA->>GPA: Split Revenue (80% County, 20% Treasury)
    GPA-->>SSA: Payment Success Notification
    SSA-->>Portal: Service Delivered
```

### 1. Access Channels (Citizen-Centric Design)
Aligned with GEA Principle: **Citizen-Centricity**.
- **Unified Front-End:** Single-window access via eCitizen for all services.
- **Omnichannel:** Seamless experience across Web, Mobile App, USSD, and physical Huduma Centers.
- **Accessibility:** Designed for inclusivity (USSD for feature phones, Assistive Tech for PWDs).

---

### 2. Trust, Security & Consent (Data Protection Act Compliance)
Aligned with GEA Principle: **Security & Privacy by Design**.
- **Consent Manager:** Centralized module to capture, track, and revoke citizen consent for data sharing as required by the **Data Protection Act (2019)**. No data moves without explicit user permission.
- **National PKI (NPKI):** All transactions are digitally signed using certificates issued by the Government CA (ICTA), ensuring non-repudiation.
- **Identity Federation:** Integration with **Maisha Namba** (IPRS) for single sign-on (SSO) and robust identity verification.

---

### 3. Orchestration & Workflow (BPMN 2.0 Standard)
Aligned with GEA Principle: **Standards-Driven & Open Architecture**.
- **Workflow Engine:** Uses **BPMN 2.0** (e.g., Camunda/Flowable) to model long-running government processes. Decouples business logic from code.
- **Dynamic Forms:** JSON-schema driven forms that render automatically on any channel.
- **API Gateway:** Centralized entry point for traffic management, rate limiting, and threat protection (WAF).

---

### 4. Interoperability (GIF & X-Road)
Aligned with GEA Principle: **Interoperability by Design**.
- **Kenya Secure Exchange Layer (KeSEL):** Based on the **X-Road** protocol. Enables secure, peer-to-peer data exchange between agencies without a central data bottleneck.
- **Central Service Catalogue:** A discoverable registry of all available government APIs (G2G) to promote reuse.
- **Legacy Adapters:** Standard wrappers to connect older, monolithic MDA systems to the modern exchange layer.

---

### 5. Government Payment Aggregator (GPA)
Aligned with GEA Principle: **Reuse & Modularity**.
- **Aggregator Model:** A single integration point for all payment providers (M-Pesa, Airtel Money, T-Kash, Equity, KCB, Visa/Mastercard).
- **Split Payments:** Built-in logic to automatically split revenue at the source (e.g., a single permit fee is split into County Revenue, National Treasury, and Regulatory Agency accounts instantly).
- **Reconciliation:** Automated daily reconciliation reports for the Auditor General.
- **Real-Time Settlement:** Instant payment notifications (IPN) to service workflows to prevent service delivery delays.

---

### 6. Authoritative Registries (Single Source of Truth)
Aligned with GEA Principle: **Data as a Strategic Asset**.
The platform integrates directly with the following **Master Data Sources** to ensure data accuracy and eliminate duplication (Once-Only Principle). These registries are accessed via **PKI-authenticated APIs** through the **Kenya Secure Exchange Layer (KeSEL / X-Road)**:

-   **IPRS (Integrated Population Registration System):** Validates identity for all Citizens and Foreign Residents.
-   **Maisha Namba / NIIMS:** The single source of truth for digital identity (National ID).
-   **BRS (Business Registration Service):** Validates Company/Business registration details and beneficial ownership.
-   **NLIMS (National Land Information Management System):** Validates land ownership, parcels, and encumbrances (Ardhisasa).
-   **NTSA (National Transport & Safety Authority):** Validates vehicle ownership, driving licenses, and PSV compliance.
-   **KRA (Kenya Revenue Authority):** Validates Tax Compliance (PIN, TCC) via iTax integration.
-   **NEMIS (National Education Management Information System):** Validates student enrollment and academic records.
-   **HRMIS (Human Resource Management Information System):** Validates public servant employment status (G2E services).
-   **IFMIS (Integrated Financial Management Information System):** Validates budget codes and facilitates G2G payments.
-   **Judiciary Case Management System (CMS):** Validates court cases, fines, and legal status.
-   **Immigration (eFNS):** Validates passport, visa, and work permit status.
-   **Civil Registration (CRS):** Authoritative source for Births and Deaths records.
-   **Social Protection (Inua Jamii):** Registry for vulnerable populations and social safety nets.
-   **Health (NHIF/SHA):** Registry for health insurance coverage and beneficiaries.

---

### 7. Governance & Standards Compliance
- **ISO 27001:** Information Security Management.
- **ISO 20022:** Financial messaging standard for the Payment Aggregator.
- **TOGAF:** Architecture development methodology.
- **GIF v4.3:** Government Interoperability Framework compliance for all APIs.
