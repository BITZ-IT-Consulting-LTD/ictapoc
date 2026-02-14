import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

# Archetype Workflows
archetypes = {
    "HOSPITAL": {
        "keywords": ["HOSPITAL", "REFERRAL", "DISPENSARY", "HEALTH CENTRE", "CLINIC", "MATHARI", "KENYATTA NATIONAL", "MOI TEACHING"],
        "narrative": "Patient management involves registration, triage, and treatment. (Standard Hospital Workflow).",
        "steps": [
            {"step_number": 1, "description": "Patient registers at the reception desk and pays registration fee.", "actor": "Patient"},
            {"step_number": 2, "description": "Nurse conducts triage (vitals check) and records history.", "actor": "Nurse"},
            {"step_number": 3, "description": "Doctor consults and prescribes treatment or diagnostic tests.", "actor": "Doctor"},
            {"step_number": 4, "description": "Patient pays for laboratory/pharmacy services.", "actor": "Patient"},
            {"step_number": 5, "description": "Patient collects medication or undergoes procedures.", "actor": "Patient"}
        ]
    },
    "STATE_CORPORATION": {
        "keywords": ["COMPANY", "CORPORATION", "LODGE", "HOTEL", "MILLS", "CREAMERIES", "PRESS", "ENTERPRISES", "LIMITED", "KENYA PIPELINE", "KENYA PORTS", "KENYA RAILWAYS", "POSTAL CORPORATION", "BROADCASTING", "CEMENT", "SUGAR", "MEAT", "SEEDS", "WINE", "CONVENTION"],
        "narrative": "Commercial service or product delivery involves order processing and fulfillment. (Standard State Corporation Workflow).",
        "steps": [
            {"step_number": 1, "description": "Customer submits an order or request for goods/services.", "actor": "Customer"},
            {"step_number": 2, "description": "Corporation processes the request and issues a quotation/proforma invoice.", "actor": "Sales Department"},
            {"step_number": 3, "description": "Customer makes payment via Bank or M-Pesa.", "actor": "Customer"},
            {"step_number": 4, "description": "Corporation releases the goods or delivers the service.", "actor": "Stores/Operations"},
            {"step_number": 5, "description": "Customer signs Delivery Note or Service Acceptance Form.", "actor": "Customer"}
        ]
    },
    "REGULATORY_AUTHORITY": {
        "keywords": ["AUTHORITY", "BOARD", "COMMISSION", "COUNCIL", "BUREAU", "AGENCY", "SERVICE", "TRUST", "FUND"],
        "narrative": "Regulatory compliance and service delivery involves application, verification, and issuance. (Standard Regulatory/Service Workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant submits application for license, permit, or service.", "actor": "Applicant"},
            {"step_number": 2, "description": "Authority verifies documents and compliance with regulations.", "actor": "Authority"},
            {"step_number": 3, "description": "Technical officers conduct assessment or inspection.", "actor": "Technical Officer"},
            {"step_number": 4, "description": "Applicant pays the prescribed fees.", "actor": "Applicant"},
            {"step_number": 5, "description": "Authority approves and issues the License/Permit/Certificate.", "actor": "Authority"}
        ]
    }
}

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    count = 0
    updated_counts = {"HOSPITAL": 0, "STATE_CORPORATION": 0, "REGULATORY_AUTHORITY": 0}

    for item in items:
        # Skip if already updated (has steps)
        if item.get('as_is_steps') and len(item.get('as_is_steps')) > 0:
            continue

        mda_name = item.get('mda_name', '').upper()
        if not mda_name:
            continue

        matched = False
        
        # 1. Hospitals
        for kw in archetypes["HOSPITAL"]["keywords"]:
            if kw in mda_name:
                item['as_is_steps'] = archetypes["HOSPITAL"]["steps"]
                item['as_is_narrative'] = archetypes["HOSPITAL"]["narrative"]
                item['process_maturity'] = {'documentation_status': 'Documented (Standard Archetype)'}
                updated_counts["HOSPITAL"] += 1
                matched = True
                break
        if matched: count += 1; continue

        # 2. State Corporations
        for kw in archetypes["STATE_CORPORATION"]["keywords"]:
            if kw in mda_name:
                item['as_is_steps'] = archetypes["STATE_CORPORATION"]["steps"]
                item['as_is_narrative'] = archetypes["STATE_CORPORATION"]["narrative"]
                item['process_maturity'] = {'documentation_status': 'Documented (Standard Archetype)'}
                updated_counts["STATE_CORPORATION"] += 1
                matched = True
                break
        if matched: count += 1; continue

        # 3. Regulatory/Service Authorities (Catch-all for remaining valid entities)
        # We need to be careful not to catch Ministries here if we want them separate, 
        # but the previous batch handled Ministries.
        for kw in archetypes["REGULATORY_AUTHORITY"]["keywords"]:
            if kw in mda_name:
                item['as_is_steps'] = archetypes["REGULATORY_AUTHORITY"]["steps"]
                item['as_is_narrative'] = archetypes["REGULATORY_AUTHORITY"]["narrative"]
                item['process_maturity'] = {'documentation_status': 'Documented (Standard Archetype)'}
                updated_counts["REGULATORY_AUTHORITY"] += 1
                matched = True
                break
        if matched: count += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Total Updated: {count}")
    print(f"Breakdown: {updated_counts}")

except Exception as e:
    print(f"Error: {e}")
