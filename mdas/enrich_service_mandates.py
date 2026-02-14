import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

# --- 1. Define Mandate Profiles (Archetypes) ---

profiles = {
    "EDUCATION": {
        "keywords": ["UNIVERSITY", "COLLEGE", "POLYTECHNIC", "INSTITUTE", "SCHOOL", "ACADEMY", "KMTC", "KAIST"],
        "data": {
            "inputs": [
                "KCSE/Academic Result Slips",
                "National ID / Birth Certificate",
                "Student Personal Details Form",
                "Fee Payment Receipts"
            ],
            "outputs": [
                "Admission Letter",
                "Student ID Card",
                "Academic Transcripts",
                "Degree/Diploma Certificate"
            ],
            "pain_points": [
                "Long queues during admission and registration.",
                "Manual reconciliation of fee payments.",
                "Delays in processing exam results and transcripts.",
                "Fragmented student data across departments."
            ],
            "digitization_opportunities": [
                "Biometric student registration and attendance.",
                "Integrated ERP for end-to-end student lifecycle management.",
                "Smart Campus Cards for access control and payments.",
                "E-learning and digital library integration."
            ]
        }
    },
    "HEALTH": {
        "keywords": ["HOSPITAL", "HEALTH", "DISPENSARY", "CLINIC", "KEMRI", "REFERRAL"],
        "data": {
            "inputs": [
                "Patient Personal/Bio-data",
                "Insurance Card / NHIF Number",
                "Medical History Records",
                "Triage Vitals (BP, Temp, etc.)"
            ],
            "outputs": [
                "Patient File / EMR Record",
                "Diagnostic Lab Reports",
                "Prescription / Medication",
                "Discharge Summary"
            ],
            "pain_points": [
                "Loss of physical patient files.",
                "Long patient wait times at triage and pharmacy.",
                "Lack of interoperability between departments (Lab, Pharmacy, Billing).",
                "Revenue leakage in cash collections."
            ],
            "digitization_opportunities": [
                "Comprehensive Electronic Medical Records (EMR).",
                "Telemedicine for remote consultations.",
                "AI-assisted diagnostics and radiology.",
                "Automated inventory management for pharmacy."
            ]
        }
    },
    "REGULATORY": {
        "keywords": ["AUTHORITY", "BOARD", "COMMISSION", "COUNCIL", "BUREAU", "AGENCY", "SERVICE", "TRUST", "NEMA", "EPRA", "NCA"],
        "data": {
            "inputs": [
                "Application Form (License/Permit)",
                "Compliance Documents (Tax Compliance, CR12)",
                "Technical Reports / Site Plans",
                "Proof of Payment"
            ],
            "outputs": [
                "License / Permit / Certificate",
                "Compliance Inspection Report",
                "Official Receipt",
                "Gazette Notice"
            ],
            "pain_points": [
                "Manual document verification takes time.",
                "High cost and time for physical inspections.",
                "Risk of counterfeit licenses/certificates.",
                "Lack of real-time monitoring of licensees."
            ],
            "digitization_opportunities": [
                "Online Licensing Management System (LMS).",
                "Integration with IPRS and BRS for auto-verification.",
                "Mobile field inspection apps with GIS.",
                "QR-coded verifiable certificates."
            ]
        }
    },
    "FINANCE_COMMERCIAL": {
        "keywords": ["FUND", "BANK", "CORPORATION", "COMPANY", "LODGE", "HOTEL", "INSURANCE", "REVENUE", "TREASURY"],
        "data": {
            "inputs": [
                "Loan/Service Application Form",
                "Business Proposal / Plan",
                "Financial Statements / Bank Records",
                "Collateral / Security Documents"
            ],
            "outputs": [
                "Loan Disbursement / Service Delivery",
                "Statement of Account",
                "Contract / Agreement",
                "Receipt / Invoice"
            ],
            "pain_points": [
                "Lengthy credit appraisal processes.",
                "Manual debt collection and reconciliation.",
                "High paperwork for loan processing.",
                "Lack of 360-degree customer view."
            ],
            "digitization_opportunities": [
                "Automated Credit Scoring and Appraisal.",
                "Mobile-based loan application and repayment.",
                "Customer Relationship Management (CRM) systems.",
                "Data analytics for risk management."
            ]
        }
    },
    "MINISTRY_POLICY": {
        "keywords": ["MINISTRY", "STATE DEPARTMENT", "OFFICE", "AFFAIRS"],
        "data": {
            "inputs": [
                "Public Inquiries / Petitions",
                "Policy Proposals / Memos",
                "Inter-agency Correspondence",
                "Cabinet Memos"
            ],
            "outputs": [
                "Policy Guidelines / Circulars",
                "Official Response Letters",
                "Cabinet Resolutions",
                "Public Service Reports"
            ],
            "pain_points": [
                "Slow movement of physical files (Bureaucracy).",
                "Loss of institutional memory (Manual registries).",
                "Difficulty in tracking correspondence status.",
                "Siloed operations between departments."
            ],
            "digitization_opportunities": [
                "Electronic Document and Records Management System (EDRMS).",
                "Digital dashboard for project monitoring.",
                "Unified communication and collaboration platforms.",
                "Knowledge Management Systems."
            ]
        }
    }
}

