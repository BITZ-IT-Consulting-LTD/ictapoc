
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fourteenth process (index 13)
process = data['processes'][13]

# Populate fields
process['executive_summary'] = "The Ministry of Agriculture and Livestock Development Kenya is mandated to promote sustainable development and management of crops and livestock, ensuring the nation's food and nutrition security. It aims to transform the agricultural sector into a competitive, commercially oriented, and economically responsive contributor to national development."
process['process_overview']['process_objective'] = "To create an enabling environment for sustainable agricultural and livestock development, enhance food and nutrition security, improve rural livelihoods, and drive economic growth through the formulation and implementation of effective agricultural policies, research, extension services, and regulation."
process['process_overview']['policy_legal_context'].append("Mandate derived from its role in formulating, implementing, and monitoring agricultural legislations, regulations, and policies. Operates under various Acts governing agriculture, livestock development, food safety, and fisheries in Kenya. (INFERRED: Specific Acts and regulations are numerous and complex, forming the legal framework.)")
process['stakeholders'].append({"stakeholder": "Farmers", "role": "Primary producers of crops and livestock; direct beneficiaries of Ministry programs", "responsibilities": "(INFERRED) Adopting sustainable practices, participating in extension programs, supplying agricultural produce."})
process['stakeholders'].append({"stakeholder": "Pastoralists", "role": "Producers of livestock products; direct beneficiaries of Ministry programs", "responsibilities": "(INFERRED) Adopting improved livestock management, participating in disease control initiatives."})
process['stakeholders'].append({"stakeholder": "Fishers", "role": "Producers of fish and marine products; direct beneficiaries of Ministry programs", "responsibilities": "(INFERRED) Adhering to sustainable fishing practices, participating in conservation efforts."})
process['stakeholders'].append({"stakeholder": "Agricultural Research Institutions", "role": "Providers of scientific knowledge and innovation for the sector", "responsibilities": "(INFERRED) Conducting research, developing improved varieties/breeds, technology transfer."})
process['stakeholders'].append({"stakeholder": "Agricultural State Corporations", "role": "Entities implementing specific mandates within the agricultural sector", "responsibilities": "(INFERRED) Executing government programs, providing specialized services (e.g., input supply, marketing)."})
process['stakeholders'].append({"stakeholder": "Consumers", "role": "Recipients of food and agricultural products", "responsibilities": "(INFERRED) Supporting local produce, making informed food choices."})
process['stakeholders'].append({"stakeholder": "International Agricultural Organizations", "role": "Partners in funding, technical assistance, and policy development", "responsibilities": "(INFERRED) Providing support for food security initiatives, sharing best practices."})

process['as_is_narrative'] = "(INFERRED) The Ministry operates by developing and enforcing agricultural and livestock policies and regulations, providing extension services and technical advice to farmers, supporting agricultural research and technology adoption, coordinating agricultural programs, ensuring quality control of agricultural inputs and produce, managing pests and diseases, and promoting the development of various sub-sectors like dairy and bee-keeping, and addressing agriculture-related disaster management."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from official website) / medium (inferred legal acts, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://kilimo.go.ke/",
    "https://adaptationataltitude.org/", # Though not primary, provided useful context in search
    "https://devex.com/", # Though not primary, provided useful context in search
    "https://beyondforest.org/" # Though not primary, provided useful context in search
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fourteenth process enriched and combined_data.json updated.")
