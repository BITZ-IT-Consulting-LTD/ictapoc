import json
import sys

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

updates = {
    "AVIATION": {
        "narrative": "Drone (RPAS) registration and import approval involves strict regulatory compliance for safety and security. (Updated with standard KCAA workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant applies for a permit to import the drone (RPAS) via KCAA email/portal.", "actor": "Applicant"},
            {"step_number": 2, "description": "KCAA inspects and registers the drone upon arrival in the country.", "actor": "KCAA"},
            {"step_number": 3, "description": "Applicant undergoes training at an approved ATO for Remote Pilot License (RPL).", "actor": "Applicant"},
            {"step_number": 4, "description": "Applicant applies for Remote Operator's Certificate (ROC) if for commercial use.", "actor": "Applicant"},
            {"step_number": 5, "description": "KCAA issues the certificate/license upon payment of fees.", "actor": "KCAA"}
        ]
    },
    "MEDICAL PRACTITIONERS AND DENTISTS": {
        "narrative": "Medical practitioner licensing is fully digital via the KMPDC Online Services Portal. (Updated with standard KMPDC workflow).",
        "steps": [
            {"step_number": 1, "description": "Practitioner logs into the KMPDC Portal (osp.kmpdc.go.ke).", "actor": "Practitioner"},
            {"step_number": 2, "description": "Practitioner updates CPD (Continuous Professional Development) points.", "actor": "Practitioner"},
            {"step_number": 3, "description": "Practitioner applies for Annual Retention/Practice License.", "actor": "Practitioner"},
            {"step_number": 4, "description": "Practitioner pays the annual retention fee via M-Pesa.", "actor": "Practitioner"},
            {"step_number": 5, "description": "System generates and emails the Annual Practice License.", "actor": "System"}
        ]
    },
    "PHARMACY AND POISONS": {
        "narrative": "Importation of pharmaceuticals requires an Import Permit via the PPB Trade Portal. (Updated with standard PPB workflow).",
        "steps": [
            {"step_number": 1, "description": "Importer logs into the PPB Online Portal.", "actor": "Importer"},
            {"step_number": 2, "description": "Importer applies for an Import Permit and uploads the Proforma Invoice.", "actor": "Importer"},
            {"step_number": 3, "description": "PPB verifies the product registration status and invoice details.", "actor": "PPB Officer"},
            {"step_number": 4, "description": "Importer pays the permit fee (e.g., 2% of FOB value).", "actor": "Importer"},
            {"step_number": 5, "description": "PPB approves and issues the electronic Import Permit.", "actor": "PPB"}
        ]
    },
    "VETERINARY BOARD": {
        "narrative": "Veterinary surgeon retention is managed online, requiring proof of CPD compliance. (Updated with standard KVB workflow).",
        "steps": [
            {"step_number": 1, "description": "Vet Surgeon logs into the KVB Portal.", "actor": "Vet Surgeon"},
            {"step_number": 2, "description": "Applicant uploads proof of CPD points and Good Standing.", "actor": "Vet Surgeon"},
            {"step_number": 3, "description": "Applicant applies for Annual Retention.", "actor": "Vet Surgeon"},
            {"step_number": 4, "description": "Applicant pays the retention fee.", "actor": "Vet Surgeon"},
            {"step_number": 5, "description": "KVB issues the Annual Retention Certificate.", "actor": "KVB"}
        ]
    },
    "VOCATIONAL EDUCATION AND TRAINING AUTHORITY": {
        "narrative": "TVET Institution accreditation involves self-assessment, peer review, and physical inspection. (Updated with standard TVETA workflow).",
        "steps": [
            {"step_number": 1, "description": "Institution applies for registration/accreditation via TVETA MIS.", "actor": "Institution"},
            {"step_number": 2, "description": "Institution conducts and submits a Self-Assessment Report.", "actor": "Institution"},
            {"step_number": 3, "description": "TVETA conducts desk review of the application.", "actor": "TVETA"},
            {"step_number": 4, "description": "TVETA conducts physical inspection of facilities and curriculum.", "actor": "TVETA Inspectors"},
            {"step_number": 5, "description": "TVETA Board approves accreditation and issues Certificate.", "actor": "TVETA Board"}
        ]
    },
    "CEREALS AND PRODUCE": {
        "narrative": "Fertilizer subsidy distribution uses an e-voucher system linked to farmer registration. (Updated with standard NCPB workflow).",
        "steps": [
            {"step_number": 1, "description": "Farmer registers with the Ministry of Agriculture (Chief/Assistant Chief).", "actor": "Farmer"},
            {"step_number": 2, "description": "Data is digitized into the KIAMIS system.", "actor": "MoA"},
            {"step_number": 3, "description": "Farmer receives an e-voucher SMS for subsidized fertilizer.", "actor": "System"},
            {"step_number": 4, "description": "Farmer visits designated NCPB depot or KNTC store.", "actor": "Farmer"},
            {"step_number": 5, "description": "Farmer pays the subsidized amount via M-Pesa.", "actor": "Farmer"},
            {"step_number": 6, "description": "Farmer collects the fertilizer.", "actor": "Farmer"}
        ]
    },
    "DAIRY BOARD": {
        "narrative": "Milk Trader licensing ensures hygiene and quality standards in the dairy value chain. (Updated with standard KDB workflow).",
        "steps": [
            {"step_number": 1, "description": "Trader applies for license via KDB portal.", "actor": "Trader"},
            {"step_number": 2, "description": "KDB inspectors inspect the premises/vehicle/containers.", "actor": "KDB Inspector"},
            {"step_number": 3, "description": "Upon compliance, trader pays the license fee.", "actor": "Trader"},
            {"step_number": 4, "description": "KDB issues the Milk Trader License.", "actor": "KDB"}
        ]
    },
    "AGRICULTURE AND FOOD AUTHORITY": {
        "narrative": "Crop dealer and export licensing is centralized under AFA's IMIS system. (Updated with standard AFA workflow).",
        "steps": [
            {"step_number": 1, "description": "Dealer registers on AFA IMIS portal.", "actor": "Dealer"},
            {"step_number": 2, "description": "Dealer applies for Export/Import/Dealer License for specific crop (e.g., Coffee, Tea, Horticulture).", "actor": "Dealer"},
            {"step_number": 3, "description": "AFA conducts verification (documentary and physical if needed).", "actor": "AFA"},
            {"step_number": 4, "description": "Dealer pays the license/cess fees.", "actor": "Dealer"},
            {"step_number": 5, "description": "AFA issues the Permit/License.", "actor": "AFA"}
        ]
    },
    "IRRIGATION AUTHORITY": {
        "narrative": "Tenant farmer management in irrigation schemes involves registration and water fee payment. (Updated with standard NIA workflow).",
        "steps": [
            {"step_number": 1, "description": "Farmer applies for plot allocation/water service at Scheme Office.", "actor": "Farmer"},
            {"step_number": 2, "description": "Scheme Manager verifies availability and eligibility.", "actor": "NIA"},
            {"step_number": 3, "description": "Farmer signs Tenancy Agreement.", "actor": "Farmer"},
            {"step_number": 4, "description": "Farmer pays Operation & Maintenance (O&M) fees.", "actor": "Farmer"},
            {"step_number": 5, "description": "NIA releases water to the farmer's plot.", "actor": "NIA"}
        ]
    },
    "COMMISSION FOR UNIVERSITY EDUCATION": {
        "narrative": "Recognition and Equation of Qualifications involves verifying foreign degrees for local validity. (Updated with standard CUE workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant applies via CUE Portal (rev.cue.or.ke).", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant uploads certified copies of certificates and transcripts.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant pays the processing fee.", "actor": "Applicant"},
            {"step_number": 4, "description": "CUE verifies authenticity with the awarding institution/foreign regulator.", "actor": "CUE"},
            {"step_number": 5, "description": "CUE issues the Recognition and Equation Letter.", "actor": "CUE"}
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