# --- 2. High-Fidelity Overrides (Specific Mandates) ---
specifics = {
    "IMMIGRATION": {
        "inputs": ["Old Passport/ID", "Birth Certificate", "Biometrics (Fingerprints, Face)"],
        "outputs": ["e-Passport", "Visa", "Work Permit"],
        "pains": ["Crowding at Nyayo House", "Delay in printing", "Manual file retrieval"],
        "opps": ["Facial recognition gates", "Decentralized printing", "Home delivery"]
    },
    "REVENUE AUTHORITY": {
        "inputs": ["Tax Return Form", "Bank Statements", "Import Entry Declaration"],
        "outputs": ["Tax Compliance Certificate", "Assessment Order", "Release Order"],
        "pains": ["Tax evasion", "Complex filing process", "System downtime"],
        "opps": ["Data warehousing/Analytics", "Real-time VAT monitoring (TIMS)", "AI for fraud detection"]
    },
    "TRANSPORT AND SAFETY": {
        "inputs": ["Old DL", "Police Abstract", "Vehicle Logbook"],
        "outputs": ["Smart DL", "Number Plate", "Inspection Cert"],
        "pains": ["Fake licenses", "Road safety data gaps", "Manual inspection"],
        "opps": ["Smart traffic cameras", "Telematics", "Digital number plates"]
    },
    "LANDS": {
        "inputs": ["Transfer Form", "Title Deed", "Land Rent Clearance"],
        "outputs": ["Search Certificate", "New Title Deed", "Green Card Entry"],
        "pains": ["Missing green cards", "Fraud/Double allocation", "Manual search"],
        "opps": ["Blockchain for land registry", "GIS digitization", "Fully cashless"]
    },
    "POLICE": {
        "inputs": ["Complaint/Statement", "Fingerprints", "Evidence"],
        "outputs": ["P3 Form", "Police Abstract", "Good Conduct Cert"],
        "pains": ["Lost case files", "Manual OB (Occurrence Book)", "Slow response"],
        "opps": ["Digitized OB", "Integrated Case Management", "CCTV surveillance"]
    }
}

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    count = 0

    for item in items:
        # Check if fields are empty
        if item.get('inputs_outputs_dependencies', {}).get('inputs'):
            continue  # Already populated

        mda_name = item.get('mda_name', '').upper()
        profile_data = None

        # A. Check Specifics first
        for key in specifics:
            if key in mda_name:
                spec = specifics[key]
                profile_data = {
                    "inputs": spec["inputs"],
                    "outputs": spec["outputs"],
                    "pain_points": spec["pains"],
                    "digitization_opportunities": spec["opps"]
                }
                break
        
        # B. Check Profiles if no specific match
        if not profile_data:
            # Determine profile
            if any(k in mda_name for k in profiles["EDUCATION"]["keywords"]):
                profile_data = profiles["EDUCATION"]["data"]
            elif any(k in mda_name for k in profiles["HEALTH"]["keywords"]):
                profile_data = profiles["HEALTH"]["data"]
            elif any(k in mda_name for k in profiles["FINANCE_COMMERCIAL"]["keywords"]):
                profile_data = profiles["FINANCE_COMMERCIAL"]["data"]
            elif any(k in mda_name for k in profiles["MINISTRY_POLICY"]["keywords"]):
                profile_data = profiles["MINISTRY_POLICY"]["data"]
            else:
                # Default to Regulatory/Service (Catch-all)
                profile_data = profiles["REGULATORY"]["data"]

        # Apply Data
        item['inputs_outputs_dependencies'] = {
            "inputs": profile_data["inputs"],
            "outputs": profile_data["outputs"],
            "external_dependencies": ["National Treasury (Funding)", "ICT Authority (Standards)"]
        }
        item['pain_points_bottlenecks_risks'] = profile_data["pain_points"]
        item['digitization_opportunities'] = profile_data["digitization_opportunities"]
        
        count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Enriched {count} MDAs with Mandate-Specific Data (Inputs/Outputs/Pains/Opps).")

except Exception as e:
    print(f"Error: {e}")
