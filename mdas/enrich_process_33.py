
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirty-fourth process (index 33)
process = data['processes'][33]

# Populate fields
process['executive_summary'] = "The State Department for Public Health and Professional Standards in Kenya, operating under the Ministry of Health, is tasked with ensuring the well-being of the Kenyan population. Its overarching goal is to achieve a nation free from preventable diseases and ill health through primary healthcare interventions, accelerating Universal Health Coverage (UHC), and contributing to Sustainable Development Goals (SDGs)."
process['process_overview']['process_objective'] = "To develop and implement policies for public health and sanitation, oversee preventive and promotive health services, strengthen disease surveillance and preparedness, scale up community health interventions, and ensure functional primary healthcare networks to achieve a nation free from preventable diseases and ill health through primary healthcare interventions."
process['process_overview']['policy_legal_context'].append("Operates under the Ministry of Health, guided by the Kenya Health Policy 2014-2030. Its mandate is underpinned by various acts and regulations related to public health (e.g., Public Health Act), disease control, food safety, and professional standards in healthcare. (INFERRED: This forms the comprehensive legal and policy framework for public health.)")
process['stakeholders'].append({"stakeholder": "Kenyan Population", "role": "Primary beneficiaries of public health interventions and health promotion efforts", "responsibilities": "(INFERRED) Participating in public health programs, adopting healthy lifestyles."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Key partners in scaling up community health interventions and promotion", "responsibilities": "(INFERRED) Engaging with community health workers, participating in local health initiatives."})
process['stakeholders'].append({"stakeholder": "Healthcare Professionals", "role": "Providers of public health services and expertise", "responsibilities": "(INFERRED) Delivering preventive and promotive services, adhering to professional standards."})
process['stakeholders'].append({"stakeholder": "Ministry of Health", "role": "Parent Ministry providing overall policy direction and oversight for health sector", "responsibilities": "(INFERRED) Setting national health agenda, resource allocation, coordinating health sector activities."})
process['stakeholders'].append({"stakeholder": "County Health Departments", "role": "Implementers of public health programs at the county level", "responsibilities": "(INFERRED) Delivering public health services, managing local health initiatives."})
process['stakeholders'].append({"stakeholder": "International Health Organizations", "role": "Partners in global health initiatives, technical support, and funding", "responsibilities": "(INFERRED) Collaborating on disease control, supporting public health programs."})

process['as_is_narrative'] = "(INFERRED) The State Department for Public Health operates by developing and enforcing public health policies and standards, overseeing preventive and promotive health campaigns (e.g., immunization), strengthening disease surveillance and response mechanisms (including outbreak detection and Rapid Response Teams), managing health education programs, administering quarantine measures, ensuring food quality and hygiene, and providing technical support and guidance to county health departments to scale up primary healthcare interventions across Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from official sources) / medium (inferred legal acts, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://health.go.ke/"
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirty-fourth process enriched and combined_data.json updated.")
