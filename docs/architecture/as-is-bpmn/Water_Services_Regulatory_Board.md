# STANDARD BPM TEMPLATE – APPLICABLE TO ALL MDAs

---

## Cover Page

*Guidance: This page should contain the official name of the Ministry, Department, or Agency (MDA), the process name, the document version, and the date of publication. It serves as the formal cover for the document.*

- **Ministry/Department/Agency (MDA):** Water Services Regulatory Board
- **Process Name:** [Enter Full Process Name]
- **Document Version:** [e.g., 1.0]
- **Date:** [YYYY-MM-DD]
- **Classification:** [e.g., Official, Sensitive, For Internal Use Only]

---

## Document Control & Version History

*Guidance: This section tracks the evolution of the document. It is critical for audit and change management purposes. Log every change, including the date, version number, a description of the change, and the name of the author/editor.*

| Version | Date       | Author(s)     | Change Description                                       |
|---------|------------|---------------|----------------------------------------------------------|
| 0.1     | YYYY-MM-DD | [Author Name] | Initial Draft                                            |
| 1.0     | YYYY-MM-DD | [Author Name] | First official release after review                      |
| ...     | ...        | ...           | ...                                                      |

---

## Executive Summary

*Guidance: Provide a high-level overview of the entire document. This should be a self-contained summary for senior leadership. It should briefly describe the process, the key findings from the AS-IS analysis (including major pain points), and the core recommendations for the TO-BE future state, highlighting the expected benefits of digitization and automation.*

---

## Process Overview

### Process Name
*Guidance: State the official, unambiguous name of the business process.*
- [e.g., Application for a Business Operating Permit]

### Service Category
*Guidance: Classify the service (e.g., G2C - Government to Citizen, G2B - Government to Business, G2G - Government to Government).*
- [e.g., G2B]

### Process Objective
*Guidance: Clearly and concisely state what this process is intended to achieve. What is its primary purpose and value?*
- [e.g., To review, approve, and issue a Business Operating Permit to eligible enterprises in compliance with the Business Act of 2024.]

### Scope (In Scope / Out of Scope)
*Guidance: Define the boundaries of the process. What activities are included (In Scope)? What related activities are explicitly excluded (Out of Scope)? This prevents ambiguity.*
- **In Scope:** [List all activities, departments, and systems that are part of this process.]
- **Out of Scope:** [List related but separate activities, departments, and systems.]

### Triggers
*Guidance: What event(s) initiate this process?*
- [e.g., Submission of a completed application form by a citizen/business.]

### End States
*Guidance: What are the possible successful and unsuccessful conclusions of this process?*
- **Successful End State(s):** [e.g., Permit issued and dispatched to the applicant.]
- **Unsuccessful End State(s):** [e.g., Application rejected and notification sent to the applicant.]

### Policy, Legal & Regulatory Context
*Guidance: List all relevant laws, acts of parliament, regulations, official circulars, and internal policies that govern this process. This is crucial for compliance.*
- [e.g., The National Business Registration Act, 2024; The Data Protection Act, 2019; MDA Service Charter.]

---
### Services Offered

*Guidance: This section details the specific services provided by Water Services Regulatory Board.*

#### Licensing of Water Service Providers (WAT-WSB-001)
- **Service Type:** B2G
- **Category:** Regulatory
- **Delivery Channel:** Online
- **Platform:** WASREB Portal
- **Legal Framework:** Water Act
- **Notes:** Utilities licensing

#### Approval of Water Tariffs (WAT-WSB-002)
- **Service Type:** B2G
- **Category:** Regulatory
- **Delivery Channel:** Internal
- **Platform:** WASREB Systems
- **Legal Framework:** Water Act
- **Notes:** Tariff setting

#### Service Provision Performance Monitoring (WAT-WSB-003)
- **Service Type:** G2G
- **Category:** Administrative
- **Delivery Channel:** Internal
- **Platform:** WASREB Systems
- **Legal Framework:** Water Act
- **Notes:** Utility oversight




## Stakeholders, Roles & Responsibilities

*Guidance: Identify all individuals, groups, or systems involved in the process. Define their specific roles and responsibilities in a clear table format.*

