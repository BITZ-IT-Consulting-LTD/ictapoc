import json
import sys

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

updates = {
    "COMMUNICATIONS AUTHORITY": {
        "narrative": "Type Approval for telecommunications equipment is managed via the CA Regulatory Management System. (Updated with standard CA workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant creates a profile on the CA Regulatory Portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant submits Type Approval application with equipment specs and test reports.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant submits a sample device (if required) to CA.", "actor": "Applicant"},
            {"step_number": 4, "description": "Applicant pays the Type Approval fee.", "actor": "Applicant"},
            {"step_number": 5, "description": "CA technical team evaluates and tests the equipment.", "actor": "CA"},
            {"step_number": 6, "description": "CA issues the Type Approval Certificate.", "actor": "CA"}
        ]
    },
    "MINING": {
        "narrative": "Mineral rights applications are processed via the Mining Cadastre Portal. (Updated with standard Mining workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant registers on the Mining Cadastre Portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant applies for a Prospecting or Mining License.", "actor": "Applicant"},
            {"step_number": 3, "description": "System checks for overlapping coordinates/rights.", "actor": "System"},
            {"step_number": 4, "description": "Applicant pays the application fee.", "actor": "Applicant"},
            {"step_number": 5, "description": "Mineral Rights Board reviews and recommends approval.", "actor": "MRB"},
            {"step_number": 6, "description": "Cabinet Secretary grants the license.", "actor": "CS Mining"}
        ]
    },
    "EXAMINATIONS COUNCIL": {
        "narrative": "Replacement of lost certificates or confirmation of results is done via the KNEC QMIS (Query Management Information System). (Updated with standard KNEC workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant registers on KNEC QMIS portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant selects 'Lost Certificate' or 'Confirmation' service.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant uploads ID, Police Abstract, and pays the fee.", "actor": "Applicant"},
            {"step_number": 4, "description": "KNEC processes the request (retrieval from archives).", "actor": "KNEC"},
            {"step_number": 5, "description": "Applicant collects the document from KNEC offices.", "actor": "Applicant"}
        ]
    },
    "WILDLIFE SERVICE": {
        "narrative": "Research permits for wildlife studies are managed via the KWS Research Authorization process. (Updated with standard KWS workflow).",
        "steps": [
            {"step_number": 1, "description": "Researcher submits a proposal and application to KWS.", "actor": "Researcher"},
            {"step_number": 2, "description": "KWS Research Committee reviews the proposal.", "actor": "KWS"},
            {"step_number": 3, "description": "Researcher obtains research license from NACOSTI (prerequisite).", "actor": "Researcher"},
            {"step_number": 4, "description": "Researcher pays KWS affiliation/permit fees.", "actor": "Researcher"},
            {"step_number": 5, "description": "KWS issues the Research Permit/Entry Pass.", "actor": "KWS"}
        ]
    },
    "FOREST SERVICE": {
        "narrative": "Movement of forest products requires a Movement Permit to curb illegal logging. (Updated with standard KFS workflow).",
        "steps": [
            {"step_number": 1, "description": "Transporter applies for a Movement Permit at the Forest Station.", "actor": "Transporter"},
            {"step_number": 2, "description": "Forest Officer inspects the forest produce and verifies origin.", "actor": "KFS Officer"},
            {"step_number": 3, "description": "Transporter pays the movement fees via M-Pesa.", "actor": "Transporter"},
            {"step_number": 4, "description": "Forest Officer issues the Movement Permit specifying route and validity.", "actor": "KFS Officer"}
        ]
    },
    "FISHERIES SERVICE": {
        "narrative": "Fishing vessel licensing ensures sustainable exploitation of marine resources. (Updated with standard KeFS workflow).",
        "steps": [
            {"step_number": 1, "description": "Vessel owner applies for a fishing license.", "actor": "Owner"},
            {"step_number": 2, "description": "KeFS conducts vessel inspection for safety and gear compliance.", "actor": "KeFS Inspector"},
            {"step_number": 3, "description": "Owner pays the license fee.", "actor": "Owner"},
            {"step_number": 4, "description": "KeFS Director General approves and issues the license.", "actor": "KeFS"}
        ]
    },
    "ANTI-COUNTERFEIT": {
        "narrative": "IPR Recordal allows brand owners to record their trademarks with ACA to prevent imports of counterfeits. (Updated with standard ACA workflow).",
        "steps": [
            {"step_number": 1, "description": "IP Right owner logs into the ACA AIMS portal.", "actor": "Brand Owner"},
            {"step_number": 2, "description": "Applicant submits application for IPR Recordal (Form ACA 1).", "actor": "Brand Owner"},
            {"step_number": 3, "description": "Applicant uploads image of genuine product and trademark certs.", "actor": "Brand Owner"},
            {"step_number": 4, "description": "Applicant pays the recordal fee.", "actor": "Brand Owner"},
            {"step_number": 5, "description": "ACA approves and issues the IPR Recordal Certificate.", "actor": "ACA"}
        ]
    },
    "NATIONAL HOUSING": {
        "narrative": "Tenant Purchase Scheme (TPS) application allows citizens to own homes through monthly installments. (Updated with standard NHC workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant identifies a housing project and applies.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant pays the required deposit (e.g., 10-20%).", "actor": "Applicant"},
            {"step_number": 3, "description": "NHC Allocation Committee allocates the unit.", "actor": "NHC"},
            {"step_number": 4, "description": "Applicant signs the Tenant Purchase Agreement.", "actor": "Applicant"},
            {"step_number": 5, "description": "Applicant makes monthly payments over the agreed period.", "actor": "Applicant"}
        ]
    },
    "TRADE NETWORK": {
        "narrative": "The Kenya TradeNet System (Single Window) integrates export/import clearances. (Updated with standard KenTrade workflow).",
        "steps": [
            {"step_number": 1, "description": "Clearing Agent/Importer registers on TradeNet System.", "actor": "User"},
            {"step_number": 2, "description": "User submits Unique Consignment Reference (UCR).", "actor": "User"},
            {"step_number": 3, "description": "User lodges declaration/manifest.", "actor": "User"},
            {"step_number": 4, "description": "Partner Government Agencies (PGAs) approve permits online.", "actor": "PGAs"},
            {"step_number": 5, "description": "User pays duties and fees via e-slip.", "actor": "User"},
            {"step_number": 6, "description": "KRA issues release order.", "actor": "KRA"}
        ]
    },
    "INDUSTRIAL TRAINING": {
        "narrative": "Industrial Training Levy compliance is mandatory for employers. (Updated with standard NITA workflow).",
        "steps": [
            {"step_number": 1, "description": "Employer registers with NITA.", "actor": "Employer"},
            {"step_number": 2, "description": "Employer declares number of employees annually.", "actor": "Employer"},
            {"step_number": 3, "description": "Employer pays the monthly levy (KES 50 per employee).", "actor": "Employer"},
            {"step_number": 4, "description": "NITA issues Compliance Certificate.", "actor": "NITA"}
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
                if 'process_maturity' not in item:
                    item['process_maturity'] = {}
                item['process_maturity']['documentation_status'] = 'Documented (Inferred Standard Process)'
                
                updated_names.append(item.get('mda_name'))
                count += 1
                break 

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {count} MDAs.")
    for name in updated_names:
        print(f"- {name}")

except Exception as e:
    print(f"Error: {e}")
