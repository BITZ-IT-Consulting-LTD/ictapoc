# Cradle to Death Services, Workflows & Forms Context

This document outlines the standard structure and required context for defining, creating, or updating functional services for the "Cradle to Death" citizen lifecycle MDAs in the ICTA POC platform.

## 1. Core Architecture

The system uses a 3-tier hierarchy to model government services:
1. **MDA (Ministry, Department, or Agency)**: The owner of the service.
2. **ServiceConfig**: The actual service being delivered to the citizen/business. It contains metadata, categorization, and the UI Form Schema (`form_schema`).
3. **WorkflowStep**: A sequenced set of steps defining the business process (BPMN-like). Divided into `as_is` (current manual state) and `to_be` (optimized digital state).

---

## 2. Service Definition (`ServiceConfig`)

When defining or updating a service, you must populate the `ServiceConfig` model. This defines how the service appears in the catalogue and what rules govern it.

### Key Fields:
- **`service_code`**: Unique identifier (e.g., `CRS-001`, `NRB-001`).
- **`service_name`**: Human-readable name (e.g., "Birth Registration", "National ID Registration").
- **`mda`**: Foreign key to the owning MDA.
- **`service_family` / `service_groups`**: MUST be mapped to the specific Catalogue Life-Cycle Group the service belongs to, directly referencing the sections in the mapping document (i.e., "The Cradle", "Childhood & Education", "Coming of Age", "Economic Life", "Family & Property", or "The Death").
- **`service_status`**: Usually `active`.
- **`priority`**: Set to `critical` for Cradle to Death services.
- **`is_public_facing`**: Boolean (True if citizens apply).
- **`form_schema`**: The JSON Schema dictating the frontend form.
- **`config`**: JSON containing rules, SLA, outputs, and event-bus triggers (e.g., triggering SHA registration on birth).

---

## 3. Form Schema (`form_schema`)

The frontend dynamically generates forms based on standard JSON Schema definitions stored in `ServiceConfig.form_schema`.

### Standard Form Schema Structure:
```json
{
  "title": "Service Application Form",
  "type": "object",
  "required": ["applicant_name", "id_number"],
  "properties": {
    "applicant_name": {
      "type": "string",
      "title": "Full Name"
    },
    "id_number": {
      "type": "string",
      "title": "National ID Number",
      "lookup_service": "IPRS"
    },
    "document_upload": {
      "type": "string",
      "format": "data-url",
      "title": "Attach Supporting Document"
    }
  }
}
```

---

## 4. Workflow Definition (`WorkflowStep`)

Workflows are built using sequential steps attached to a `ServiceConfig`. To make a service fully functional, you need to define the `to_be` lifecycle stages.

### Key Fields for a Step:
- **`step_name`**: Name of the action.
- **`step_type`**: `manual` (requires user intervention) or `api_call` (automated system integration).
- **`bpmn_element_type`**: `start_event`, `user_task`, `service_task`, `exclusive_gateway`, or `end_event`.
- **`lifecycle_stage`**: `to_be` (for the functional digital workflow).
- **`sequence`**: Integer order (1, 2, 3...).
- **`role`**: Which RBAC role is responsible (e.g., `MDA_OFFICER`, `SYSTEM`).
- **`action`**: The system action taken (e.g., `APPROVE`, `ISSUE_CERTIFICATE`, `TRIGGER_EVENT`).

---

## 5. Sourcing Business Processes & Workflows (Anti-Hallucination)

When generating, updating, or migrating workflows and form schemas for the POC, **do not invent or hallucinate the business processes**.

All factual data regarding the specific steps, forms, required documents, and approval hierarchies must be sourced strictly from the official Cradle to Death documentation.

If generating scripts or configurations for a specific service:
1. **Reference Real Data:** Request or provide the specific markdown file containing the actual service flow before building the `ServiceConfig` or `WorkflowStep` objects.
2. **Placeholder Over Invention:** If a specific field or step is unknown, use explicit placeholders (e.g., `[TBD: Awaiting BPR Confirmation]`) rather than guessing.
3. **Align with Mappings:** Use the provided process maps to determine whether a step is a `manual` user task, an `api_call` (integration), or an `exclusive_gateway` (decision node).

---

## 6. Directory Sourcing & TO-BE Focus

When generating seeding files, strict adherence to the correct files and workflow stages is required:
1. **Source Files:** All business process information MUST be extracted from the markdown files listed in `/Users/mac/ictapoc/mdas/docs_final/Cradle_to_Death_MDAs.md`. These files reside in `/Users/mac/ictapoc/mdas/docs_final/`.
2. **Strict TO-BE Focus:** Completely ignore any AS-IS (legacy) workflows mentioned in the documents. Generate `WorkflowStep` objects exclusively where `lifecycle_stage = 'to_be'`.
3. **Event-Driven Workflows:** Cradle to Death processes often trigger secondary processes (e.g., Birth Registration triggers IPRS update and SHA enrollment). Represent these event triggers as `service_task` with `api_call`.

