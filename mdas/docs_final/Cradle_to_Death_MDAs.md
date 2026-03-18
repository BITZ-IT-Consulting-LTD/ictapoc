# Cradle to Death: Government Service Delivery Lifecycle

This document provides a detailed mapping of the key Ministries, Departments, and Agencies (MDAs) involved in a citizen's lifecycle. It outlines the specific services and processes delivered at each stage, from birth ("The Cradle") to estate administration ("The Death").

---

## 1. The Cradle (Birth & Identity)
**Objective:** Establish legal existence, foundational identity, and basic social protections.

*   **Civil Registration Services (CRS)**
    *   *File:* [`_CIVIL_REGISTRATION_SERVICES_CRS____Service_Delivery.md`](./_CIVIL_REGISTRATION_SERVICES_CRS____Service_Delivery.md)
    *   *Processes:*
        *   **Birth Registration:** Registration of a child's birth at a hospital or via an administrative Chief, leading to the creation of a digital identity and generation of a Unique Personal Identifier (Maisha Namba / UPI).
        *   **Death Registration:** Processing death notifications, auto-updating population registries, and issuing burial permits and Death Certificates.
*   **Ministry of Health**
    *   *File:* [`Ministry_of_Health___Service_Delivery.md`](./Ministry_of_Health___Service_Delivery.md)
    *   *Processes:*
        *   **Service Delivery (Health Notification):** Notification of birth and death occurrences directly from health facilities to the civil registration databases.
*   **Integrated Population Registration System (IPRS)**
    *   *File:* [`_INTEGRATED_POPULATION_REGISTRATION_SYSTEM___Service_Delivery.md`](./_INTEGRATED_POPULATION_REGISTRATION_SYSTEM___Service_Delivery.md)
    *   *Processes:*
        *   **IPRS Identity Registration and Verification:** Acting as the "Single Source of Truth" that consolidates civil data to instantly verify citizen identities for all other MDAs (e.g., KRA, NTSA).
        *   **IPRS Record Update:** Real-time updating of population records based on life events, broadcasting status changes across the government event bus.
*   **Social Health Authority (SHA) / National Health Insurance Fund (NHIF)**
    *   *File:* [`National_Health_Insurance_Fund___Service_Delivery.md`](./National_Health_Insurance_Fund___Service_Delivery.md)
    *   *Processes:*
        *   **Automated SHA Registration and Assessment:** Event-driven enrollment into the Social Health Authority for medical cover, incorporating automatic dependency linking and intelligent means testing for contributions.

## 2. Childhood & Education
**Objective:** Facilitate learning, development, and academic progression through structured systems.

*   **Ministry of Education**
    *   *File:* [`Ministry_of_Education___Service_Delivery.md`](./Ministry_of_Education___Service_Delivery.md)
    *   *Processes:*
        *   **Student Registration & Transition (NEMIS):** Tracking student enrollment and transition through basic education using the National Education Management Information System.
*   **National Schools Registry**
    *   *Role:* The authoritative database for all accredited basic education institutions, used for school selection and geo-spatial mapping. *(System database, no direct citizen application process).*
*   **Kenya National Examinations Council (KNEC)**
    *   *File:* [`Kenya_National_Examinations_Council___Service_Delivery.md`](./Kenya_National_Examinations_Council___Service_Delivery.md)
    *   *Processes:*
        *   **Service Delivery (Exam Administration):** Administration of national examinations (like KPSEA and KCSE) and the secure issuance of academic certificates.
*   **Kenya Universities and Colleges Central Placement Service (KUCCPS)**
    *   *File:* [`Kenya_Universities_And_Colleges_Central_Placement_Service___Student_Admission.md`](./Kenya_Universities_And_Colleges_Central_Placement_Service___Student_Admission.md)
    *   *Processes:*
        *   **Student Admission:** Centralized, merit-based placement of students into public and private universities, colleges, and TVETs.
*   **Higher Education Loans Board (HELB)**
    *   *File:* [`Higher_Education_Loans_Board___Loan_Processing.md`](./Higher_Education_Loans_Board___Loan_Processing.md)
    *   *Processes:*
        *   **Loan Processing:** Receiving applications, conducting means testing, and disbursing higher education loans and bursaries to support students.

## 3. Coming of Age (Adulthood & Citizenship)
**Objective:** Transition to legal adulthood, rights, privileges, and responsibilities.

*   **National Registration Bureau (NRB)**
    *   *File:* [`_NATIONAL_REGISTRATION_BUREAU_NRB____Service_Delivery.md`](./_NATIONAL_REGISTRATION_BUREAU_NRB____Service_Delivery.md)
    *   *Processes:*
        *   **National Identity Card Registration:** The foundational transition to adulthood via the biometric registration and issuance of the National Identity Card (Maisha Card) at age 18.
