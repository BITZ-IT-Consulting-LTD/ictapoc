
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the twenty-fifth process (index 24)
process = data['processes'][24]

# Populate fields
process['executive_summary'] = "The State Department for Environment in Kenya operates under the Ministry of Environment, Climate Change and Forestry. Its primary mandate is to conserve, protect, and sustainably manage the environment and natural resources to support biodiversity and socio-economic transformation. It also facilitates good governance in environmental protection, restoration, and management for equitable and sustainable development."
process['process_overview']['process_objective'] = "To conserve, protect, and sustainably manage the environment and natural resources; undertake climate change actions (mitigation and adaptation); implement pollution control measures; and promote forestry development to ensure a clean, healthy, and safe environment for all Kenyans, contributing to biodiversity and socio-economic transformation."
process['process_overview']['policy_legal_context'].append("Operates under the Ministry of Environment, Climate Change and Forestry, established by Executive Order No. 1 of 2023. Its mandate is guided by national environmental legislation, including the Environmental Management and Co-ordination Act (EMCA), climate change policies, and forestry acts. (INFERRED: This forms the comprehensive legal framework for environmental governance.)")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Beneficiaries of a clean and healthy environment; participants in conservation efforts", "responsibilities": "(INFERRED) Engaging in sustainable practices, reporting environmental degradation."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Directly impacted by environmental policies and conservation efforts", "responsibilities": "(INFERRED) Participating in community-based conservation, sustainable resource use."})
process['stakeholders'].append({"stakeholder": "Industries", "role": "Subjects of environmental regulations and pollution control measures", "responsibilities": "(INFERRED) Adhering to environmental standards, implementing cleaner production technologies."})
process['stakeholders'].append({"stakeholder": "Conservation Organizations", "role": "Partners in environmental protection and biodiversity conservation", "responsibilities": "(INFERRED) Collaborating on conservation projects, advocating for environmental policies."})
process['stakeholders'].append({"stakeholder": "Forestry Sector", "role": "Stakeholders involved in forest development and management", "responsibilities": "(INFERRED) Practicing sustainable forestry, participating in re-afforestation."})
process['stakeholders'].append({"stakeholder": "National Environment Management Authority (NEMA)", "role": "Key implementing agency for environmental regulations", "responsibilities": "(INFERRED) Enforcing environmental laws, conducting environmental impact assessments."})
process['stakeholders'].append({"stakeholder": "International Environmental Bodies", "role": "Collaborators on global environmental issues and climate change", "responsibilities": "(INFERRED) Harmonizing national policies with international conventions, providing technical support."})

process['as_is_narrative'] = "(INFERRED) The State Department for Environment operates by formulating national policies for climate change, environment, and forestry, protecting and conserving natural resources like water towers and wetlands, developing forestry programs, implementing pollution control measures, providing meteorological services, and driving climate change mitigation and adaptation strategies. It also promotes research and innovation in environmental sustainability."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from official sources) / medium (inferred legal acts, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://environment.go.ke/",
    "https://chm-cbd.net/", # Provided context on Ministry and Executive Order
    "https://developmentaid.org/", # Provided context on Ministry and functions
    "https://weadapt.org/", # Provided context on Ministry and functions
    "https://nema.go.ke/" # Provided context on NEMA's role under the Ministry
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Twenty-fifth process enriched and combined_data.json updated.")