---

## 7. Dummy Registries, Instant Processing & Fallbacks

The POC utilizes mocked dummy registries, meaning system behavior must reflect instant decision-making with robust manual fallbacks:
1. **Instant Processing:** System validations and registry checks should be modeled as `api_call` steps that execute instantly (`is_mock = True`). The primary workflow path should assume instant automated approval or validation from these registries.
2. **Mandatory Manual Intervention Fallbacks:** Real-world systems fail. For every automated `api_call` (dummy registry check), you MUST immediately follow it with an `exclusive_gateway` node.
3. **Fallback Routing:** If the API check fails, the gateway must route to a `manual` step (`user_task`) assigned to an `MDA_OFFICER` for manual intervention and review, before returning to the main flow or terminating.

---

## 8. Form Inference

Because frontend forms are completely dynamic, they must be inferred directly from the TO-BE process steps:
1. **Analyze Requirements:** Infer the `form_schema` (JSON Schema) by analyzing the required documents and citizen inputs described in the TO-BE process of the markdown document.
2. **Logical Mapping:** Create corresponding fields in the `form_schema` with logical types (`string` for PIN, `data-url` for document uploads).

---

## 9. Available Dummy Registries

When generating `api_call` workflow steps, use the exact uppercase keys below to link to the POC's mocked dummy registries. Set the `config["registry_name"]` to one of these keys.

### Identity & Civil Registration
- **`IPRS`**: Integrated Population Registration System (citizen identity)
- **`NRB`**: National Registration Bureau (ID cards/Maisha card)
- **`CRS`**: Civil Registration Services (Birth/Death certificates)
- **`IMMIGRATION`**: Department of Immigration Services (Passports/Visas)
- **`MAISHA_AUTH`**: Digital ID Authentication Service
- **`LIVESCAN_KIT`**: Biometric Collection Service
- **`ECITIZEN_APP`**: eCitizen Account Registry

### Business & Entities
- **`BRS`**: Business Registration Service (companies/business names)
- **`KRA`**: Kenya Revenue Authority (PINs/tax compliance)
- **`NGO_BOARD`**: NGO Coordination Board

### Land & Assets
- **`ARDHISASA`**: National Land Information Management System
- **`COLLATERAL`**: Movable assets registry

### Transport
- **`NTSA`**: National Transport and Safety Authority (vehicles/driving licenses)
- **`KCAA`**: Kenya Civil Aviation Authority (aircraft)

### Education & Professionals
- **`NEMIS`**: National Education Management Information System (student UPIs)
- **`HELB`**: Higher Education Loans Board
- **`KNEC`**: Kenya National Examinations Council
- **`TSC`**: Teachers Service Commission
- **`PROFESSIONAL_BODIES`**: EBK, KMPDC, LSK members

### Social Services & Health
- **`SOCIAL_PROTECTION`**: Single Registry / Inua Jamii (beneficiaries)
- **`SHA`**: Social Health Authority / NHIF
- **`NSSF`**: National Social Security Fund
- **`HOSPITAL`**: Master Facility List / General Hospital Registry
- **`HOSPITAL_HIS`**: Hospital Information System (patient records)

### Other Key Registries
- **`JUDICIARY`**: Judiciary Case Tracking System (CTS)
- **`GAZETTE`**: Kenya Gazette
- **`IEBC`**: Voter Register

---

## 10. The "Once-Only" Principle & KeSEL Data Fetching

The architecture relies on the Kenya Secure Exchange Layer (KeSEL) to enforce the "Once-Only Principle." Citizens must not be asked to manually enter data that resides in a foundational registry.

**Rules for Seeding:**
1. **Minimalist Forms:** The `form_schema` should only collect the primary identifier (e.g., `parent_id_number`, `upi`, `kra_pin`) and any genuinely new data. Do not create text fields for `first_name`, `date_of_birth`, or `gender` if an ID or UPI is being provided.
2. **Pre-Verification API Steps:** Every workflow that relies on an identity or entity must begin with an `api_call` step to fetch data from the relevant registry (e.g., an `api_call` to `IPRS` to validate the parent's ID during Birth Registration, or an `api_call` to `CRS` to validate a child's UPI during School Enrollment).
3. **Data Chaining:** Recognize the sequence of the lifecycle. A UPI generated in `CRS` becomes the lookup key for `NEMIS`, which then feeds into `NRB`, etc. Ensure the workflow steps reflect querying the upstream registry.