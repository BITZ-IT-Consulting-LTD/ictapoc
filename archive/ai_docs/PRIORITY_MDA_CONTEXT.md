# Priority MDA Services, Workflows & Forms Context

This document outlines the standard structure and required context for defining, creating, or updating functional services for Priority MDAs in the ICTA POC platform.

## 1. Core Architecture

The system uses a 3-tier hierarchy to model government services:
1. **MDA (Ministry, Department, or Agency)**: The owner of the service.
2. **ServiceConfig**: The actual service being delivered to the citizen/business. It contains metadata, categorization, and the UI Form Schema (`form_schema`).
3. **WorkflowStep**: A sequenced set of steps defining the business process (BPMN-like). Divided into `as_is` (current manual state) and `to_be` (optimized digital state).

---

## 2. Service Definition (`ServiceConfig`)

When defining or updating a service, you must populate the `ServiceConfig` model. This defines how the service appears in the catalogue and what rules govern it.

### Key Fields:
- **`service_code`**: Unique identifier (e.g., `MOH-001`, `AFA-002`).
- **`service_name`**: Human-readable name (e.g., "Food Import Permit").
- **`mda`**: Foreign key to the owning MDA.
- **`service_family` / `service_groups`**: Used for grouping (e.g., "Business & Revenue").
- **`service_status`**: Usually `active`.
- **`priority`**: Set to `high` or `critical` for priority MDAs.
- **`is_public_facing`**: Boolean (True if citizens apply).
- **`form_schema`**: The JSON Schema dictating the frontend form (see Section 3).
- **`config`**: JSON containing rules, SLA, outputs.

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
      "lookup_service": "IPRS" // Indicates this field should trigger an API lookup
    },
    "document_upload": {
      "type": "string",
      "format": "data-url",
      "title": "Attach Supporting Document"
    }
  }
}
```
*Note: If `form_schema` is empty, the system falls back to the `shared_form_schema` defined in the service's `ServiceFamily`.*

---

## 4. Workflow Definition (`WorkflowStep`)

Workflows are built using sequential steps attached to a `ServiceConfig`. To make a service fully functional, you need to define the `to_be` lifecycle stages.

### Key Fields for a Step:
- **`step_name`**: Name of the action (e.g., "Review Application").
- **`step_type`**: `manual` (requires user intervention) or `api_call` (automated system integration).
- **`bpmn_element_type`**: `start_event`, `user_task`, `service_task`, `exclusive_gateway`, or `end_event`.
- **`lifecycle_stage`**: `to_be` (for the functional digital workflow) or `as_is` (for legacy reference).
- **`sequence`**: Integer order (1, 2, 3...).
- **`role`**: Which RBAC role is responsible (e.g., `MDA_OFFICER`, `SUPERVISOR`).
- **`action`**: The system action taken (e.g., `APPROVE`, `REJECT`, `ISSUE_CERTIFICATE`).

### Example Workflow Flow:
1. **Sequence 1**: `Start Event` - Citizen submits the form (Payload captured against `ServiceRequest`).
2. **Sequence 2**: `User Task` - MDA Officer reviews documents (`role`: `MDA_OFFICER`).
3. **Sequence 3**: `Service Task` - Payment Gateway / API call (`step_type`: `api_call`).
4. **Sequence 4**: `End Event` - Issue Permit & Close Request.

---

## 5. Integration & Adapters (`RegistryAdapter` & `RegistryEndpoint`)

For priority MDAs that require external validation (like IPRS for Identity, KRA for Tax, or NTSA for vehicles):
- Steps with `step_type = 'api_call'` should link to a `RegistryEndpoint`.
- Adapters can be mocked (`is_mock = True`) during POC, with `mock_data` handling the simulated responses.

---

## 6. Implementation Strategy for POC

To update or seed these entities functionally:
1. Ensure the `MDA` exists in the database with `is_priority=True`.
2. Construct a JSON or Python dictionary representing the `ServiceConfig` (including `form_schema` and `config`).
3. Construct a list of dictionaries for `WorkflowStep` entries representing the `to_be` workflow.
4. Utilize or create a custom seeding script (similar to `backend/seed_form_schemas.py` or `backend/seed_priority_mdas.py`) that uses Django ORM (`ServiceConfig.objects.update_or_create(...)`) to inject the definitions.

---

## 7. Sourcing Business Processes & Workflows (Anti-Hallucination)

When generating, updating, or migrating workflows and form schemas for the POC, **do not invent or hallucinate the business processes**.

All factual data regarding the specific steps, forms, required documents, and approval hierarchies must be sourced strictly from the official Business Process Reengineering (BPR) documentation, AS-IS/TO-BE analysis reports, or official MDA procedure manuals. 

If generating scripts or configurations for a specific service:
1. **Reference Real Data:** Request or provide the specific markdown, PDF, or text file containing the actual service flow before building the `ServiceConfig` or `WorkflowStep` objects.
2. **Placeholder Over Invention:** If a specific field or step is unknown, use explicit placeholders (e.g., `[TBD: Awaiting BPR Confirmation]`) rather than guessing.
3. **Align with Mappings:** Use the provided process maps to determine whether a step is a `manual` user task, an `api_call` (integration), or an `exclusive_gateway` (decision node).

---

## 8. Directory Sourcing & TO-BE Focus

When generating seeding files, strict adherence to the correct files and workflow stages is required:
1. **Source Directory:** All business process information MUST be extracted from the markdown files located in `/Users/mac/ictapoc/mdas/docs_final/priority_mdas`.
2. **Strict TO-BE Focus:** Completely ignore any AS-IS (legacy) workflows mentioned in the documents. Generate `WorkflowStep` objects exclusively where `lifecycle_stage = 'to_be'`.

---

## 9. Dummy Registries, Instant Processing & Fallbacks

The POC utilizes mocked dummy registries, meaning system behavior must reflect instant decision-making with robust manual fallbacks:
1. **Instant Processing:** System validations and registry checks should be modeled as `api_call` steps that execute instantly (`is_mock = True`). The primary workflow path should assume instant automated approval or validation from these registries.
2. **Mandatory Manual Intervention Fallbacks:** Real-world systems fail. For every automated `api_call` (dummy registry check), you MUST immediately follow it with an `exclusive_gateway` node.
3. **Fallback Routing:** If the API check fails (e.g., mismatch in IPRS or KRA), the gateway must route to a `manual` step (`user_task`) assigned to an `MDA_OFFICER` for manual intervention and review, before returning to the main flow or terminating.

---

## 10. Form Inference

Because frontend forms are completely dynamic, they must be inferred directly from the TO-BE process steps:
1. **Analyze Requirements:** Infer the `form_schema` (JSON Schema) by analyzing the required documents and citizen inputs described in the TO-BE process of the markdown document.
2. **Logical Mapping:** For example, if the process mentions 'Submit KRA Pin and Business Certificate', create corresponding fields in the `form_schema` with logical types (`string` for PIN, `data-url` for document uploads).

---

## 11. Available Dummy Registries

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