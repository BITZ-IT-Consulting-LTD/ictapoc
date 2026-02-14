# Anti-Counterfeit Authority – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Anti-Counterfeit Authority
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Anti-Counterfeit Authority (ACA) Kenya is a State Corporation established under the Anti-Counterfeit Act 2008. Its primary mandate is to protect intellectual property rights and consumer rights by actively combating trade in counterfeit goods, raising public awareness, and coordinating with other organizations involved in anti-counterfeiting efforts in Kenya.

---

## Process Flowchart (BPMN 2.0 - Mermaid)
*Guidance: This diagram visualizes the process flow across different actors (Swimlanes).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph BrandOwner [Brand Owner]
        S1["IP Right owner logs into the ACA AIMS portal."]
        S2["Applicant submits application for IPR Recordal (Fo..."]
        S3["Applicant uploads image of genuine product and tra..."]
        S4["Applicant pays the recordal fee."]
    end
    subgraph ACA [ACA]
        S5["ACA approves and issues the IPR Recordal Certifica..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> End((End))
```

---

## Process Overview
### Process Name
Service Delivery

### Service Category
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within Anti-Counterfeit Authority.

### Triggers
- Submission of application/request by Brand Owner.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| ACA | Process Actor | Performs actions as defined in steps. |
| Brand Owner | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Brand Owner | IP Right owner logs into the ACA AIMS portal. | Digital | |
| 2 | Brand Owner | Applicant submits application for IPR Recordal (Form ACA 1). | Manual | |
| 3 | Brand Owner | Applicant uploads image of genuine product and trademark certs. | Manual | |
| 4 | Brand Owner | Applicant pays the recordal fee. | Manual | |
| 5 | ACA | ACA approves and issues the IPR Recordal Certificate. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Manual document verification takes time.
- High cost and time for physical inspections.
- Risk of counterfeit licenses/certificates.
- Lack of real-time monitoring of licensees.

### Opportunities
- Online Licensing Management System (LMS).
- Integration with IPRS and BRS for auto-verification.
- Mobile field inspection apps with GIS.
- QR-coded verifiable certificates.

---

## KPIs
| KPI | Baseline | Target |
|---|---|---|
| Turnaround Time | 30 Days | 5 Days |
| CSAT | 50% | 90% |
