
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighth process (index 7)
process = data['processes'][7]

# Populate fields
process['executive_summary'] = "The State Department for Public Service and Human Capital in Kenya is responsible for national and sectoral development planning, human resource management within the public service, and overseeing critical functions like national statistics, census, population policy, and Sustainable Development Goals (SDGs) coordination."
process['process_overview']['process_objective'] = "To provide policy direction and management for human resources in the public service, coordinate national and sectoral development planning, and ensure effective implementation, monitoring, and evaluation of various government initiatives, including SDGs and public investment."
process['process_overview']['policy_legal_context'].append("Functions outlined in Executive Order No. 1 of January 14, 2020 (revised in May 2020).")
process['stakeholders'].append({"stakeholder": "Public Servants", "role": "Beneficiaries of HR policies and development programs", "responsibilities": "(INFERRED) Adhering to public service values, participating in development initiatives."})
process['stakeholders'].append({"stakeholder": "Other Government Ministries, Departments, and Agencies", "role": "Collaborators in national planning, HR management, and implementation of government programs", "responsibilities": "(INFERRED) Aligning with national development plans, implementing HR policies."})
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Ultimate beneficiaries of efficient public service and national development outcomes", "responsibilities": "(INFERRED) Engaging with public services, contributing to national development."})
process['stakeholders'].append({"stakeholder": "Human Resources Management Professionals Examinations Board (HRMPEB)", "role": "Institution operating under the State Department for professional development", "responsibilities": "(INFERRED) Developing HR curricula, examining and certifying HR professionals."})

process['as_is_narrative'] = "(INFERRED) The State Department engages in formulating national development plans, developing and implementing HR policies for the public service, managing specific funds like the National Government Constituency Development Fund, overseeing national statistics and census activities, and coordinating the monitoring and evaluation of economic trends and SDGs."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (executive order, specific functions) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = ["https://devolution.go.ke/", "https://parliament.go.ke/", "https://the-star.co.ke/", "https://hrmpeb.or.ke/"]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighth process enriched and combined_data.json updated.")
