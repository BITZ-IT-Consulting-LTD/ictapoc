import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

steps = [
  { "step_number": 1, "description": "Applicant logs into the eCitizen portal (www.ecitizen.go.ke) and navigates to the Department of Immigration Services section.", "actor": "Applicant" },
  { "step_number": 2, "description": "Applicant fills the online passport application form, providing personal details, parents' details, and next of kin information.", "actor": "Applicant" },
  { "step_number": 3, "description": "Applicant uploads scanned copies of required documents (National ID, Birth Certificate, Recommender's ID, Parents' IDs).", "actor": "Applicant" },
  { "step_number": 4, "description": "Applicant pays the prescribed passport fee via mobile money (M-Pesa), credit card, or bank transfer on the eCitizen platform.", "actor": "Applicant" },
  { "step_number": 5, "description": "System generates a payment receipt and a pre-filled application form, which the applicant must download and print.", "actor": "System" },
  { "step_number": 6, "description": "Applicant schedules a biometric appointment date and time at a preferred Immigration Center.", "actor": "Applicant" },
  { "step_number": 7, "description": "Applicant physically presents themselves at the Immigration Center on the appointed date with original documents and printed application forms.", "actor": "Applicant" },
  { "step_number": 8, "description": "Immigration Officer verifies original documents against the application and captures applicant's biometrics (fingerprints, photo, signature).", "actor": "Immigration Officer" },
  { "step_number": 9, "description": "Application undergoes internal processing, security vetting, and approval.", "actor": "Immigration Department" },
  { "step_number": 10, "description": "Passport is printed and dispatched to the collection desk.", "actor": "Immigration Department" },
  { "step_number": 11, "description": "Applicant receives an SMS notification and collects the passport in person upon verification of identity.", "actor": "Applicant" }
]

try:
    with open(file_path, 'r') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    
    updated = False
    for item in items:
        if 'IMMIGRATION' in item.get('mda_name', '').upper():
            item['as_is_steps'] = steps
            item['as_is_narrative'] = "The passport application process is largely digitized via the eCitizen platform for submission and payment, but requires physical presence for biometric capture and collection. (Updated with specific e-Passport workflow steps)."
            updated = True
            print(f"Updated object: {item['mda_name']}")
            break
    
    if updated:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print("Successfully wrote changes to file.")
    else:
        print("Could not find Immigration object to update.")

except Exception as e:
    print(f"Error: {e}")
