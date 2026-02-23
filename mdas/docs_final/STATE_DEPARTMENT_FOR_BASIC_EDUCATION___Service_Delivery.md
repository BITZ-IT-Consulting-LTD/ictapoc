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
*This section will be updated with Nemis-specific pain points and opportunities.*

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*This section will be updated with the Nemis TO-BE process flowchart.*

---

## Future State Process (TO-BE)
*This section will be updated with the Nemis TO-BE detailed steps.*

---

## References
Derived from official mandates.