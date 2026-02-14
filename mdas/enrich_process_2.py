
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the third process (index 2)
process = data['processes'][2]

# Populate fields
process['executive_summary'] = "The Office of the Data Protection Commissioner (ODPC) in Kenya is responsible for regulating the processing of personal data, protecting individual privacy, and ensuring compliance with the Data Protection Act, 2019. It acts as an oversight body, promotes self-regulation, and investigates data protection infringements."
process['process_overview']['process_objective'] = "To oversee and enforce the implementation of the Data Protection Act, 2019, ensuring appropriate handling of personal data, protecting the privacy of individuals, and establishing robust legal and institutional mechanisms for data protection in Kenya."
process['process_overview']['policy_legal_context'].append("Established and mandated under the Data Protection Act, 2019, which provides the legal framework for personal data protection in Kenya.")
process['stakeholders'].append({"stakeholder": "Data Subjects (Individuals)", "role": "Rights holders whose personal data is processed", "responsibilities": "(INFERRED) Understanding and exercising their data protection rights."})
process['stakeholders'].append({"stakeholder": "Data Controllers", "role": "Entities that determine the purpose and means of processing personal data", "responsibilities": "(INFERRED) Ensuring compliance with the Data Protection Act, registering with ODPC."})
process['stakeholders'].append({"stakeholder": "Data Processors", "role": "Entities that process personal data on behalf of a data controller", "responsibilities": "(INFERRED) Processing data according to instructions, adhering to security measures."})
process['stakeholders'].append({"stakeholder": "Public and Private Bodies", "role": "Entities that process personal data in their operations", "responsibilities": "(INFERRED) Complying with data protection principles and regulations."})
process['stakeholders'].append({"stakeholder": "International Data Protection Bodies", "role": "Collaborators in international data protection matters", "responsibilities": "(INFERRED) Promoting cross-border data protection cooperation."})

process['as_is_narrative'] = "(INFERRED) The ODPC implements its mandate by registering data controllers/processors, conducting assessments and inspections, investigating complaints from data subjects, issuing enforcement notices, promoting public awareness of data protection rights, and fostering international cooperation on data protection."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = ["https://odpc.go.ke/"]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Third process enriched and combined_data.json updated.")
