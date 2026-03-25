# ICT AND DIGITAL ECONOMY – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Ministry of Information, Communications and the Digital Economy
- **Department:** State Department for ICT and the Digital Economy (SDICT)
- **Process Name:** Digital Government Infrastructure & ICT project Coordination
- **Document Version:** 3.0 (DPI Aligned)
- **Date:** 2026-03-25
- **Classification:** Official
- **Strategic Category:** Priority MDA / Architecture Authority
- **Service Model:** G2G / G2B / G2C
- **Life-Cycle Group:** Infrastructure & Governance

---

## Service Mandate
**Official Website:** [www.ict.go.ke](https://www.ict.go.ke)

The State Department for ICT and Digital Economy (SDICT) is the national authority for the **Digital Superhighway**. It is mandated to coordinate the digitization of all government services, manage national ICT infrastructure (NOFBI), and set the standards for the **Kenya Digital Shared Services Architecture Platform (DSAP)**.

**Critical DPI Components Managed:**
- **Huduma Bridge (KeSEL / X-Road):** The national interoperability backbone.
- **Government Cloud (G-Cloud):** Centralized secure hosting.
- **Trust Hub:** Managing National PKI and digital certificates.
- **Shared Services:** Workflow engines, IDP, and Notification services for use by all MDAs.

---

## Executive Summary
The State Department for ICT and the Digital Economy acts as the **Architectural Orchestrator** for Kenya's Digital Public Infrastructure (DPI). This BPD refines the coordination process for national ICT projects to ensure 100% alignment with the **Huduma Bridge model**. 

By transitioning from manual "Standards Checks" to **BPMN-orchestrated workflows**, the department ensures that every government system is born interoperable. The **National Records Registry (EDRMS)** now serves as the permanent archive for all ICT policies and digital asset configurations, while **KeSEL (X-Road)** is established as the mandatory layer for all inter-agency data exchanges.

---

## 1. DPI-ALIGNED ARCHITECTURE (4 LAYERS)

All ICT and Digital Economy processes are mapped to the national architecture:

### Layer 1: Access (The Frontend)
- **eCitizen:** Primary interface for citizens and businesses.
- **Officer Workbench:** Centralized dashboard for ICT Authority and SDICT officers to review projects and policies.

### Layer 2: Core Platform (Shared Services)
- **Workflow Engine (BPMN):** Orchestrates project approvals, policy reviews, and infrastructure requests.
- **Trust Hub (NPKI):** Issues digital seals for approved ICT standards and policies.
- **Notification Service:** Real-time updates to MDAs on project milestones.

### Layer 3: Interoperability (The Bridge)
- **Huduma Bridge (KeSEL / X-Road):** Mandatory conduit for all MDA system integrations (e.g., KRA, IPRS, BRS).

### Layer 4: Registries (Authority)
- **National Records Registry (EDRMS):** Authoritative archive for Policies, Standards, and Project Charters.
- **National Digital Asset Registry:** Tracking all government software, hardware, and IP.

---

## 2. REFINED TO-BE PROCESS FLOW

| Step | Layer | Actor | Action | Component |
|---|---|---|---|---|
| **1** | Access | MDA | Submits Digitization Plan / Infrastructure request via eCitizen Workbench. | Officer Workbench |
| **2** | Core | BPMN Engine | Automatically creates a project instance and assigns to SDICT/ICTA review team. | Workflow Engine |
| **3** | Registries | SDICT Officer | Validates the request against current **National ICT Standards** archived in EDRMS. | EDRMS |
| **4** | Interop | KeSEL | Automatically fetches existing MDA system metadata via **KeSEL (X-Road)** to check for duplication. | KeSEL Bridge |
| **5** | Core | Trust Hub | Digitally signs the **Letter of Approval / Technical Clearance** using NPKI. | Trust Hub (NPKI) |
| **6** | Registries | System | Provisions required assets (e.g., G-Cloud space, API keys) and logs in Asset Registry. | Asset Registry |
| **7** | Delivery | Notification | Notifies MDA of project commencement and provides integration adapters. | Notification Service |

---

## 3. DESIGN PRINCIPLES (KDEAP COMPLIANCE)

- **Interoperable by Design:** No system is cleared unless it includes a native **KeSEL (X-Road)** adapter.
- **Registry-First:** All policy decisions must be referenced against the **National Records Registry (EDRMS)**.
- **Human-in-the-Loop:** While workflows are automated, the final technical clearance remains a human-validated decision supported by the BPMN engine.
- **Decoupled Architecture:** Separating the application logic from the underlying DPI components (Identity, Payment, Trust).

---

## 4. COMPLIANCE & GOVERNANCE

The department ensures all MDAs adhere to:
- **Kenya DSAP Architecture:** Establishing a unified stack for government apps.
- **Executive Order No. 1 of 2025:** Mandating centralized registry-driven governance.
- **Cybersecurity Standards:** Enforcing NPKI-based non-repudiation for all digital transactions.

---

## 5. CHANGE LOG

| Area | Original State | Refined (DPI) State | Impact |
|---|---|---|---|
| **Orchestration** | Manual project reviews. | **BPMN-driven** project lifecycle. | Faster approvals and transparent audit trails. |
| **Integration** | Ad-hoc system connections. | Mandatory **KeSEL (X-Road)** adapters. | 100% interoperability across MDAs. |
| **Records** | Physical files / Standalone PDFs. | **EDRMS** as the National Records Registry. | Legal archival and instant policy retrieval. |
| **Trust** | Physical stamps/signatures. | **Trust Hub (NPKI)** digital seals. | Non-repudiation and security of ICT clearances. |

---

## References
- Kenya DSAP/KDEAP Architecture Framework (2025)
- National ICT Policy (2019)
- Executive Order No. 1 of 2025
- Data Protection Act (2019)

---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)