| Stakeholder | Role             | Responsibilities                                                              |
|-------------|------------------|-------------------------------------------------------------------------------|
| Citizen     | Applicant        | Submits application, provides required documents, pays fees.                  |
| Officer A   | Front Desk Officer | Receives and verifies application for completeness.                           |
| System X    | Payment Gateway  | Processes fee payments.                                                       |
| Officer B   | Review Officer   | Conducts substantive review of the application against policy criteria.     |
| Director    | Approver         | Makes the final decision to approve or reject the application.                |

---

## Inputs, Outputs & External Dependencies

*Guidance: Detail what is required to start the process and what is produced at the end. Also, note any dependencies on external entities not directly involved in the process.*

- **Inputs:** [e.g., Completed Application Form (Form-A), Certificate of Incorporation, Tax Compliance Certificate.]
- **Outputs:** [e.g., Official Business Operating Permit, Rejection Letter, Payment Receipt.]
- **External Dependencies:** [e.g., Verification of Tax Compliance with the National Revenue Authority.]

---

## Process Maturity Assessment

### Existing Workflow: Yes / Partial / No
*Guidance: State the condition of the existing workflow documentation based on initial assessment. Select one.*
- [e.g., Partial]
- *(Note: If 'Partial', describe what exists and what is missing. If 'No', state that the following AS-IS process is a constructed baseline.)*

### Documentation Status
*Guidance: Describe the state and quality of any existing documentation (e.g., formal documented procedures, informal notes, outdated guides, non-existent).*

### Level of Automation
*Guidance: Describe the current role of technology in the process (e.g., Fully Manual, Semi-Automated with some systems like email, Fully Digital).*

---

## High-Level Process Narrative (AS-IS)

*Guidance: Write a brief, paragraph-style story of how the process works from start to finish. This narrative should be easy for anyone to understand without getting into technical details.*

---

## Detailed Step-by-Step Process (AS-IS)

*Guidance: This is the core of the AS-IS analysis. Document each step in a structured table. Assign a step number, identify the responsible role, provide a clear description of the action, and note the average time taken if known. Flag any steps that are assumed.*

| Step | Role               | Action Description                                                                   | System/Tool Used | Time (Avg) | Notes                                           |
|------|--------------------|--------------------------------------------------------------------------------------|------------------|------------|-------------------------------------------------|
| 1    | Citizen (Applicant)| Downloads application form from the MDA website.                                       | Website          | 10 mins    |                                                 |
| 2    | Citizen (Applicant)| Fills form manually and gathers required supporting documents.                         | Manual           | 3 hours    |                                                 |
| 3    | Citizen (Applicant)| Submits physical documents at the MDA front desk.                                    | Manual           | 1 hour     |                                                 |
| 4    | Front Desk Officer | Receives documents, performs a completeness check against a physical checklist.        | Manual           | 15 mins    | *Assumed based on standard government practice.*    |
| ...  | ...                | ...                                                                                  | ...              | ...        |                                                 |

---

## Decision Points & Business Rules

*Guidance: Identify all points in the process where a decision is made. Document the rules that govern these decisions in a `IF-THEN-ELSE` format.*

| Decision Point ID | Step | Decision Required                                  | Business Rule(s)                                                                    |
|-------------------|------|----------------------------------------------------|-------------------------------------------------------------------------------------|
| DP-01             | 4    | Is the application package complete?               | **IF** all required documents are present, **THEN** proceed to Step 5 (Logging). **ELSE** return to Applicant with a deficiency note. |
| DP-02             | 7    | Does the application meet regulatory criteria?     | **IF** criteria are met, **THEN** forward to Director for approval. **ELSE** draft rejection letter. |

---

## Exceptions & Alternate Scenarios

*Guidance: Document what happens when things go wrong or deviate from the main path. How are errors handled?*

| Exception ID | Triggering Condition                               | Handling Procedure                                                                  |
|--------------|----------------------------------------------------|-------------------------------------------------------------------------------------|
| E-01         | System X (Payment Gateway) is offline.             | Front Desk Officer advises applicant to pay via the designated bank account and present the deposit slip. |
| E-02         | Applicant submits an expired supporting document.  | Process is paused. An official notification is sent to the applicant with a 14-day compliance window. |

---

## Pain Points, Bottlenecks & Risks

*Guidance: Based on the AS-IS analysis, identify key problems. Link them to specific process steps where possible.*

