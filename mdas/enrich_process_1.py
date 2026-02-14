
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the second process (index 1)
process = data['processes'][1]

# Populate fields
process['executive_summary'] = "The Office of the Attorney General (OAG) in Kenya serves as the principal legal advisor to the National Government, upholding the rule of law and ensuring equal access to justice. It represents the government in legal proceedings, safeguards the Constitution, and promotes good governance and human rights."
process['process_overview']['process_objective'] = "To provide comprehensive legal advice to the national government, represent it in legal proceedings (excluding criminal cases), and promote, protect, and uphold the rule of law and access to justice for all Kenyans."
process['process_overview']['policy_legal_context'].append("Mandated under Article 156 of the Constitution of Kenya, 2010. Discharges functions of a Cabinet Secretary in relation to the Department of Justice, pursuant to Executive Order No. 2 of 2013.")
process['stakeholders'].append({"stakeholder": "National Government of Kenya", "role": "Client; recipient of legal advice and representation", "responsibilities": "(INFERRED) Seeking legal counsel, adhering to legal frameworks."})
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Beneficiaries of the rule of law, human rights, and access to justice", "responsibilities": "(INFERRED) Upholding laws, seeking justice."})
process['stakeholders'].append({"stakeholder": "Legal Sector Institutions", "role": "Collaborators in justice administration", "responsibilities": "(INFERRED) Adhering to legal standards, cooperating on legal reforms."})

process['as_is_narrative'] = "(INFERRED) The OAG operates by providing legal opinions to government entities, representing them in civil suits, reviewing legislation, and advising on international legal matters, all aimed at ensuring adherence to the Constitution and promotion of justice."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, constitutional basis) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = ["https://ag.go.ke/", "https://vellum.co.ke/", "https://afro.co.ke/", "https://en.wikipedia.org/wiki/Attorney_General_of_Kenya"]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Second process enriched and combined_data.json updated.")
