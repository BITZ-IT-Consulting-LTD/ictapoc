
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifty-second process (index 51)
process = data['processes'][51]

# Populate fields
process['executive_summary'] = "The Kenya Forest Service (KFS) is a state corporation established under the Forests Act of 2005 and formalized by the Forest Conservation and Management Act of 2016. Its mandate is to provide for the development and sustainable management, including conservation and rational utilization, of all forest resources for the socio-economic development of Kenya and for environmental benefits such as water catchment protection and carbon sequestration."
process['process_overview']['process_objective'] = "To conserve, protect, and manage all public forests; to prepare and implement management plans for forest resources; to regulate the use of forest resources through licenses and permits; to promote forestry education and training; to manage critical water catchment areas; to rehabilitate degraded forest areas; to increase national forest cover; and to protect and secure forest assets, thereby ensuring sustainable forest management for national development and environmental well-being."
process['process_overview']['policy_legal_context'].append("Established under the Forests Act of 2005 and subsequently formalized by the Forest Conservation and Management Act of 2016. These Acts provide the comprehensive legal framework for the conservation, management, and sustainable utilization of forest resources in Kenya.")
process['stakeholders'].append({"stakeholder": "Local Communities (Community Forest Associations - CFAs)", "role": "Partners in participatory forest management and beneficiaries of forest resources", "responsibilities": "(INFERRED) Engaging in co-management activities, utilizing forest resources sustainably, protecting forests."})
process['stakeholders'].append({"stakeholder": "Forest-Dependent Industries", "role": "Commercial entities utilizing forest products (e.g., timber, non-wood products)", "responsibilities": "(INFERRED) Operating within legal frameworks, promoting sustainable sourcing, value addition."})
process['stakeholders'].append({"stakeholder": "Sawmillers / Timber Dealers", "role": "Businesses involved in processing and trading timber", "responsibilities": "(INFERRED) Adhering to licensing requirements, ensuring legal timber trade."})
process['stakeholders'].append({"stakeholder": "Environmental Conservation Organizations", "role": "Partners in forest protection, biodiversity conservation, and environmental advocacy", "responsibilities": "(INFERRED) Collaborating on conservation projects, raising awareness, advocacy."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in forest management, especially community and private forests", "responsibilities": "(INFERRED) Supporting local forest initiatives, implementing environmental policies."})
process['stakeholders'].append({"stakeholder": "Researchers / Academia", "role": "Contributors to forestry science, research, and innovation", "responsibilities": "(INFERRED) Conducting scientific studies, advising on best practices."})
process['stakeholders'].append({"stakeholder": "Policy Makers (relevant ministries)", "role": "Recipients of technical advice for forest policy formulation and implementation", "responsibilities": "(INFERRED) Formulating forest policies, providing oversight to KFS."})
process['stakeholders'].append({"stakeholder": "Farmers (agroforestry)", "role": "Participants in tree planting and agroforestry initiatives", "responsibilities": "(INFERRED) Planting trees on farms, contributing to increased forest cover."})
process['stakeholders'].append({"stakeholder": "General Public", "role": "Beneficiaries of environmental services from forests and responsible forest users", "responsibilities": "(INFERRED) Participating in tree planting, respecting forest regulations."})

process['as_is_narrative'] = "(INFERRED) KFS operates by developing and implementing comprehensive management plans for public forests, including conservation, protection, and utilization strategies. It regulates access to and use of forest products through a system of licenses and permits, and actively engages in reforestation, afforestation, and rehabilitation of degraded forest areas. The Service provides technical support and guidance to Community Forest Associations (CFAs) and private forest owners, enforces forest laws to combat illegal logging and encroachment, and maintains a Geographic Information System (GIS) database of all forests in Kenya. KFS also collaborates with research institutions and promotes forestry education and training to enhance sustainable forest management practices and maximize the socio-economic benefits derived from forest resources."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kenyaforestservice.org/",
    "https://ecitizen.go.ke/", # Provided context
    "https://afro.co.ke/", # Provided context
    "https://chm-cbd.net/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifty-second process enriched and combined_data.json updated.")
