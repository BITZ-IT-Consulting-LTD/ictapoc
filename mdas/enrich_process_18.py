
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the nineteenth process (index 18)
process = data['processes'][18]

# Populate fields
process['executive_summary'] = "The State Department for Mining in Kenya is responsible for formulating policies for the extractive industry, overseeing mineral exploration, and managing mining activities. It aims to promote mineral value addition, ensure health and safety in mines, and develop the mining sector's capacity to contribute to national development."
process['process_overview']['process_objective'] = "To develop and implement policies for mineral exploration and exploitation, manage quarrying activities, maintain geological data, ensure and enforce health and safety standards in mines, and promote mineral value addition to optimize the benefits from Kenya's mineral resources for sustainable national development."
process['process_overview']['policy_legal_context'].append("Mandate established by Executive Order No. 1 of 2018 (revised). Operates under the Mining Act and other relevant legislations governing mineral exploration, extraction, management, and environmental protection in Kenya. (INFERRED: These acts form the comprehensive legal framework for the mining sector.)")
process['stakeholders'].append({"stakeholder": "Mining Companies/Investors", "role": "Entities engaged in mineral exploration and extraction", "responsibilities": "(INFERRED) Complying with mining laws, investing responsibly, ensuring environmental protection."})
process['stakeholders'].append({"stakeholder": "Artisanal Miners", "role": "Small-scale miners involved in mineral extraction", "responsibilities": "(INFERRED) Adhering to safety standards, participating in regulated mining activities."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Communities impacted by mining activities; beneficiaries of sustainable resource management", "responsibilities": "(INFERRED) Engaging in consultations, benefiting from community development projects."})
process['stakeholders'].append({"stakeholder": "National Mining Corporation (NMC)", "role": "Institution under its oversight for strategic mineral development", "responsibilities": "(INFERRED) Strategic exploration, investment in mining ventures."})
process['stakeholders'].append({"stakeholder": "Mineral Rights Board (MRB)", "role": "Institution under its oversight for granting and managing mineral rights", "responsibilities": "(INFERRED) Advising on mineral rights, ensuring fair allocation."})
process['stakeholders'].append({"stakeholder": "Geologist Registration Board (GRB)", "role": "Institution under its oversight for regulating geological professionals", "responsibilities": "(INFERRED) Registering geologists, ensuring professional standards."})
process['stakeholders'].append({"stakeholder": "Environmental Agencies", "role": "Collaborators in ensuring environmental protection in mining areas", "responsibilities": "(INFERRED) Overseeing environmental impact assessments, enforcing environmental regulations."})

process['as_is_narrative'] = "(INFERRED) The State Department operates by formulating mining policies and strategies, undertaking mineral exploration and inventory mapping, maintaining and disseminating geological data, regulating and managing quarrying activities, inspecting mines for health and safety compliance, promoting capacity development in the mining sector, and fostering mineral value addition. It also engages with various stakeholders to ensure responsible and sustainable exploitation of mineral resources."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from official sources) / medium (inferred legal acts, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://ministryofmines.co.ke/",
    "https://policyvault.africa/", # Provided context on Executive Order
    "https://devolution.go.ke/" # Provided context on Executive Order
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Nineteenth process enriched and combined_data.json updated.")
