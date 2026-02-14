
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighteenth process (index 17)
process = data['processes'][17]

# Populate fields
process['executive_summary'] = "The National Transport and Safety Authority (NTSA) is a Kenyan government agency focused on continually improving the accessibility and safety of the country's road transport system. It provides comprehensive online services for individuals, vehicles, and transport service providers, and regulates various aspects of road transport to enhance road safety for all."
process['process_overview']['process_objective'] = "To ensure an accessible and safe road transport system in Kenya by regulating driver and vehicle licensing, managing vehicle registration and transfers, overseeing transport service providers, and implementing road safety initiatives to reduce road accidents and fatalities."
process['process_overview']['policy_legal_context'].append("NTSA operates under specific legislation governing road transport and safety in Kenya, primarily the National Transport and Safety Authority Act, which establishes its mandate and functions. (INFERRED: This Act provides the legal framework for its regulatory and enforcement activities.)")
process['stakeholders'].append({"stakeholder": "Individual Road Users (Drivers, Passengers, Pedestrians)", "role": "Primary subjects of NTSA's safety regulations and beneficiaries of a safe road system", "responsibilities": "(INFERRED) Adhering to traffic laws, obtaining proper licenses, practicing safe road behavior."})
process['stakeholders'].append({"stakeholder": "Vehicle Owners", "role": "Subjects of vehicle registration, inspection, and transfer regulations", "responsibilities": "(INFERRED) Registering vehicles, ensuring roadworthiness, complying with ownership transfer rules."})
process['stakeholders'].append({"stakeholder": "Transport Service Providers (Operators, Dealers, Garages)", "role": "Entities regulated and licensed by NTSA to provide transport-related services", "responsibilities": "(INFERRED) Obtaining licenses, adhering to operational standards, ensuring vehicle safety."})
process['stakeholders'].append({"stakeholder": "Organizations with Fleets", "role": "Entities managing multiple vehicles; subjects of fleet management regulations", "responsibilities": "(INFERRED) Complying with fleet safety standards, ensuring drivers are licensed and vehicles are maintained."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Transport)", "role": "Parent Ministry providing oversight and policy direction", "responsibilities": "(INFERRED) Policy formulation, resource allocation, strategic guidance for NTSA."})

process['as_is_narrative'] = "(INFERRED) NTSA's operations involve developing and implementing road safety policies, providing online and physical services for driver licensing (including Smart DL), vehicle registration and transfer, regulating speed limiters, issuing licenses for dealers and garages, conducting conformity assessments for vehicles, and overseeing transport network companies. It also conducts road safety campaigns and enforces traffic laws to achieve its objective of safer roads."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (functions from official website) / medium (inferred legal context, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://ntsa.go.ke/",
    "https://ecitizen.go.ke/" # For integration context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighteenth process enriched and combined_data.json updated.")
