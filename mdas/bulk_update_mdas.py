import json
import sys

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

updates = {
    "KENYA REVENUE AUTHORITY": {
        "narrative": "The tax return filing process is fully digitized via the iTax portal, allowing taxpayers to file returns and pay taxes online without visiting KRA offices. (Updated with standard iTax workflow).",
        "steps": [
            {"step_number": 1, "description": "Taxpayer logs into the KRA iTax portal (itax.kra.go.ke) using PIN and password.", "actor": "Taxpayer"},
            {"step_number": 2, "description": "Taxpayer selects 'Returns' menu and chooses 'File Return' or 'File Nil Return'.", "actor": "Taxpayer"},
            {"step_number": 3, "description": "Taxpayer selects the tax obligation (e.g., Income Tax Resident) and period.", "actor": "Taxpayer"},
            {"step_number": 4, "description": "Taxpayer downloads the Excel/ODS return form (or uses the web-based form for simple returns).", "actor": "Taxpayer"},
            {"step_number": 5, "description": "Taxpayer fills the return form offline and uploads the generated ZIP file back to the portal.", "actor": "Taxpayer"},
            {"step_number": 6, "description": "System validates the return and generates an E-Return Acknowledgement Receipt.", "actor": "System"},
            {"step_number": 7, "description": "Taxpayer downloads and prints the Acknowledgement Receipt.", "actor": "Taxpayer"}
        ]
    },
    "TRANSPORT AND SAFETY": {
        "narrative": "Driving license renewal is a self-service process on the NTSA/eCitizen portal, integrated with mobile payment. (Updated with standard NTSA workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant logs into the NTSA/eCitizen portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant selects 'Driving License Renewal' service.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant chooses the renewal period (1 year or 3 years).", "actor": "Applicant"},
            {"step_number": 4, "description": "Applicant pays the renewal fee via M-Pesa or Card.", "actor": "Applicant"},
            {"step_number": 5, "description": "System generates a renewal slip (for Smart DL) or updates the record.", "actor": "System"},
            {"step_number": 6, "description": "Applicant collects the Smart DL from the selected center (if applying for a card) or prints the renewal slip.", "actor": "Applicant"}
        ]
    },
    "BUSINESS REGISTRATION": {
        "narrative": "Business Name registration is fully online via the eCitizen BRS portal, covering name search, reservation, and registration. (Updated with standard BRS workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant logs into the eCitizen BRS portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant conducts a Business Name Search and reserves a name.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant selects 'Business Name Registration' (BN2) once the name is approved.", "actor": "Applicant"},
            {"step_number": 4, "description": "Applicant fills the online form (nature of business, address, partners' details).", "actor": "Applicant"},
            {"step_number": 5, "description": "Applicant uploads scanned IDs and passport photos of partners.", "actor": "Applicant"},
            {"step_number": 6, "description": "Applicant pays the registration fee via M-Pesa.", "actor": "Applicant"},
            {"step_number": 7, "description": "Registrar reviews and approves the application.", "actor": "Registrar of Companies"},
            {"step_number": 8, "description": "Applicant downloads the Certificate of Registration.", "actor": "Applicant"}
        ]
    },
    "POLICE SERVICE": {
        "narrative": "The Police Clearance Certificate (Good Conduct) process involves online application and payment via eCitizen, followed by physical biometrics capture. (Updated with standard DCI workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant logs into the eCitizen portal and selects Directorate of Criminal Investigations (DCI).", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant selects 'Police Clearance Certificate' application.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant pays the processing fee via M-Pesa.", "actor": "Applicant"},
            {"step_number": 4, "description": "Applicant downloads and prints the C24 Fingerprint Form and receipt.", "actor": "Applicant"},
            {"step_number": 5, "description": "Applicant physically visits DCI Headquarters or a Huduma Center for fingerprint recording.", "actor": "Applicant"},
            {"step_number": 6, "description": "DCI officer records fingerprints and processes the check.", "actor": "DCI Officer"},
            {"step_number": 7, "description": "Applicant receives notification and downloads the certificate from eCitizen.", "actor": "Applicant"}
        ]
    },
    "LANDS": {
        "narrative": "Land searches and transactions are conducted via the Ardhisasa platform for Nairobi properties, with manual processes transitioning elsewhere. (Updated with standard Ardhisasa workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant logs into the Ardhisasa platform (ardhisasa.lands.go.ke).", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant selects 'Search' under Land Administration.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant enters the Parcel Number and uploads ID/Consent if required.", "actor": "Applicant"},
            {"step_number": 4, "description": "Applicant pays the search fee via M-Pesa.", "actor": "Applicant"},
            {"step_number": 5, "description": "System generates the Search Certificate showing ownership and encumbrances.", "actor": "System"},
            {"step_number": 6, "description": "Applicant downloads and prints the Official Search Result.", "actor": "Applicant"}
        ]
    },
    "HIGHER EDUCATION LOANS": {
        "narrative": "HELB loan application is a hybrid process involving online form filling on the HELB portal and submission of signed physical forms. (Updated with standard HELB workflow).",
        "steps": [
            {"step_number": 1, "description": "Student registers/logs into the HELB Student Portal.", "actor": "Student"},
            {"step_number": 2, "description": "Student selects the appropriate Loan Product (e.g., Undergraduate First Time).", "actor": "Student"},
            {"step_number": 3, "description": "Student fills the detailed financial and personal background form online.", "actor": "Student"},
            {"step_number": 4, "description": "Student prints the filled form.", "actor": "Student"},
            {"step_number": 5, "description": "Student has the form signed by guarantors, a lawyer/magistrate, and the local Chief.", "actor": "Student"},
            {"step_number": 6, "description": "Student drops the physical form at a Huduma Center or Bank.", "actor": "Student"},
            {"step_number": 7, "description": "HELB processes the loan and disburses funds to the university/student.", "actor": "HELB"}
        ]
    },
    "POWER AND LIGHTING": {
        "narrative": "New power connection involves application, site survey, quotation payment, and physical installation. (Updated with standard KPLC workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant applies for new supply via eCitizen, KPLC Self Service Portal, or physically.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant submits ID, PIN, and Wiring Certificates.", "actor": "Applicant"},
            {"step_number": 3, "description": "KPLC staff visits the site for survey and estimation.", "actor": "KPLC Staff"},
            {"step_number": 4, "description": "KPLC issues a Quotation for the connection costs.", "actor": "KPLC"},
            {"step_number": 5, "description": "Applicant pays the quotation amount.", "actor": "Applicant"},
            {"step_number": 6, "description": "KPLC installs the meter and connects power.", "actor": "KPLC Staff"}
        ]
    },
    "ENVIRONMENT MANAGEMENT": {
        "narrative": "EIA Licensing involves submission of project reports, fee payment, review, and licensing. (Updated with standard NEMA workflow).",
        "steps": [
            {"step_number": 1, "description": "Proponent submits a Project Report (via a registered expert) to NEMA.", "actor": "Proponent/Expert"},
            {"step_number": 2, "description": "Proponent pays the EIA processing fee (0.1% of project cost).", "actor": "Proponent"},
            {"step_number": 3, "description": "NEMA reviews the report and may conduct site visits or public participation.", "actor": "NEMA"},
            {"step_number": 4, "description": "NEMA issues Approval conditions.", "actor": "NEMA"},
            {"step_number": 5, "description": "Proponent accepts conditions.", "actor": "Proponent"},
            {"step_number": 6, "description": "NEMA issues the EIA License.", "actor": "NEMA"}
        ]
    },
    "HOSPITAL INSURANCE": {
        "narrative": "NHIF (SHA) registration involves submitting personal details to receive a membership number/card. (Updated with standard NHIF workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant visits NHIF portal, Huduma Center, or uses USSD code.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant fills the registration form with ID and dependent details.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant attaches/uploads ID copy and passport photo.", "actor": "Applicant"},
            {"step_number": 4, "description": "System/Officer registers the member and issues a Membership Number.", "actor": "System/Officer"},
            {"step_number": 5, "description": "Applicant receives NHIF Card (or virtual confirmation).", "actor": "Applicant"}
        ]
    },
    "SOCIAL SECURITY FUND": {
        "narrative": "NSSF registration is instant via the self-service portal or USSD. (Updated with standard NSSF workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant accesses NSSF Self Service Portal or USSD.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant enters National ID/Alien ID number and details.", "actor": "Applicant"},
            {"step_number": 3, "description": "System validates details from IPRS.", "actor": "System"},
            {"step_number": 4, "description": "System generates NSSF Number immediately.", "actor": "System"},
            {"step_number": 5, "description": "Applicant prints the NSSF card/membership details.", "actor": "Applicant"}
        ]
    },
    "BUREAU OF STANDARDS": {
        "narrative": "Product certification involves application, payment, inspection, testing, and issuance of the permit. (Updated with standard KEBS workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant applies for Standardization Mark via KEBS IMS portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant pays the certification fees.", "actor": "Applicant"},
            {"step_number": 3, "description": "KEBS officers visit the factory for inspection and sample collection.", "actor": "KEBS Officer"},
            {"step_number": 4, "description": "Samples are tested in KEBS laboratories.", "actor": "KEBS Lab"},
            {"step_number": 5, "description": "Upon passing tests, the Standardization Mark Permit is issued.", "actor": "KEBS"}
        ]
    },
    "IMMIGRATION": {
        "narrative": "The passport application process is largely digitized via the eCitizen platform for submission and payment, but requires physical presence for biometric capture and collection. (Updated with specific e-Passport workflow steps).",
        "steps": [
            {"step_number": 1, "description": "Applicant logs into the eCitizen portal and navigates to Immigration Services.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant fills the online passport application form.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant uploads scanned copies of ID, Birth Certificate, etc.", "actor": "Applicant"},
            {"step_number": 4, "description": "Applicant pays the fee via M-Pesa.", "actor": "Applicant"},
            {"step_number": 5, "description": "Applicant downloads application form and receipt.", "actor": "Applicant"},
            {"step_number": 6, "description": "Applicant books appointment for biometrics.", "actor": "Applicant"},
            {"step_number": 7, "description": "Applicant visits Immigration Center for biometrics.", "actor": "Applicant"},
            {"step_number": 8, "description": "Passport is processed and printed.", "actor": "Immigration"},
            {"step_number": 9, "description": "Applicant collects passport.", "actor": "Applicant"}
        ]
    }
}

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    count = 0
    updated_names = []

    for item in items:
        mda_name = item.get('mda_name', '').upper()
        if not mda_name:
            continue
            
        for key in updates:
            if key in mda_name:
                item['as_is_steps'] = updates[key]['steps']
                item['as_is_narrative'] = updates[key]['narrative']
                # Mark as documented
                if 'process_maturity' not in item:
                    item['process_maturity'] = {}
                item['process_maturity']['documentation_status'] = 'Documented (Inferred Standard Process)'
                
                updated_names.append(item.get('mda_name'))
                count += 1
                break # Stop checking keys for this item once matched

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {count} MDAs.")
    for name in updated_names:
        print(f"- {name}")

except Exception as e:
    print(f"Error: {e}")
