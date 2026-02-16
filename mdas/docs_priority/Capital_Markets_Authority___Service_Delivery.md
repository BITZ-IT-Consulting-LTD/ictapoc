# Capital Markets Authority – Service Delivery

## Cover Page
- **Ministry/Department/Agency (MDA):** Capital Markets Authority
- **Process Name:** Service Delivery
- **Document Version:** 1.0
- **Date:** 2026-02-14
- **Classification:** Official

---

## Executive Summary
The Capital Markets Authority (CMA) Kenya is an independent public agency established in 1989 by the Capital Markets Act Cap 485A. Its dual mandate is to regulate and facilitate the development of orderly, fair, and efficient capital markets in Kenya. CMA's primary responsibility is to protect the interests of investors, government, employees, issuers of securities, and market intermediaries. By ensuring market integrity, transparency, and investor confidence, CMA plays a vital role in mobilizing and allocating capital resources to finance long-term productive investments for Kenya's economic growth and development.

---

## Service Mandate & Legal Basis
### Statutory Mandate
To license and supervise all capital market intermediaries, including stockbrokers, investment banks, fund managers, and collective investment schemes; to ensure the proper conduct of all licensed persons and market institutions; to regulate the issuance of capital market products, including bonds, shares, Exchange Traded Funds (ETFs), and Real Estate Investment Trusts (REITs), as well as market activities like online forex trading; to promote market development through research on new products and institutions, fostering product innovation, supporting institutional capacity development, and stimulating robust market infrastructure; to educate investors and raise public awareness to enhance financial literacy; to protect investors' interests from financial loss and ensure market integrity, including operating a compensation fund; to oversee trading activity on the Nairobi Securities Exchange (NSE) and enforce compliance with disclosure standards; to develop a framework to facilitate the use of electronic commerce for the advancement of capital markets in Kenya; and to enforce compliance with capital market laws and regulations, including imposing fines, suspending or revoking licenses, investigating complaints, and pursuing prosecution for financial misconduct.

### Legal Context
- Established by the Capital Markets Act Cap 485A Laws of Kenya in 1989 (inaugurated in 1990), which provides the comprehensive legal and regulatory framework for capital markets operations. CMA operates under the National Treasury and Planning and is crucial for implementing government financial sector policies, attracting both domestic and foreign investment, and ensuring market stability and investor confidence in line with national development agendas like Vision 2030 and financial inclusion strategies.

---

## 1. AS-IS Process Flowchart (BPMN 2.0)
*Current State visualization.*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant creates a profile on the CMA Online Port..."]
        S2["Applicant selects the license category (e.g., Inve..."]
        S3["Applicant uploads required corporate documents and..."]
        S4["Applicant pays the application fee."]
        S6["Upon approval, applicant pays the annual license f..."]
    end
    subgraph CMA [CMA]
        S5["CMA conducts fit and proper assessments of directo..."]
        S7["CMA issues the License."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> End((End))
```

---

## Process Overview
### Service Category
- G2B (Government to Business)

### Scope
- **In Scope:** End-to-end processing within Capital Markets Authority.

### Triggers
- Submission of application/request by Applicant.

### End States
- **Successful:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Stakeholders
| Stakeholder | Role | Responsibilities |
|---|---|---|
| Applicant | Process Actor | Performs actions as defined in steps. |
| CMA | Process Actor | Performs actions as defined in steps. |

---

## Inputs & Outputs
- **Inputs:** Application Form (License/Permit), Compliance Documents (Tax Compliance, CR12), Technical Reports / Site Plans, Proof of Payment
- **Outputs:** License / Permit / Certificate, Compliance Inspection Report, Official Receipt, Gazette Notice

---

## Detailed Process (AS-IS)
| Step | Role | Action | Tool | Notes |
|---|---|---|---|---|
| 1 | Applicant | Applicant creates a profile on the CMA Online Portal. | Digital | |
| 2 | Applicant | Applicant selects the license category (e.g., Investment Bank, Broker). | Manual | |
| 3 | Applicant | Applicant uploads required corporate documents and business plan. | Manual | |
| 4 | Applicant | Applicant pays the application fee. | Manual | |
| 5 | CMA | CMA conducts fit and proper assessments of directors/shareholders. | Manual | |
| 6 | Applicant | Upon approval, applicant pays the annual license fee. | Manual | |
| 7 | CMA | CMA issues the License. | Manual | |

---

## Pain Points & Opportunities
### Pain Points
- Manual document verification takes time.
- High cost and time for physical inspections.
- Risk of counterfeit licenses/certificates.
- Lack of real-time monitoring of licensees.

### Opportunities
- Integration with IPRS/BRS via Service Bus.
- Adoption of Government Payment Gateway.
- Implementation of Automated Rules Engine.
- Issuance of Digital Verifiable Credentials.

---

## 2. TO-BE Process Flowchart (BPMN 2.0)
*Future State visualization (Optimized with Service Bus & Registries).*

```mermaid
graph TD
    Start((Start)) --> S1
    subgraph Applicant [Applicant]
        S1["Applicant logs in via Single Sign-On (SSO) and sel..."]
        S4["Applicant pays fees via the Government Payment Gat..."]
    end
    subgraph System [System]
        S2["Applicant enters Business Registration Number; Sys..."]
        S3["System performs auto-validation of compliance (e.g..."]
        S5["Application is processed by the Rules Engine. (Low..."]
        S7["System generates a Verifiable Digital Certificate ..."]
    end
    subgraph Officer [Officer]
        S6["Complex cases are routed to the Officer Workbench ..."]
    end
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> S6
    S6 --> S7
    S7 --> End((End))
```

## Future State Process (TO-BE)
### Narrative
The To-Be process leverages the Government Service Bus to integrate with BRS (Business Registry) and the Payment Gateway. Manual data entry and document uploads are replaced by real-time API validations, enabling a paperless, cashless, and presence-less service experience.

### Optimized Steps (Digital)
| Step | Actor | Action | System |
|---|---|---|---|
| 1 | Applicant | Applicant logs in via Single Sign-On (SSO) and selects the service. | Citizen Portal / SSO |
| 2 | System | Applicant enters Business Registration Number; System auto-populates details from BRS (Business Registry) via the Service Bus. | Service Bus / Registry API |
| 3 | System | System performs auto-validation of compliance (e.g., KRA Tax Status) via Inter-Agency APIs. | Service Bus / Compliance Engine |
| 4 | Applicant | Applicant pays fees via the Government Payment Gateway; System auto-receipts. | Payment Gateway |
| 5 | System | Application is processed by the Rules Engine. (Low-risk cases are Auto-Approved). | Workflow Engine |
| 6 | Officer | Complex cases are routed to the Officer Workbench for digital review and approval. | Officer Workbench |
| 7 | System | System generates a Verifiable Digital Certificate (QR Code) and notifies the applicant. | Output Generator |

---

## References & Evidence
The information in this document was derived from the following official sources:

- [https://www.cmarcp.or.ke/](https://www.cmarcp.or.ke/)
- [https://policyvault.africa/](https://policyvault.africa/)
- [https://infoshop.org/](https://infoshop.org/)
- [https://wikipedia.org/](https://wikipedia.org/)
- [https://saraka.info/](https://saraka.info/)
- [https://serrarigroup.com/](https://serrarigroup.com/)
- [https://thekenyatimes.com/](https://thekenyatimes.com/)
- [https://youtube.com/](https://youtube.com/)
- [https://payatlas.com/](https://payatlas.com/)
