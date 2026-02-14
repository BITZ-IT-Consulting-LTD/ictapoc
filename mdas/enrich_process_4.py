
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifth process (index 4)
process = data['processes'][4]

# Populate fields
process['executive_summary'] = "The State Department for Immigration and Citizen Services in Kenya controls and regulates the entry, exit, and residency of individuals, manages citizenship, and provides related services. It is responsible for issuing passports and other travel documents, as well as maintaining population registers for citizens and foreign nationals."
process['process_overview']['process_objective'] = "To control and regulate immigration, manage citizenship applications, issue travel and identification documents, and ensure secure and efficient citizen services in accordance with national laws and policies."
process['process_overview']['policy_legal_context'].append("Mandate derived from Chapter 3 of the Constitution of Kenya 2010, the Kenya Citizenship and Immigration Act, 2011, and the Kenya Citizenship and Immigration Regulations, 2012. Other relevant laws and policies also apply.")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Recipients of passport, citizenship, and identification services", "responsibilities": "(INFERRED) Complying with application requirements, adhering to immigration laws."})
process['stakeholders'].append({"stakeholder": "Foreign Nationals", "role": "Subjects of immigration control, residency, and work permit services", "responsibilities": "(INFERRED) Complying with visa, permit, and residency regulations."})
process['stakeholders'].append({"stakeholder": "Other Government Agencies", "role": "Collaborators in national security, data collection, and enforcement", "responsibilities": "(INFERRED) Sharing information, cooperating on border security and data management."})

process['as_is_narrative'] = "(INFERRED) The Department operates by manning points of entry/exit, processing applications for passports, visas, permits, and citizenship, registering non-citizens, enforcing immigration laws, and managing the Integrated Population Registration System to maintain a national population register."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = ["https://immigration.go.ke/", "https://ecitizen.go.ke/"]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifth process enriched and combined_data.json updated.")
