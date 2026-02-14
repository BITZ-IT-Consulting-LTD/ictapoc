
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixteenth process (index 15)
process = data['processes'][15]

# Populate fields
process['executive_summary'] = "The State Department for Lands and Physical Planning in Kenya plays a crucial role in the country's socio-economic development by overseeing land administration, physical planning, and land use management. Its mission is to facilitate improved livelihoods through efficient land administration, equitable access, secure tenure, and sustainable management of land resources."
process['process_overview']['process_objective'] = "To develop and implement national lands policy, facilitate physical planning for optimal land use, conduct land adjudication and registration, provide survey and mapping services, perform land and property valuation, and maintain a comprehensive public land bank to ensure secure tenure and sustainable land management in Kenya."
process['process_overview']['policy_legal_context'].append("Mandate outlined in Executive Order No. 2 of November 2023. Operates under various land-related legislations including, but not limited to, the Land Act, Land Registration Act, Physical Planning Act, and relevant constitutional provisions regarding land. (INFERRED: The specific Acts are numerous and constitute the legal framework.)")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Landowners, land applicants, and beneficiaries of land services and secure tenure", "responsibilities": "(INFERRED) Complying with land laws, seeking legitimate land services."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in physical planning and land use management", "responsibilities": "(INFERRED) Coordinating physical planning at county level, implementing national land policies."})
process['stakeholders'].append({"stakeholder": "Land Developers", "role": "Entities involved in land utilization and development", "responsibilities": "(INFERRED) Adhering to physical planning regulations, contributing to urban and rural development."})
process['stakeholders'].append({"stakeholder": "Surveyors", "role": "Professionals providing land surveying and mapping services", "responsibilities": "(INFERRED) Conducting accurate land surveys, collaborating with the Department on mapping."})
process['stakeholders'].append({"stakeholder": "Valuers", "role": "Professionals providing land and property valuation services", "responsibilities": "(INFERRED) Conducting impartial valuations for various purposes."})
process['stakeholders'].append({"stakeholder": "Registrars", "role": "Officials responsible for land registration and record-keeping", "responsibilities": "(INFERRED) Maintaining accurate land registries, processing land transactions."})
process['stakeholders'].append({"stakeholder": "Environmental Agencies", "role": "Partners in ensuring sustainable land use and environmental protection", "responsibilities": "(INFERRED) Collaborating on environmental impact assessments for land projects."})

process['as_is_narrative'] = "(INFERRED) The State Department's operations encompass formulating land policies, providing physical planning advisory services, conducting land adjudication and settlement programs, carrying out land surveying and mapping, administering public and private land, performing property valuations for various purposes, and registering land transactions and other legal documents related to land. It also involves digitization of land records and decentralization of land management services."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from official sources) / medium (inferred legal acts, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://lands.go.ke/",
    "https://developmentaid.org/" # Though not primary, provided useful context in search
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixteenth process enriched and combined_data.json updated.")
