import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

# Archetype Workflows
archetypes = {
    "PROFESSIONAL_BOARD": {
        "keywords": ["BOARD", "COUNCIL", "INSTITUTE OF", "SOCIETY OF"],
        "exclude": ["WATER", "CEREALS", "PRODUCE", "REVENUE", "EXAMINATIONS", "TEA", "COFFEE", "SUGAR", "PEST", "FILM", "LOANS", "POWER", "LIGHTING", "ANTI", "GAMING", "BETTING", "LOTTERIES", "COPYRIGHT", "DAIRY", "IRRIGATION", "FOREST", "WILDLIFE", "LAND", "EXPORT", "SPECIAL", "ZONE", "HOUSING", "INDUSTRIAL", "MEDICAL", "NURSING", "CLINICAL", "PHARMACY", "VETERINARY"], 
        # Note: Excluding specific boards we might have done or want to do differently. 
        # Actually, Medical/Nursing/Clinical/Pharmacy/Vet boards are PERFECT for this archetype, so I should NOT exclude them if they haven't been done.
        # I removed Medical/Nursing etc from exclusions below in logic or relying on "already updated" check.
        # Re-evaluating exclusions: I will only exclude things that are definitely NOT professional boards (like Water Boards, Marketing Boards).
        "narrative": "Professional registration and licensing involves verification of academic qualifications and issuance of practicing certificates. (Standard Professional Board Workflow).",
        "steps": [
            {"step_number": 1, "description": "Professional registers on the Board's Online Portal.", "actor": "Professional"},
            {"step_number": 2, "description": "Applicant uploads academic certificates and professional testimonials.", "actor": "Professional"},
            {"step_number": 3, "description": "Board Secretariat conducts verification and indexing.", "actor": "Board"},
            {"step_number": 4, "description": "Applicant pays the registration/annual retention fee.", "actor": "Professional"},
            {"step_number": 5, "description": "Board gazettes the member and issues the Annual Practicing Certificate.", "actor": "Board"}
        ]
    },
    "FINANCE_AGENCY": {
        "keywords": ["FINANCE", "FUND", "BANK", "CAPITAL", "DEVELOPMENT CORPORATION", "CREDIT"],
        "exclude": ["CENTRAL BANK", "LAND", "WATER"],
        "narrative": "Financial support application involves credit appraisal and disbursement. (Standard Government Finance Workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant submits loan/grant application form with business proposal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Agency conducts desk appraisal and credit scoring.", "actor": "Agency"},
            {"step_number": 3, "description": "Field officer visits for due diligence (if applicable).", "actor": "Field Officer"},
            {"step_number": 4, "description": "Committee approves the facility/grant.", "actor": "Committee"},
            {"step_number": 5, "description": "Funds are disbursed to the applicant's account.", "actor": "Agency"}
        ]
    },
    "MINISTRY_POLICY": {
        "keywords": ["MINISTRY OF", "STATE DEPARTMENT", "CABINET OFFICE", "EXECUTIVE OFFICE"],
        "exclude": [],
        "narrative": "Public service delivery focuses on policy formulation, oversight, and complaints handling. (Standard Ministry Workflow).",
        "steps": [
            {"step_number": 1, "description": "Citizen/Stakeholder submits inquiry, complaint, or policy proposal via email or office.", "actor": "Citizen"},
            {"step_number": 2, "description": "Central Registry receives and tags the correspondence.", "actor": "Registry"},
            {"step_number": 3, "description": "Relevant Technical Directorate reviews and drafts response/action.", "actor": "Directorate"},
            {"step_number": 4, "description": "Principal Secretary/Director approves the response.", "actor": "PS/Director"},
            {"step_number": 5, "description": "Ministry issues official response or policy guideline.", "actor": "Ministry"}
        ]
    }
}

# Explicit exclusions for Professional Boards (things that are NOT people regulators)
board_exclusions = ["WATER", "CEREALS", "PRODUCE", "REVENUE", "EXAMINATIONS", "TEA", "COFFEE", "SUGAR", "PEST", "FILM", "LOANS", "POWER", "LIGHTING", "ANTI", "GAMING", "BETTING", "LOTTERIES", "COPYRIGHT", "DAIRY", "IRRIGATION", "FOREST", "WILDLIFE", "LAND", "EXPORT", "SPECIAL", "ZONE", "HOUSING", "INDUSTRIAL", "TOURISM", "TRADE", "NGO", "RETIREMENT", "BENEFITS", "INSURANCE", "CAPITAL", "COMPETITION", "COMMUNICATIONS", "AVIATION", "MARITIME", "PORTS", "RAILWAYS", "AIRPORTS", "PIPELINE", "KENYA REVENUE", "KENYA BUREAU"]

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    count = 0
    updated_counts = {"PROFESSIONAL_BOARD": 0, "FINANCE_AGENCY": 0, "MINISTRY_POLICY": 0}

    for item in items:
        # Skip if already updated (has steps)
        if item.get('as_is_steps') and len(item.get('as_is_steps')) > 0:
            continue

        mda_name = item.get('mda_name', '').upper()
        if not mda_name:
            continue

        matched = False
        
        # 1. Professional Boards
        is_excluded = any(ex in mda_name for ex in board_exclusions)
        if not is_excluded:
            for kw in archetypes["PROFESSIONAL_BOARD"]["keywords"]:
                if kw in mda_name:
                    item['as_is_steps'] = archetypes["PROFESSIONAL_BOARD"]["steps"]
                    item['as_is_narrative'] = archetypes["PROFESSIONAL_BOARD"]["narrative"]
                    item['process_maturity'] = {'documentation_status': 'Documented (Standard Archetype)'}
                    updated_counts["PROFESSIONAL_BOARD"] += 1
                    matched = True
                    break
        if matched: count += 1; continue

        # 2. Finance Agencies
        for kw in archetypes["FINANCE_AGENCY"]["keywords"]:
            if kw in mda_name and "REVENUE" not in mda_name:
                item['as_is_steps'] = archetypes["FINANCE_AGENCY"]["steps"]
                item['as_is_narrative'] = archetypes["FINANCE_AGENCY"]["narrative"]
                item['process_maturity'] = {'documentation_status': 'Documented (Standard Archetype)'}
                updated_counts["FINANCE_AGENCY"] += 1
                matched = True
                break
        if matched: count += 1; continue

        # 3. Ministries
        for kw in archetypes["MINISTRY_POLICY"]["keywords"]:
            if kw in mda_name:
                item['as_is_steps'] = archetypes["MINISTRY_POLICY"]["steps"]
                item['as_is_narrative'] = archetypes["MINISTRY_POLICY"]["narrative"]
                item['process_maturity'] = {'documentation_status': 'Documented (Standard Archetype)'}
                updated_counts["MINISTRY_POLICY"] += 1
                matched = True
                break
        if matched: count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Total Updated: {count}")
    print(f"Breakdown: {updated_counts}")

except Exception as e:
    print(f"Error: {e}")
