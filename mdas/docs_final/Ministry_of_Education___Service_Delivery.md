# MINISTRY OF EDUCATION – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** MINISTRY OF EDUCATION
- **Process Name:** Student Registration & Transition (NEMIS)
- **Document Version:** 1.3
- **Date:** 2026-02-19
- **Classification:** Official

---

## Executive Summary
The Ministry of Education (MoE) is responsible for national education policy and standards. The **National Education Management Information System (NEMIS)** is the central repository for all student data, assigning a Unique Personal Identifier (UPI) to every learner from Early Years Education (EYE) to University.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Manual Entry / System Glitches).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph School [Head Teacher / Principal]
        S1["Receives Student Admission (Form 1 / Grade 1)"]
        S2["Collects Birth Certificate & Parent ID Copies"]
        S3["Logs into NEMIS Portal"]
        S4["Manually Enters Student Bio-Data"]
    end
    subgraph NEMIS [NEMIS System]
        S5["Validates Birth Cert No. (Offline/Batch)"]
        S6["Generates UPI (Unique Personal Identifier)"]
        S7["Allocates Capitation Funds (FSE / FDSE)"]
    end
    subgraph Parent [Parent / Guardian]
        S8["Checks UPI Status via SMS/Portal"]
    end
    
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> End((End))
```

---

## Process Overview
### Process Name
Student Registration & Capitation (NEMIS)

### Service Category
- G2C (Government to Citizen) / G2G (Government to School)

### Scope
- **In Scope:** Registration of learners in Public/Private Basic Education institutions; Disbursement of Free Primary/Day Secondary Education funds.
- **Out of Scope:** University placement (KUCCPS handles this based on NEMIS data).

### Triggers
- Admission of a child to school (PP1, Grade 1, Form 1).
- Transfer of a student between schools.

### End States
- **Successful:** UPI Generated; Capitation Disbursed.

### Policy Context
- Basic Education Act, 2013; Sessional Paper No. 1 of 2019.

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Head Teacher | Data Entrant | Captures learner details on NEMIS. |
| County Director of Education (CDE) | Approver | Approves school registrations and transfers. |
| Parent | Beneficiary | Provides birth documents; monitors progress. |
| KNEC | Consumer | Uses NEMIS data for exam registration (KPSEA, KCSE). |

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Parent / Guardian | **Admission:** Takes child to school for admission (PP1, Grade 1, or transfer). | Physical Presence | Child must be physically present for verification. |
| 2 | Parent / Guardian | **Submission:** Submits required documents: Birth Certificate (Mandatory), Parent ID copy, Passport photo, Previous school details, Immunization card. | Physical Documents | *Constraint:* Without Birth Cert, admission is often delayed. |
| 3 | School | **Verification:** Checks authenticity of documents (Spelling, DOB, Parent details). | Manual Check | If Birth Cert missing, parent is advised to register birth first. |
| 4 | School | **Manual Recording:** Records learner details in the physical Admission Register and Class Register. | Physical Register | Creates the official school admission record (offline). |
| 5 | School Admin | **Portal Login:** Logs into NEMIS portal using school credentials. | NEMIS Web Portal | Often done at cyber cafés due to lack of school internet. |
| 6 | School Admin | **Data Entry:** Manually enters learner details into NEMIS (Birth Cert No, Name, Gender, DOB, Parent details). | NEMIS Web Portal | *Bottleneck:* School applies to NEMIS on behalf of learner; Parent cannot do this directly. |
| 7 | NEMIS System | **Validation:** Automatically checks against CRS. | Integration API | **Outcomes:** <br>• Valid: Learner accepted.<br>• Duplicate: Transfer required.<br>• Invalid: Registration rejected (Learner stuck). |
| 8 | NEMIS System | **Generation:** Generates **Unique Personal Identifier (UPI)**. | System | This becomes the learner’s permanent education ID for exams (KPSEA, KCSE) and Capitation. |
| 9 | School | **Confirmation:** Confirms learner is now fully registered and Active in NEMIS. | Dashboard | Learner is now officially recognized by Ministry of Education. |

**Summary:** The reality is that **Parents DO NOT apply directly to NEMIS**. Parents apply to the school, and the **School applies to NEMIS** on behalf of the learner. The final artifact is the **UPI Number**.

---

## Pain Points & Opportunities
### Pain Points
- **System Downtime:** NEMIS crashes frequently during Form 1 admission.
- **Data Mismatch:** Rigid validation against CRS (e.g., "Maina" vs "Maina J.") causes rejection.
- **Manual Transfers:** Moving a student requires the *previous* school to "release" them online. Head Teachers often refuse/delay this.
- **Capitation Loss:** Schools lose funds for students whose UPI generation is stuck.
- **Cyber Costs:** Head Teachers in rural areas travel long distances to access internet.

### Opportunities
- **Auto-Registration:** Link Birth Registration (CRS) to Education. A child turning 4 is *automatically* eligible for PP1.
- **Offline Mode:** Allow data capture on a mobile app without internet, syncing later.
- **Parent Self-Service:** Allow parents to register/transfer their own children via eCitizen, removing the Head Teacher bottleneck.
- **Biometrics:** Introduce simple biometrics to eliminate ghost students definitively.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Repeatable WoG Platform).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Parent [Citizen via eCitizen]
        S1["Logs into eCitizen (SSO)"]
        S2["Selects 'School Admission Service'"]
        S3["System Auto-Populates Child Details (CRS)"]
        S4["Selects Preferred School (Geo-Located)"]
    end
    subgraph WoG_Platform [Service Engine & Workflow]
        S5["Validates Age & School Capacity (Business Rules)"]
        S6["Checks Duplicate Enrollment (Unique UPI)"]
    end
    subgraph School [Head Teacher Workbench]
        S7["Receives Digital Application"]
        S8["Approves Admission (One-Click)"]
    end
    subgraph NEMIS_Core [Backend Systems]
        S9["Updates Learner Status to 'Enrolled'"]
        S10["Triggers Capitation Calculation"]
    end
    subgraph Payments [Govt Payment Aggregator]
        S11["Disburses Funds to School Account"]
        S12["Notifies Parent & School (SMS/Email)"]
    end
    
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> S9
    S9 --> S10
    S10 --> S11
    S11 --> S12
    S12 --> End((End))
```

