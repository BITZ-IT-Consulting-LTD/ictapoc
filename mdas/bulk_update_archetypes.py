import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

# Archetype Workflows
archetypes = {
    "EDUCATION": {
        "keywords": ["UNIVERSITY", "POLYTECHNIC", "COLLEGE", "INSTITUTE OF TECHNOLOGY", "TTI", "VC", "JQUAT", "JKUAT", "DEKUT", "JOOUST", "KMTC", "KAIST"],
        "narrative": "Student admission and registration involves acceptance of placement, fee payment, and biometric registration. (Standard Higher Education Workflow).",
        "steps": [
            {"step_number": 1, "description": "Student receives placement notification via KUCCPS or applies directly as Self-Sponsored.", "actor": "Student"},
            {"step_number": 2, "description": "Student logs into the Institution's Student Portal to accept admission and download Admission Letter.", "actor": "Student"},
            {"step_number": 3, "description": "Student pays tuition and statutory fees via Bank or eCitizen.", "actor": "Student"},
            {"step_number": 4, "description": "Student physically reports to the institution for document verification (original slips, certs).", "actor": "Student"},
            {"step_number": 5, "description": "Institution registers the student in the ERP system.", "actor": "Registrar"},
            {"step_number": 6, "description": "Student is issued a Student ID card.", "actor": "Student"}
        ]
    },
    "INFRASTRUCTURE_AGENCY": {
        "keywords": ["WATER WORKS", "DEVELOPMENT AUTHORITY", "ROADS AUTHORITY", "HIGHWAYS AUTHORITY", "URBAN ROADS", "RURAL ROADS"],
        "narrative": "Project procurement involves competitive tendering for infrastructure development. (Standard Infrastructure Procurement Workflow).",
        "steps": [
            {"step_number": 1, "description": "Agency advertises tender on Public Procurement Information Portal (PPIP) and website.", "actor": "Agency"},
            {"step_number": 2, "description": "Bidder downloads tender documents and prepares bid (Technical & Financial).", "actor": "Bidder"},
            {"step_number": 3, "description": "Bidder submits bid via e-Procurement portal or tender box.", "actor": "Bidder"},
            {"step_number": 4, "description": "Evaluation Committee conducts opening, technical, and financial evaluation.", "actor": "Evaluation Committee"},
            {"step_number": 5, "description": "Accounting Officer awards the tender to the lowest responsive bidder.", "actor": "Accounting Officer"},
            {"step_number": 6, "description": "Contract is signed after the 14-day standstill period.", "actor": "Agency/Bidder"}
        ]
    },
    "RESEARCH": {
        "keywords": ["RESEARCH INSTITUTE", "RESEARCH ORGANIZATION", "KEMRI", "KALRO", "KEFRI", "KMFRI"],
        "narrative": "Research proposal approval involves scientific and ethical review. (Standard Research Institute Workflow).",
        "steps": [
            {"step_number": 1, "description": "Researcher submits research proposal/protocol to the Institute.", "actor": "Researcher"},
            {"step_number": 2, "description": "Scientific Steering Committee (SSC) reviews scientific merit.", "actor": "SSC"},
            {"step_number": 3, "description": "Ethics Review Committee (ERC) reviews ethical compliance.", "actor": "ERC"},
            {"step_number": 4, "description": "Researcher pays institutional affiliation/review fees.", "actor": "Researcher"},
            {"step_number": 5, "description": "Institute issues Letter of Approval/Affiliation.", "actor": "Institute"}
        ]
    }
}

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    count = 0
    updated_counts = {"EDUCATION": 0, "INFRASTRUCTURE_AGENCY": 0, "RESEARCH": 0}

    for item in items:
        # Skip if already updated (has steps)
        if item.get('as_is_steps') and len(item.get('as_is_steps')) > 0:
            continue

        mda_name = item.get('mda_name', '').upper()
        if not mda_name:
            continue

        matched = False
        
        # Check Education
        for kw in archetypes["EDUCATION"]["keywords"]:
            if kw in mda_name and "KENYA INSTITUTE OF CURRICULUM" not in mda_name: # Exclude non-teaching institutes if needed
                item['as_is_steps'] = archetypes["EDUCATION"]["steps"]
                item['as_is_narrative'] = archetypes["EDUCATION"]["narrative"]
                item['process_maturity'] = {'documentation_status': 'Documented (Standard Archetype)'}
                updated_counts["EDUCATION"] += 1
                matched = True
                break
        
        if matched: count += 1; continue

        # Check Infrastructure
        for kw in archetypes["INFRASTRUCTURE_AGENCY"]["keywords"]:
            if kw in mda_name:
                item['as_is_steps'] = archetypes["INFRASTRUCTURE_AGENCY"]["steps"]
                item['as_is_narrative'] = archetypes["INFRASTRUCTURE_AGENCY"]["narrative"]
                item['process_maturity'] = {'documentation_status': 'Documented (Standard Archetype)'}
                updated_counts["INFRASTRUCTURE_AGENCY"] += 1
                matched = True
                break
        
        if matched: count += 1; continue

        # Check Research
        for kw in archetypes["RESEARCH"]["keywords"]:
            if kw in mda_name:
                item['as_is_steps'] = archetypes["RESEARCH"]["steps"]
                item['as_is_narrative'] = archetypes["RESEARCH"]["narrative"]
                item['process_maturity'] = {'documentation_status': 'Documented (Standard Archetype)'}
                updated_counts["RESEARCH"] += 1
                matched = True
                break
        
        if matched: count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Total Updated: {count}")
    print(f"Breakdown: {updated_counts}")

except Exception as e:
    print(f"Error: {e}")
