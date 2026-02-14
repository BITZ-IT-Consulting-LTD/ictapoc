import json
import sys

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

updates = {
    "CAPITAL MARKETS AUTHORITY": {
        "narrative": "Licensing of market intermediaries (brokers, fund managers) is conducted via the CMA Online Portal. (Updated with standard CMA workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant creates a profile on the CMA Online Portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant selects the license category (e.g., Investment Bank, Broker).", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant uploads required corporate documents and business plan.", "actor": "Applicant"},
            {"step_number": 4, "description": "Applicant pays the application fee.", "actor": "Applicant"},
            {"step_number": 5, "description": "CMA conducts fit and proper assessments of directors/shareholders.", "actor": "CMA"},
            {"step_number": 6, "description": "Upon approval, applicant pays the annual license fee.", "actor": "Applicant"},
            {"step_number": 7, "description": "CMA issues the License.", "actor": "CMA"}
        ]
    },
    "COMPETITION AUTHORITY": {
        "narrative": "Merger notification and approval ensures fair competition in the market. (Updated with standard CAK workflow).",
        "steps": [
            {"step_number": 1, "description": "Merging parties submit a merger notification to CAK.", "actor": "Merging Parties"},
            {"step_number": 2, "description": "Parties pay the merger filing fee based on turnover.", "actor": "Merging Parties"},
            {"step_number": 3, "description": "CAK conducts preliminary assessment to determine if full analysis is needed.", "actor": "CAK"},
            {"step_number": 4, "description": "CAK conducts full stakeholder analysis and market testing.", "actor": "CAK"},
            {"step_number": 5, "description": "CAK issues a determination (Approval, Approval with conditions, or Rejection).", "actor": "CAK"}
        ]
    },
    "INSURANCE REGULATORY": {
        "narrative": "Insurance Agent and Broker licensing is automated via the IRA Online Portal. (Updated with standard IRA workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant registers on the IRA Online Portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant applies for New/Renewal License and uploads COP (Certificate of Proficiency).", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant pays the license fee via M-Pesa/Bank.", "actor": "Applicant"},
            {"step_number": 4, "description": "IRA system validates details automatically (for agents) or via officer review (for brokers).", "actor": "IRA"},
            {"step_number": 5, "description": "System generates and emails the License.", "actor": "System"}
        ]
    },
    "RETIREMENT BENEFITS": {
        "narrative": "Pension scheme registration ensures compliance with the RBA Act. (Updated with standard RBA workflow).",
        "steps": [
            {"step_number": 1, "description": "Trustees submit application for registration of a scheme.", "actor": "Trustees"},
            {"step_number": 2, "description": "Trustees submit Trust Deed and Rules.", "actor": "Trustees"},
            {"step_number": 3, "description": "RBA reviews the governance structure and service provider contracts.", "actor": "RBA"},
            {"step_number": 4, "description": "Trustees pay the registration levy.", "actor": "Trustees"},
            {"step_number": 5, "description": "RBA issues the Certificate of Registration.", "actor": "RBA"}
        ]
    },
    "SACCO SOCIETIES": {
        "narrative": "SASRA licensing for Deposit-Taking Saccos (DT-Saccos) involves rigorous prudential checks. (Updated with standard SASRA workflow).",
        "steps": [
            {"step_number": 1, "description": "Proposed Sacco applies for letter of intent.", "actor": "Sacco"},
            {"step_number": 2, "description": "SASRA conducts pre-licensing inspection of systems and premises.", "actor": "SASRA"},
            {"step_number": 3, "description": "Sacco demonstrates minimum capital compliance.", "actor": "Sacco"},
            {"step_number": 4, "description": "SASRA reviews policies and governance.", "actor": "SASRA"},
            {"step_number": 5, "description": "SASRA issues the Deposit-Taking License.", "actor": "SASRA"}
        ]
    },
    "TOURISM REGULATORY": {
        "narrative": "Tourism enterprise licensing ensures standards in hotels and tour operations. (Updated with standard TRA workflow).",
        "steps": [
            {"step_number": 1, "description": "Operator applies for license via TRA Portal.", "actor": "Operator"},
            {"step_number": 2, "description": "Operator pays the application fee.", "actor": "Operator"},
            {"step_number": 3, "description": "TRA conducts physical inspection of the facility/vehicle.", "actor": "TRA Inspector"},
            {"step_number": 4, "description": "Upon compliance, operator pays the license fee.", "actor": "Operator"},
            {"step_number": 5, "description": "TRA issues the Tourism License.", "actor": "TRA"}
        ]
    },
    "KENYA INVESTMENT": {
        "narrative": "The Investment Certificate facilitates distinct incentives for foreign and local investors. (Updated with standard KenInvest workflow).",
        "steps": [
            {"step_number": 1, "description": "Investor creates account on e-Investment Portal.", "actor": "Investor"},
            {"step_number": 2, "description": "Investor submits project proposal and proof of investment (min $100k for foreign, KES 1M for local).", "actor": "Investor"},
            {"step_number": 3, "description": "KenInvest appraises the project.", "actor": "KenInvest"},
            {"step_number": 4, "description": "Investor pays the certificate fee.", "actor": "Investor"},
            {"step_number": 5, "description": "KenInvest issues the Investment Certificate.", "actor": "KenInvest"}
        ]
    },
    "WATER RESOURCES": {
        "narrative": "Water abstraction permits are managed via the WRA Permit Database. (Updated with standard WRA workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant applies for Water Permit (Category A, B, C, or D) via eCitizen/WRA.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant submits Hydrological Assessment Report.", "actor": "Applicant"},
            {"step_number": 3, "description": "WRA conducts site verification and public notification (for large categories).", "actor": "WRA"},
            {"step_number": 4, "description": "Applicant pays assessment and permit fees.", "actor": "Applicant"},
            {"step_number": 5, "description": "WRA issues the Water Permit.", "actor": "WRA"}
        ]
    },
    "PUBLIC PROCUREMENT": {
        "narrative": "AGPO (Access to Government Procurement Opportunities) registration is key for youth, women, and PWDs. (Updated with standard PPRA/Treasury workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant registers business on AGPO Portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant uploads ID, Business Reg Cert, and Tax Compliance Cert.", "actor": "Applicant"},
            {"step_number": 3, "description": "PPRA/Treasury verifies documents.", "actor": "PPRA"},
            {"step_number": 4, "description": "System approves application.", "actor": "System"},
            {"step_number": 5, "description": "Applicant downloads the AGPO Certificate.", "actor": "Applicant"}
        ]
    },
    "PERSONS WITH DISABILITIES": {
        "narrative": "Disability Registration provides an ID card for tax exemptions and services. (Updated with standard NCPWD workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant visits a gazetted Government Hospital for assessment.", "actor": "Applicant"},
            {"step_number": 2, "description": "Director of Medical Services signs the assessment report.", "actor": "MoH"},
            {"step_number": 3, "description": "Applicant submits report to NCPWD via eCitizen or County Office.", "actor": "Applicant"},
            {"step_number": 4, "description": "NCPWD Vetting Committee reviews application.", "actor": "NCPWD"},
            {"step_number": 5, "description": "NCPWD issues the Disability ID Card.", "actor": "NCPWD"}
        ]
    },
    "NGO COORDINATING": {
        "narrative": "NGO Registration involves name reservation, vetting, and certification. (Updated with standard NGO Board workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant conducts Name Search and Reservation at NGO Board.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant submits Form 1 (Application) with Constitution and Minutes.", "actor": "Applicant"},
            {"step_number": 3, "description": "NGO Board conducts background checks (National Intelligence).", "actor": "NGO Board"},
            {"step_number": 4, "description": "Applicant pays registration fees.", "actor": "Applicant"},
            {"step_number": 5, "description": "NGO Board issues Certificate of Registration.", "actor": "NGO Board"}
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
