
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fourth process (index 3)
process = data['processes'][3]

# Populate fields
process['executive_summary'] = "The Huduma Secretariat Kenya is mandated to transform public service delivery, providing efficient, effective, accessible, and citizen-centric services through integrated 'one-stop-shop' platforms like Huduma Centres and Huduma E-Services. It's a flagship project under Kenya Vision 2030."
process['process_overview']['process_objective'] = "To develop, operationalize, support, and maintain integrated government service platforms (Huduma Centres, Huduma E-Services, Contact Centre) to provide quality, accessible, dignified, and convenient public services to Kenyan citizens from various government entities."
process['process_overview']['policy_legal_context'].append("A flagship project under Kenya Vision 2030 Medium-Term Plan II (2013-2017). Operates under the Ministry of Public Service and Gender, State Department for Public Service. (INFERRED: Specific policy and legislative frameworks exist for the establishment, operationalization, and management of these one-stop-shop government services.)")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Primary beneficiaries and recipients of public services", "responsibilities": "(INFERRED) Utilizing services, providing feedback for improvement."})
process['stakeholders'].append({"stakeholder": "Government Ministries, Departments, Agencies, and Counties", "role": "Service providers and partners whose services are integrated into Huduma platforms", "responsibilities": "(INFERRED) Integrating services, collaborating on process re-engineering, providing data."})
process['stakeholders'].append({"stakeholder": "Ministry of Public Service and Gender", "role": "Parent Ministry providing oversight and strategic direction", "responsibilities": "(INFERRED) Policy guidance, resource allocation, performance monitoring."})

process['as_is_narrative'] = "(INFERRED) The Huduma Secretariat develops and maintains integrated service platforms, coordinates daily operations of Huduma Centres, implements customer relationship management, and drives digitization and re-engineering of public service processes to enhance efficiency and citizen access."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = ["https://hudumakenya.go.ke/"]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fourth process enriched and combined_data.json updated.")
