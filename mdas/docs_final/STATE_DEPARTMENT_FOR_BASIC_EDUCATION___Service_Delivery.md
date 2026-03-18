# STATE DEPARTMENT FOR BASIC EDUCATION – Student Registration & Transition (NEMIS)

## Cover Page
- **Ministry/Department/Agency (MDA):** STATE DEPARTMENT FOR BASIC EDUCATION
- **Process Name:** Student Registration & Transition (NEMIS)
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The National Education Management Information System (NEMIS) is a central registry for student data, assigning a Unique Personal Identifier (UPI) to learners across all education levels, from Early Years Education (EYE) to University. This document outlines the AS-IS process for student registration and UPI allocation within Nemis.

---

## 1. AS-IS PROCESS: Student Registration in NEMIS

**Registry:** National Education Management Information System
**Owner:** Ministry of Education Kenya
**Purpose:** Assign a Unique Personal Identifier (UPI) and track learner lifecycle

### AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization (Manual Entry / System Glitches).*

```mermaid
graph TD
    Start((Start)) --> S1

    subgraph Parent_Guardian [Parent / Guardian]
        S1["Child Admitted to School (Presents documents)"]
    end

    subgraph School_NEMIS_Operator [School / NEMIS Operator]
        S2["School Logs into NEMIS"]
        S3["Open Learner Registration Module"]
        S4["Enter Learner Bio Data"]
        S5["Enter Parent / Guardian Details"]
        S6["Upload Supporting Documents"]
    end

    subgraph NEMIS_System [NEMIS System]
        S7["Submit Registration (Validates Birth Certificate)"]
        S8["UPI Generated"]
    end

    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> S8
    S8 --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;

    class Start start;
    class End endNode;
    class S1,S2,S3,S4,S5,S6 userTask;
    class S7,S8 serviceTask;
```

### BUSINESS PROCESS OVERVIEW
**Process Name:** Learner Registration and UPI Allocation
**Trigger:** Child admitted to school (PP1, Grade 1, or transfer)

### ACTORS
| Actor             | Role                       |
|-------------------|----------------------------|
| Parent / Guardian | Provides student documents |
| School Headteacher | Approves registration      |
| School NEMIS Operator | Enters student data        |
| Ministry of Education | Maintains system           |

### AS-IS WORKFLOW STEPS
| Step | Actor                 | Action                                                                | Tool / System | Notes |
|------|-----------------------|-----------------------------------------------------------------------|---------------|-------|
| 1    | Parent / Guardian     | **Child Admitted to School:** Parent presents: Birth Certificate (Mandatory), Immunization Card (Optional), Transfer Letter (if applicable) | Physical Presence | Student accepted to school |
| 2    | School NEMIS Operator | **School Logs into NEMIS:** Operator logs into NEMIS Portal using school credentials. | NEMIS Portal  |       |
| 3    | School NEMIS Operator | **Open Learner Registration Module:** Navigates to Learner → Register Learner. | NEMIS Portal  |       |
| 4    | School NEMIS Operator | **Enter Learner Bio Data:** Inputs form fields from Birth Certificate (First Name, Middle Name, Last Name, Gender, Date of Birth, Birth Certificate Number, Nationality), Parent County, Parent Sub County, School Generated Admission Number, School Admission Date, School Class. | NEMIS Portal  |       |
| 5    | School NEMIS Operator | **Enter Parent / Guardian Details:** Inputs Father Name, Father ID Number, Mother Name, Mother ID Number, Guardian Name, Guardian ID Number, Parent Phone Number from Parent. | NEMIS Portal  |       |
| 6    | School NEMIS Operator | **Upload Supporting Documents:** Uploads Birth Certificate Copy (Mandatory), Optional: Passport Photo. | NEMIS Portal  |       |
| 7    | System Action         | **Submit Registration:** NEMIS validates Birth Certificate format.      | NEMIS System  |       |
| 8    | System Action         | **UPI Generated:** NEMIS generates Unique Personal Identifier (UPI).    | NEMIS System  | Example: UPI: 12345678901 |

### OUTPUT
**UPI Number Assigned**
Student now exists in: National Education Register

### REGISTRY DATA CREATED (AS-IS)
| Field                 |
|-----------------------|
| Learner Record        |
| UPI                   |
| Birth Certificate Number |
| Name                  |
| Gender                |
| Date of Birth         |
| Parent Details        |
| School                |
| Class                 |
| Admission Date        |