## Detailed Process (TO-BE) - Configurable & Automated
| Step | Role | Action | System Component | Logic / Integration |
|---|---|---|---|---|
| 1 | Parent / Guardian | **Initiation:** Logs into eCitizen and selects "School Admission Service". | **eCitizen Portal** (Unified Front-End) | Authenticated via **Maisha Namba (SSO)**. |
| 2 | System | **Data Fetch:** Auto-populates child's details using Parent ID / Birth Entry Number. | **Integration Layer (X-Road)** | Fetches data from **CRS Registry** (Source of Truth). No manual entry of names/DOB. |
| 3 | Parent | **Selection:** Selects preferred school from a geo-located list. | **Service Engine** | System filters schools by **Capacity** and **Learner Age** eligibility. |
| 4 | System | **Auto-Validation:** Validates application against business rules (Age, Zone, Capacity). | **Workflow Engine** | *Rule:* If `Age < 6`, reject for Grade 1. If `Capacity = 0`, disable selection. |
| 5 | School (Head Teacher) | **Approval:** Receives digital notification and approves admission on the workbench. | **Officer Workbench** | "One-Click" approval. No physical file verification needed (Data is trusted). |
| 6 | System | **Enrollment:** Automatically links Learner UPI to School Code in NEMIS. | **NEMIS Database** | Learner status updates to `Enrolled`. |
| 7 | System | **Capitation Trigger:** Automatically calculates FSE/FDSE amount for the new learner. | **Business Rules Engine** | *Logic:* `Amount = Capitation_Rate * 1`. |
| 8 | GPA | **Disbursement:** Disburses funds directly to School Account. | **Govt Payment Aggregator** | Real-time settlement. No "ghost students." |
| 9 | Parent | **Notification:** Receives SMS/Email confirmation of admission. | **Notification Service** | "Your child has been admitted to [School Name]." |

---

## 3. Standard Data Inputs
*Required fields for the WoG Digital Service.*

### A. School Enrollment (New Admission)
| Field Name | Type | Source | Validation |
|---|---|---|---|
| Child UPI | String | System Fetch (CRS) | Must exist in CRS |
| Parent ID | String | User Input (Auth) | Must match CRS Parent |
| School Code | String | User Input / List | Must be Active School |
| Admission Date | Date | System (Today) | Auto-filled |
| Grade Level | Enum | System Calculated | Based on Age (DOB) |
| Disability Status | Enum | User Input | Optional |

### B. Student Transfer Request
| Field Name | Type | Source | Validation |
|---|---|---|---|
| Child UPI | String | User Input | Must be currently enrolled |
| From School | String | System Fetch | Read-only |
| To School Code | String | User Input | Must have capacity |
| Reason | String | Enum (Relocation, etc.) | Required |
| Transfer Date | Date | User Input | Cannot be past |

---

## References
- Basic Education Act.