*   **State Department for Immigration & Citizen Services**
    *   *File:* [`STATE_DEPARTMENT_FOR_IMMIGRATION_AND_CITIZEN_SERVICES___Passport_Application.md`](./STATE_DEPARTMENT_FOR_IMMIGRATION_AND_CITIZEN_SERVICES___Passport_Application.md)
    *   *Processes:*
        *   **Passport Application & Issuance:** Processing biometric applications and issuing passports and other travel documents to enable international mobility.
*   **National Transport and Safety Authority (NTSA)**
    *   *File:* [`NATIONAL_TRANSPORT_AND_SAFETY_AUTHORITY_NTSA____Driving_License_Renewal.md`](./NATIONAL_TRANSPORT_AND_SAFETY_AUTHORITY_NTSA____Driving_License_Renewal.md)
    *   *Processes:*
        *   **Driving License Renewal:** The process of validating a driver's credentials, processing fee payments, and renewing smart driving licenses via the TIMS/eCitizen portal.

## 4. Economic Life (Employment & Business)
**Objective:** Enable participation in the formal economy, taxation, and long-term social security.

*   **Kenya Revenue Authority (KRA)**
    *   *File:* [`Kenya_Revenue_Authority___Tax_Return_Filing.md`](./Kenya_Revenue_Authority___Tax_Return_Filing.md)
    *   *Processes:*
        *   **Tax Return Filing (and PIN Registration):** Enrollment of citizens and businesses into the tax system (KRA PIN) and the processing of periodic tax returns to ensure national compliance.
*   **Business Registration Service (BRS)**
    *   *File:* [`Business_Registration_Service___Service_Delivery.md`](./Business_Registration_Service___Service_Delivery.md)
    *   *Processes:*
        *   **Business Name & Company Registration:** Formalizing economic participation by legally registering business names, private limited companies, and partnerships.
*   **National Social Security Fund (NSSF)**
    *   *File:* [`National_Social_Security_Fund___Service_Delivery.md`](./National_Social_Security_Fund___Service_Delivery.md)
    *   *Processes:*
        *   **Automated NSSF Registration and Contribution:** Mandatory and event-driven enrollment for retirement savings when a citizen begins formal or informal employment, tracking monthly contributions.

## 5. Family & Property
**Objective:** Formalizing family units, managing legal affairs, and establishing secure property ownership.

*   **State Law Office (Attorney General)**
    *   *File:* [`State_Law_Office_The___Service_Delivery.md`](./State_Law_Office_The___Service_Delivery.md)
    *   *Processes:*
        *   **Marriage Registration:** Processing notices of marriage, running bigamy checks, officiating ceremonies, and issuing secure Marriage Certificates.
        *   **Societies Registration:** The legal registration and regulation of associations, societies, and religious organizations.
*   **Ministry of Lands (State Department for Lands and Physical Planning)**
    *   *File:* [`STATE_DEPARTMENT_FOR_LANDS_AND_PHYSICAL_PLANNING___Service_Delivery.md`](./STATE_DEPARTMENT_FOR_LANDS_AND_PHYSICAL_PLANNING___Service_Delivery.md)
    *   *Processes:*
        *   **Land Registration / Title Deed Issuance:** Validating land ownership and issuing secure, verifiable Title Deeds via the Ardhisasa platform.
        *   **Property Transfer (Change of Ownership):** Facilitating the transfer of property, incorporating biometric consent, encumbrance checks, and stamp duty payments.

## 6. The Death (End of Life & Succession)
**Objective:** Closing the citizen lifecycle legally, administering succession, and reunifying assets.

*   **The Judiciary**
    *   *File:* [`THE_JUDICIARY___Service_Delivery.md`](./THE_JUDICIARY___Service_Delivery.md)
    *   *Processes:*
        *   **Succession & Probate Administration:** The legal process of filing succession cases, validating wills, publishing gazette notices, and issuing Grants of Probate or Administration to distribute a deceased person's estate.
*   **Unclaimed Financial Assets Authority (UFAA)**
    *   *File:* [`Unclaimed_Financial_Assets_Authority___Service_Delivery.md`](./Unclaimed_Financial_Assets_Authority___Service_Delivery.md)
    *   *Processes:*
        *   **Claim for Unclaimed Financial Assets:** Discovering dormant financial assets (bank accounts, shares) and processing claims to reunify these assets with the legal beneficiaries or administrators.
*   **Public Trustee (under Office of the Attorney General)**
    *   *File:* [`OFFICE_OF_THE_ATTORNEY_GENERAL_AG____Service_Delivery.md`](./OFFICE_OF_THE_ATTORNEY_GENERAL_AG____Service_Delivery.md)
    *   *Processes:*
        *   **Public Trustee Estate Administration:** Providing impartial administration for estates of citizens who die without a will (intestate), identifying assets, settling debts, and distributing the remainder to lawful heirs.

---

### Validation Survey
Please provide your feedback here: [https://ee.kobotoolbox.org/x/4Ls7SlCG](https://ee.kobotoolbox.org/x/4Ls7SlCG)
