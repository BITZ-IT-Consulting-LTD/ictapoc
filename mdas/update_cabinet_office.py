import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

cabinet_update = {
    "narrative": "The Cabinet Office coordinates the processing of Cabinet Memoranda, scheduling of meetings, and communication of Executive decisions. (Updated with specific Cabinet Secretariat workflow).",
    "steps": [
        {"step_number": 1, "description": "Ministry/State Department submits a Draft Cabinet Memo to the Head of Public Service.", "actor": "Ministry PS"},
        {"step_number": 2, "description": "Cabinet Office Secretariat reviews the Memo for policy alignment and formatting compliance.", "actor": "Cabinet Secretariat"},
        {"step_number": 3, "description": "Approved Memo is allocated a Cabinet Paper Number and scheduled for an upcoming Cabinet Meeting.", "actor": "Secretary to Cabinet"},
        {"step_number": 4, "description": "Cabinet deliberates on the Memo during the scheduled meeting.", "actor": "The Cabinet"},
        {"step_number": 5, "description": "Cabinet Office records the decision as a Cabinet Minute (Resolution).", "actor": "Secretariat"},
        {"step_number": 6, "description": "Cabinet Office issues a 'Notification of Cabinet Decision' to the originating Ministry.", "actor": "Head of Public Service"}
    ],
    "inputs": [
        "Draft Cabinet Memo",
        "Policy Proposal Document",
        "Legal Opinion (Attorney General)",
        "Treasury Concurrence (Financial Implications)"
    ],
    "outputs": [
        "Cabinet Paper Number",
        "Cabinet Minute/Resolution",
        "Notification of Decision Letter"
    ],
    "pain_points": [
        "Manual movement of sensitive physical files.",
        "Risk of leakage of confidential information.",
        "Delays in scheduling and feedback.",
        "Difficulty in tracking implementation status."
    ],
    "digitization_opportunities": [
        "Secure e-Cabinet System for digital memo distribution.",
        "Biometric access control for meeting documents.",
        "Digital dashboard for tracking Cabinet decision implementation.",
        "Encrypted communication channels."
    ]
}

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    updated = False

    for item in items:
        if item.get('mda_name') == "CABINET OFFICE":
            item['as_is_steps'] = cabinet_update['steps']
            item['as_is_narrative'] = cabinet_update['narrative']
            item['inputs_outputs_dependencies'] = {
                "inputs": cabinet_update['inputs'],
                "outputs": cabinet_update['outputs'],
                "external_dependencies": ["All Ministries", "Attorney General", "National Treasury"]
            }
            item['pain_points_bottlenecks_risks'] = cabinet_update['pain_points']
            item['digitization_opportunities'] = cabinet_update['digitization_opportunities']
            
            # Ensure To-Be reflects G2G nature (e-Cabinet)
            item['to_be_process'] = {
                "narrative": "The To-Be process utilizes a secure e-Cabinet System where Ministers access papers via tablets, and decisions are digitally tracked.",
                "steps": [
                    {"step_number": 1, "description": "Ministry uploads Memo to secure e-Cabinet Portal.", "actor": "PS", "system": "e-Cabinet"},
                    {"step_number": 2, "description": "System validates attachments (AG/Treasury) and routes for Secretariat review.", "actor": "System", "system": "e-Cabinet"},
                    {"step_number": 3, "description": "Secretariat schedules the item digitally; Agenda is pushed to Cabinet tablets.", "actor": "Secretariat", "system": "e-Cabinet"},
                    {"step_number": 4, "description": "Decisions are recorded in the system during the meeting.", "actor": "Secretariat", "system": "e-Cabinet"},
                    {"step_number": 5, "description": "System auto-generates Notification Letter and emails it to the Ministry.", "actor": "System", "system": "e-Cabinet"}
                ]
            }
            
            item['process_maturity'] = {'documentation_status': 'Documented (Specific Mandate)'}
            updated = True
            break

    if updated:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Successfully updated CABINET OFFICE.")
    else:
        print("CABINET OFFICE not found.")

except Exception as e:
    print(f"Error: {e}")
