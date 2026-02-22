# 🌐 Kenya Citizen Lifecycle: Configuration Guide

This document outlines how to manage and configure the **Unified Cradle-to-Death Service Lifecycle** using the Administrative Registry Suite. Each stage of the citizen journey is modeled as a discrete, configurable **Service Node** within the National Service Registry.

---

## 🛠️ Administrative Workflow

The lifecycle is managed through three primary strategic layers:

### 1. Service Identity Registry
Define the institutional owner (MDA), the life event group, and the strategic designation of the service.
- **Access**: `Admin Dashboard` > `Service Config` > `Service Identity`
- **Key Parameters**: MDA Code (e.g., `CRS`, `NRB`), Life Event Group (e.g., `Birth`, `Education`).

### 2. Technical Schema Registry (Data Acquisition)
Configure exactly what data is harvested at each stage.
- **Mechanism**: `Form Schema Builder`
- **Configuration Path**: Edit Service > `Form Schema` tab.
- **Techniques**:
    - **Read-Only Lookups**: Set fields like `upi` or `mother_id` to `Read-Only` for cross-registry inheritance.
    - **Biometric Targets**: Define fields with Type `File` and Format `data-url` for ICAO photo or fingerprint ingestion.
    - **Validation Rules**: Assign technical designations (Machine Slugs) that match backend API orchestration keys.

### 3. Logic Backbone orchestration (Workflow)
Define the sequence of human disposition and machine logic.
- **Mechanism**: `Workflow Step Manager`
- **Configuration Path**: Edit Service > `Workflow Pipeline` tab.
- **Node Types**:
    - **Manual Institutional Action**: Used for Registrar approvals, Identity verification, or manual audits.
    - **Automated API Handshake (Bridge)**: Used for IPRS lookups, UPI minting, or ledger updates.
    - **Machine Logic (System Task)**: Internal scoring or automated validation logic.

---

## 📅 Lifecycle Node Configuration Reference

| Node ID | Service Name | Institutional Registry | Core Data Schema | Pipeline Logic |
| :--- | :--- | :--- | :--- | :--- |
| **WF-STEP-01** | **Birth Notification (Hospital)** | Ministry of Health | `mother_id`, `gender`, `dob` | Hospital Capture → IPRS Lookup → B1 Notification |
| **WF-STEP-01b** | **Birth Certificate Issuance** | Civil Registration (CRS) | `notification_number`, `child_name` | Citizen Init → B1 Verification → UPI MINTING → Registrar Approval |
| **WF-STEP-03** | **Education (NEMIS)** | MoE (Basic Education) | `upi`, `school_code` | Parent Request → NEMIS Validation → Enrollment |
| **WF-STEP-04** | **Maisha Namba Upgrade** | NRB (Identification) | `fingerprints`, `photo` | Biometric Ingestion → AFIS Check → ID Issuance |
| **WF-STEP-06** | **Passport Issuance** | Immigration Services | `upi`, `live_selfie` | Record Fetch → Security Screening → DTC Minting |
| **WF-STEP-08** | **Marriage Registry** | State Law Office (AG) | `groom_id`, `bride_id` | Notice Filing → Legal Review → Spousal Linking |
| **WF-STEP-10** | **Succession & Probate** | The Judiciary | `death_cert_no`, `assets` | Death Trigger → Inventory Audit → Estate Grant |

---

## 🚀 Deployment & Seeding

To reset the lifecycle baseline to the national standard, execute the unified seeding utility:

```bash
python3 backend/seed_unified_catalogue.py
```

### Strategic Synchronization Tips
- **Inheritance**: Always use the Maisha Namba (`upi`) as the primary key in schemas to ensure data traverses the lifecycle.
- **Transparency**: Update the `Description` field to explain how institutional data flows from the previous milestone.
- **Authority**: Ensure Roles are assigned strictly (e.g., `CRS Registrar`, `Immigration Officer`) to maintain institutional trust.