### REGISTRY DEPENDENCY (AS-IS)
**Input:** Birth Certificate Number
**Source:** Civil Registration Services

### REAL-WORLD VALIDATION (AS-IS)
Currently: Manual validation by school. No real-time CRS API integration in most cases.

### KEY OUTPUT USED BY OTHER SYSTEMS
**UPI used in:**
- Education tracking
- Capitation funding
- Exams registration (KCPE / KCSE)

### PROCESS FLOW SUMMARY (AS-IS)
Child admitted to School
↓
School logs into NEMIS
↓
Enter learner details
↓
Upload Birth Certificate
↓
Submit
↓
NEMIS generates UPI

### AS-IS PROCESS CHARACTERISTICS
| Attribute          | Status       |
|--------------------|--------------|
| Automation         | Semi-manual  |
| Initiated by       | School       |
| Identity verification | Manual       |
| Primary Key        | UPI          |
| Dependency         | Birth Certificate |

### FINAL OUTPUT OF NEMIS PROCESS
UPI Number

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

## 2. TO-BE PROCESS: Student Registration in NEMIS (Optimized)

### TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Repeatable WoG Platform / Automated).*

```mermaid
graph TD
    Start((Start)) --> T1

    subgraph Citizen_eCitizen [Citizen - eCitizen Portal]
        T1["Parental Enrollment Request<br>(Selects child & school)"]
    end

    subgraph WoG_Platform [WoG Platform - Education Service Bus]
        T2{"Validate UPI Registry<br>(Verifies identity via CRS Registry)"}
        T3{"Verify School Capacity<br>(Real-time check via Schools Registry)"}
    end

    subgraph School_Head_Teacher [School - Head Teacher Workbench]
        T4["Head Teacher Admission<br>(Digital review & one-click approval)"]
    end

    subgraph NEMIS_Backend [NEMIS Backend]
        T5["NEMIS Record Finalization<br>(Auto-enrollment & capitation trigger)"]
    end

    T1 --> T2
    T2 -- Valid --> T3
    T2 -- Invalid --> E1(Error: Invalid UPI/Parentage)
    T3 -- Capacity OK --> T4
    T3 -- No Capacity --> E2(Error: School Capacity Full)
    T4 --> T5
    T5 --> End((End))

    classDef start fill:#27ae60,stroke:#27ae60,color:#fff;
    classDef endNode fill:#e74c3c,stroke:#e74c3c,color:#fff;
    classDef userTask fill:#3498db,stroke:#2980b9,color:#fff;
    classDef serviceTask fill:#9b59b6,stroke:#8e44ad,color:#fff;
    classDef decisionGateway fill:#f39c12,stroke:#f39c12,color:#fff;
    classDef error fill:#e74c3c,stroke:#e74c3c,color:#fff;

    class Start start;
    class End endNode;
    class T1,T4 userTask;
    class T2,T3,T5 serviceTask;
    class E1,E2 error;
```

### Detailed Process (TO-BE) - Configurable & Automated
| Step | Actor / System        | Action                                                             | System Component      | Logic / Integration                                             |
|------|-----------------------|--------------------------------------------------------------------|-----------------------|-----------------------------------------------------------------|
| 1    | Parent / Guardian     | **Initiation:** Selects child (via Maisha Namba / UPI) and preferred school on eCitizen. | **eCitizen Portal**   | Uses `Maisha Namba (SSO)` for authentication.                 |
| 2    | WoG Platform (System) | **UPI Validation:** Verifies child existence and parentage records. | **CRS Registry API**  | Fetches birth details via the `Service Bus`.                    |
| 3    | WoG Platform (System) | **Capacity Check:** Validates school has space and child meets age requirements. | **National Schools Registry** | Calls `Verify School Capacity` endpoint dynamically.            |
| 4    | School Headteacher    | **Admission Review:** Approves the digital application on the workbench. | **Officer Workbench** | Validated data removes need for physical file review.             |
| 5    | NEMIS Backend (System)| **Enrollment Sync:** Finalizes record in NEMIS and triggers capitation. | **NEMIS Workflow Engine** | Auto-enrolls and calculates FDSE/FPE funds.                       |

---

## References
Derived from official mandates.


---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)
