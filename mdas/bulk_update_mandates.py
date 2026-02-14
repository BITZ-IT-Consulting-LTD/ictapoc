import json
import sys

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

updates = {
    "NATIONAL TREASURY": {
        "narrative": "The National Treasury manages the Exchequer Release process to fund MDAs and Counties based on approved budgets and cash flow plans. (Derived from PFM Act Mandate).",
        "steps": [
            {"step_number": 1, "description": "MDA/County submits Cash Flow Plan and Exchequer Requisition to Treasury.", "actor": "MDA/County"},
            {"step_number": 2, "description": "Treasury Budget Department reviews requisition against approved estimates.", "actor": "Budget Dept"},
            {"step_number": 3, "description": "Accountant General Services Department (AGSD) processes the payment voucher.", "actor": "AGSD"},
            {"step_number": 4, "description": "Controller of Budget (COB) approves the withdrawal.", "actor": "COB"},
            {"step_number": 5, "description": "Treasury releases funds to the MDA/County Central Bank account via IFMIS.", "actor": "Treasury"}
        ]
    },
    "FINANCIAL REPORTING CENTRE": {
        "narrative": "Reporting institutions submit Suspicious Transaction Reports (STRs) to FRC for analysis and dissemination to law enforcement. (Derived from POCAMLA Act Mandate).",
        "steps": [
            {"step_number": 1, "description": "Reporting Institution (Bank/Forex) detects suspicious activity.", "actor": "Reporting Institution"},
            {"step_number": 2, "description": "Compliance Officer logs into goAML Portal.", "actor": "Compliance Officer"},
            {"step_number": 3, "description": "Officer uploads the STR (Suspicious Transaction Report) and supporting documents.", "actor": "Compliance Officer"},
            {"step_number": 4, "description": "FRC Analysts review and analyze the report for money laundering links.", "actor": "FRC Analyst"},
            {"step_number": 5, "description": "FRC disseminates intelligence report to DCI/EACC/NIS for investigation.", "actor": "FRC"}
        ]
    },
    "NACADA": {
        "narrative": "Licensing of alcoholic drink importers/exporters involves strict vetting to prevent illicit trade. (Derived from Alcoholic Drinks Control Act Mandate).",
        "steps": [
            {"step_number": 1, "description": "Importer/Exporter registers on NACADA Portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant submits dossier (Product sample, KEBS cert, KRA Tax Compliance).", "actor": "Applicant"},
            {"step_number": 3, "description": "NACADA conducts physical inspection of storage/premises.", "actor": "NACADA Inspector"},
            {"step_number": 4, "description": "Applicant pays the licensing fee.", "actor": "Applicant"},
            {"step_number": 5, "description": "NACADA issues Import/Export License.", "actor": "NACADA"}
        ]
    },
    "GEOTHERMAL DEVELOPMENT": {
        "narrative": "GDC explores and drills geothermal wells, selling steam to power generators like KenGen. (Derived from GDC Mandate).",
        "steps": [
            {"step_number": 1, "description": "GDC conducts surface exploration and identifies drilling sites.", "actor": "GDC Science Team"},
            {"step_number": 2, "description": "GDC drills exploration and production wells.", "actor": "GDC Drilling"},
            {"step_number": 3, "description": "Wells are tested for steam viability and pressure.", "actor": "GDC Engineers"},
            {"step_number": 4, "description": "Steam Gathering System connects wells to the power plant.", "actor": "GDC"},
            {"step_number": 5, "description": "Steam is metered and sold to KenGen/IPP for electricity generation.", "actor": "GDC"}
        ]
    },
    "SOLICITOR GENERAL": {
        "narrative": "The State Law Office reviews and approves government contracts and treaties before signing. (Derived from Office of Attorney General Act).",
        "steps": [
            {"step_number": 1, "description": "MDA submits draft contract/MOU to the Attorney General.", "actor": "MDA"},
            {"step_number": 2, "description": "Solicitor General assigns State Counsel to review the document.", "actor": "Solicitor General"},
            {"step_number": 3, "description": "State Counsel reviews for legal compliance and risks.", "actor": "State Counsel"},
            {"step_number": 4, "description": "Legal opinion/clearance is drafted and approved.", "actor": "SG/AG"},
            {"step_number": 5, "description": "Advisory opinion/Clearance letter sent back to MDA.", "actor": "Attorney General"}
        ]
    },
    "MEAT COMMISSION": {
        "narrative": "KMC implements the Livestock Offtake Program to purchase animals from farmers for processing. (Derived from KMC Act).",
        "steps": [
            {"step_number": 1, "description": "Farmer delivers livestock to KMC depot/factory.", "actor": "Farmer"},
            {"step_number": 2, "description": "KMC Vets inspect animals for health and quality (Ante-mortem).", "actor": "KMC Vet"},
            {"step_number": 3, "description": "Animals are weighed to determine purchase price.", "actor": "KMC Weighbridge"},
            {"step_number": 4, "description": "Animals are slaughtered and processed.", "actor": "KMC Operations"},
            {"step_number": 5, "description": "Payment is processed to the farmer's bank account.", "actor": "KMC Finance"}
        ]
    },
    "NEW KENYA CO-OPERATIVE": {
        "narrative": "New KCC collects milk from farmers and cooperatives for processing and marketing. (Derived from Core Business).",
        "steps": [
            {"step_number": 1, "description": "Farmer delivers milk to New KCC Cooling Plant/Collection Centre.", "actor": "Farmer"},
            {"step_number": 2, "description": "Milk is tested for quality (lactometer/alcohol test) and weighed.", "actor": "Quality Clerk"},
            {"step_number": 3, "description": "Delivery slip is issued to the farmer.", "actor": "Clerk"},
            {"step_number": 4, "description": "Milk is transported to main processing factory.", "actor": "Logistics"},
            {"step_number": 5, "description": "Farmer receives monthly payment based on volume and quality.", "actor": "Finance"}
        ]
    },
    "ANTI-FEMALE GENITAL": {
        "narrative": "The Board coordinates the reporting and rescue of FGM victims and prosecution of offenders. (Derived from Prohibition of FGM Act).",
        "steps": [
            {"step_number": 1, "description": "Member of public reports FGM incident/threat via Hotline/Chief.", "actor": "Reporter"},
            {"step_number": 2, "description": "Anti-FGM Board coordinates with Police/Chief for intervention.", "actor": "Board/Police"},
            {"step_number": 3, "description": "Victim is rescued and taken to a safe house/medical facility.", "actor": "Rescue Team"},
            {"step_number": 4, "description": "Suspects are arrested and statements recorded.", "actor": "Police"},
            {"step_number": 5, "description": "Board provides legal support for prosecution.", "actor": "Board Legal Team"}
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
        # Update even if matched before if we have better data now? 
        # Or only if empty. Let's prioritize these updates as they are high quality.
        
        mda_name = item.get('mda_name', '').upper()
        if not mda_name:
            continue
            
        for key in updates:
            # Flexible matching
            if key in mda_name:
                item['as_is_steps'] = updates[key]['steps']
                item['as_is_narrative'] = updates[key]['narrative']
                if 'process_maturity' not in item:
                    item['process_maturity'] = {}
                item['process_maturity']['documentation_status'] = 'Documented (Specific Mandate-Based)'
                
                updated_names.append(item.get('mda_name'))
                count += 1
                break 

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {count} MDAs with Specific Mandate Data.")
    for name in updated_names:
        print(f"- {name}")

except Exception as e:
    print(f"Error: {e}")