| ID   | Type (Pain Point/Bottleneck/Risk) | Description                                                               | Impacted Step(s) |
|------|-----------------------------------|---------------------------------------------------------------------------|------------------|
| PP-01| Pain Point                        | Applicant must travel physically to submit the application.               | 3                |
| BN-01| Bottleneck                        | All applications must be approved by a single Director, causing delays.   | 8                |
| R-01 | Risk                              | Loss of physical documents during inter-office transit.                   | 6, 7             |

---

## Future State Process (TO-BE)

*Guidance: Describe the vision for the redesigned, optimized, and digitized process. This should be a high-level narrative explaining how the new process will work and feel for the stakeholders, especially the citizen.*

---

## Digitization, Automation & Integration Opportunities

*Guidance: Propose specific, actionable improvements in a table. Link them to the pain points identified earlier. This section forms the basis for technical requirements.*

| Opportunity ID | Pain Point ID | Proposed Solution                                                                    | Type (Digitization/Automation/Integration) | Expected Benefit                                          |
|----------------|---------------|--------------------------------------------------------------------------------------|--------------------------------------------|-----------------------------------------------------------|
| OPT-01         | PP-01         | Develop an online portal for application submission and document upload.             | Digitization                               | Eliminates physical travel for applicants; 24/7 access.   |
| OPT-02         | BN-01         | Implement a rule-based engine to auto-approve standard applications based on pre-defined criteria. Implement delegated authority for others. | Automation                                 | Reduces Director's workload; speeds up approval times.    |
| OPT-03         | R-01, E-01    | Integrate the portal with the National Revenue Authority for real-time tax compliance checks and with the payment gateway. | Integration                                | Reduces fraud, eliminates manual verification, seamless payments. |

---

## KPIs & Performance Indicators

*Guidance: Define measurable metrics to track the performance of both the AS-IS and TO-BE processes. This demonstrates the value of the transformation.*

| KPI ID | Metric                                  | AS-IS Baseline | TO-BE Target |
|--------|-----------------------------------------|----------------|--------------|
| KPI-01 | Average End-to-End Processing Time      | 15 Business Days | 3 Business Days |
| KPI-02 | Cost Per Transaction                    | [e.g., KES 500]  | [e.g., KES 50]  |
| KPI-03 | Citizen Satisfaction Score (CSAT)       | 40%              | 90%            |
| KPI-04 | First-Time-Right Application Percentage | 60%              | 95%            |

---

## Change Impact Assessment

*Guidance: Analyze the impact of moving from AS-IS to TO-BE on people, processes, and technology.*

- **People:** [e.g., Need for training on the new digital system for all officers. Potential role changes for Front Desk staff.]
- **Process:** [e.g., Elimination of manual data entry steps. Introduction of a new digital review workflow.]
- **Technology:** [e.g., Requirement to procure/develop a new portal. Need for integration APIs.]
- **Policy:** [e.g., Policy amendment required to recognize digital signatures and submissions as legally valid.]

---

## Assumptions, Gaps & Open Issues

*Guidance: List all assumptions made during the analysis, any information that was not available (gaps), and questions that need to be answered by the MDA to finalize the BPM.*

- **Assumptions:** [e.g., Assumed that all officers have access to a computer and reliable internet.]
- **Gaps:** [e.g., Data on the volume of applications per month was not available.]
- **Open Issues:** [e.g., Who will be the designated data steward for the new digital system?]

---

## Appendices

*Guidance: Include supplementary materials that are too detailed for the main body of the document.*
- [e.g., Process Flowcharts (AS-IS and TO-BE), System Architecture Diagrams, detailed data models.]

---

## Glossary

*Guidance: Define any acronyms, jargon, or technical terms used in the document to ensure a common understanding.*

| Term/Acronym | Definition                                                 |
|--------------|------------------------------------------------------------|
| AS-IS        | The current state of the business process.                 |
| TO-BE        | The future, desired state of the business process.         |
| G2C          | Government-to-Citizen.                                     |
| KPI          | Key Performance Indicator.                                 |

---

## Data Elements / Forms

*Guidance: List and describe all data fields collected during the process. This is critical for database design and form creation. If existing forms are used, they can be attached here.*

| Form Name/ID      | Data Element       | Data Type (e.g., Text, Number, Date) | Is it PII? (Personally Identifiable Information) |
|-------------------|--------------------|--------------------------------------|--------------------------------------------------|
| Form-A            | Business Name      | Text                                 | No                                               |
| Form-A            | Director's ID No.  | Text                                 | Yes                                              |
| ...               | ...                | ...                                  | ...                                              |
