import json
import sys

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

updates = {
    "HUDUMA SECRETARIAT": {
        "narrative": "Huduma Centres provide a one-stop-shop for government services via a queuing and counter service model. (Updated with standard Huduma Centre workflow).",
        "steps": [
            {"step_number": 1, "description": "Citizen visits Huduma Centre and undergoes security check.", "actor": "Citizen"},
            {"step_number": 2, "description": "Citizen proceeds to the Information Desk for guidance and ticket issuance.", "actor": "Citizen"},
            {"step_number": 3, "description": "Citizen waits in the waiting area until their ticket number is called/displayed.", "actor": "Citizen"},
            {"step_number": 4, "description": "Citizen proceeds to the designated counter for service (e.g., ID replacement, NHIF).", "actor": "Citizen"},
            {"step_number": 5, "description": "Huduma Agent serves the citizen (verification, processing, or referral).", "actor": "Huduma Agent"},
            {"step_number": 6, "description": "Citizen makes payment via M-Pesa/Posta Pay if applicable.", "actor": "Citizen"},
            {"step_number": 7, "description": "Citizen provides feedback on service quality via the terminal.", "actor": "Citizen"}
        ]
    },
    "EXPORT PROCESSING ZONES AUTHORITY": {
        "narrative": "EPZ Enterprise licensing involves proposal evaluation, investment appraisal, and licensing for export-oriented businesses. (Updated with standard EPZA workflow).",
        "steps": [
            {"step_number": 1, "description": "Investor submits a project proposal and application form to EPZA.", "actor": "Investor"},
            {"step_number": 2, "description": "EPZA appraises the project (investment capital, export market, employment creation).", "actor": "EPZA"},
            {"step_number": 3, "description": "Upon approval, EPZA issues a Letter of Offer.", "actor": "EPZA"},
            {"step_number": 4, "description": "Investor accepts offer and pays the annual license fee.", "actor": "Investor"},
            {"step_number": 5, "description": "EPZA issues the EPZ Enterprise License.", "actor": "EPZA"}
        ]
    },
    "KENYA AIRPORTS AUTHORITY": {
        "narrative": "Airport Security Pass issuance involves strict vetting and application through the KAA security department. (Updated with standard KAA workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant/Employer submits security pass application letter to Airport Manager.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant fills the security pass application form and attaches ID/Good Conduct Cert.", "actor": "Applicant"},
            {"step_number": 3, "description": "KAA Security conducts vetting and background checks.", "actor": "KAA Security"},
            {"step_number": 4, "description": "Upon approval, applicant pays the requisite fee.", "actor": "Applicant"},
            {"step_number": 5, "description": "Pass is printed and issued to the applicant.", "actor": "KAA"}
        ]
    },
    "KENYA CIVIL AVIATION AUTHORITY": {
        "narrative": "Drone (RPAS) registration involves importation approval, registration, and operator certification. (Updated with standard KCAA workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant applies for a permit to import the drone (RPAS).", "actor": "Applicant"},
            {"step_number": 2, "description": "KCAA inspects and registers the drone upon arrival.", "actor": "KCAA"},
            {"step_number": 3, "description": "Applicant undergoes training at an approved ATO for Remote Pilot License (RPL).", "actor": "Applicant"},
            {"step_number": 4, "description": "Applicant applies for Remote Operator's Certificate (ROC) if for commercial use.", "actor": "Applicant"},
            {"step_number": 5, "description": "KCAA issues the certificate/license.", "actor": "KCAA"}
        ]
    },
    "KENYA FILM CLASSIFICATION BOARD": {
        "narrative": "Film licensing and classification ensures content compliance with national standards. (Updated with standard KFCB workflow).",
        "steps": [
            {"step_number": 1, "description": "Filmmaker applies for filming license via KFCB portal.", "actor": "Filmmaker"},
            {"step_number": 2, "description": "Filmmaker submits script/synopsis for examination.", "actor": "Filmmaker"},
            {"step_number": 3, "description": "KFCB reviews content and assigns age rating/classification.", "actor": "KFCB"},
            {"step_number": 4, "description": "Filmmaker pays the classification and licensing fees.", "actor": "Filmmaker"},
            {"step_number": 5, "description": "KFCB issues the Filming License and Classification Certificate.", "actor": "KFCB"}
        ]
    },
    "KENYA INDUSTRIAL PROPERTY INSTITUTE": {
        "narrative": "Trademark registration protects intellectual property through search, examination, and advertisement. (Updated with standard KIPI workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant conducts a trademark search (Form TM27) to ensure uniqueness.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant files application for registration (Form TM2) and pays fee.", "actor": "Applicant"},
            {"step_number": 3, "description": "KIPI conducts formal and substantive examination.", "actor": "KIPI"},
            {"step_number": 4, "description": "If approved, the mark is advertised in the Industrial Property Journal for 60 days.", "actor": "KIPI"},
            {"step_number": 5, "description": "If no opposition, applicant pays registration fee.", "actor": "Applicant"},
            {"step_number": 6, "description": "KIPI issues Certificate of Registration.", "actor": "KIPI"}
        ]
    },
    "KENYA MARITIME AUTHORITY": {
        "narrative": "Seafarer certification ensures maritime personnel meet STCW standards. (Updated with standard KMA workflow).",
        "steps": [
            {"step_number": 1, "description": "Seafarer undergoes mandatory training at an approved maritime institution.", "actor": "Seafarer"},
            {"step_number": 2, "description": "Seafarer applies to KMA for Certificate of Competency (CoC) or Proficiency.", "actor": "Seafarer"},
            {"step_number": 3, "description": "Seafarer undergoes medical fitness examination.", "actor": "Seafarer"},
            {"step_number": 4, "description": "KMA verifies training and medical records.", "actor": "KMA"},
            {"step_number": 5, "description": "KMA conducts oral/written examination (for officers).", "actor": "KMA"},
            {"step_number": 6, "description": "KMA issues the Seafarer Certificate.", "actor": "KMA"}
        ]
    },
    "KENYA PLANT HEALTH INSPECTORATE SERVICES": {
        "narrative": "Phytosanitary certification is required for exporting plant materials, involving inspection and lab testing. (Updated with standard KEPHIS workflow).",
        "steps": [
            {"step_number": 1, "description": "Exporter registers as a client on the KEPHIS ECS portal.", "actor": "Exporter"},
            {"step_number": 2, "description": "Exporter applies for Phytosanitary Certificate for a specific consignment.", "actor": "Exporter"},
            {"step_number": 3, "description": "KEPHIS inspector inspects the consignment at the packhouse/exit point.", "actor": "KEPHIS Inspector"},
            {"step_number": 4, "description": "Samples may be taken for laboratory analysis.", "actor": "KEPHIS Lab"},
            {"step_number": 5, "description": "Upon compliance, Exporter pays inspection fees.", "actor": "Exporter"},
            {"step_number": 6, "description": "KEPHIS issues the Phytosanitary Certificate.", "actor": "KEPHIS"}
        ]
    },
    "NATIONAL CONSTRUCTION AUTHORITY": {
        "narrative": "Project registration ensures construction sites are compliant and pay the NCA levy. (Updated with standard NCA workflow).",
        "steps": [
            {"step_number": 1, "description": "Developer/Contractor logs into NCA portal.", "actor": "Developer"},
            {"step_number": 2, "description": "Developer registers the project details (contractor, consultants, value).", "actor": "Developer"},
            {"step_number": 3, "description": "System calculates the Construction Levy (0.5% for projects >5M).", "actor": "System"},
            {"step_number": 4, "description": "Developer pays the levy.", "actor": "Developer"},
            {"step_number": 5, "description": "NCA conducts compliance inspection.", "actor": "NCA"},
            {"step_number": 6, "description": "NCA issues Compliance Certificate.", "actor": "NCA"}
        ]
    },
    "ENERGY AND PETROLEUM REGULATORY AUTHORITY": {
        "narrative": "Licensing for solar technicians and electrical contractors is digital via the EPRA portal. (Updated with standard EPRA workflow).",
        "steps": [
            {"step_number": 1, "description": "Applicant logs into EPRA License Management System.", "actor": "Applicant"},
            {"step_number": 2, "description": "Applicant selects license type (e.g., Solar PV T1/T2) and uploads academic certs.", "actor": "Applicant"},
            {"step_number": 3, "description": "Applicant pays the application fee.", "actor": "Applicant"},
            {"step_number": 4, "description": "EPRA reviews application and invites applicant for interview/exam.", "actor": "EPRA"},
            {"step_number": 5, "description": "Upon passing, applicant pays grant fee.", "actor": "Applicant"},
            {"step_number": 6, "description": "EPRA issues the License.", "actor": "EPRA"}
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
