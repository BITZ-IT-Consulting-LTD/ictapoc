
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixty-fourth process (index 63)
process = data['processes'][63]

# Populate fields
process['executive_summary'] = "The Kenya Rural Roads Authority (KeRRA) is a State corporation established in 2008 under the Kenya Roads Act, 2007. Its primary mandate is to manage, develop, rehabilitate, and maintain the rural road network across Kenya. KeRRA plays a crucial role in enhancing connectivity for rural communities, facilitating the transportation of agricultural produce to markets, and supporting overall rural economic development, thereby contributing to poverty reduction and improved livelihoods."
process['process_overview']['process_objective'] = "To construct, upgrade, rehabilitate, and maintain roads within the rural road network; to control and manage road reserves and access to roadside developments; to implement road policies specifically tailored for rural roads; to ensure compliance with axle load control regulations on rural roads; to collect, collate, and analyze data pertinent to rural road usage for effective planning; to monitor and evaluate the utilization and impact of rural roads; to prepare road work programs for all rural roads; and to coordinate with other road authorities and government agencies on integrated road network development."
process['process_overview']['policy_legal_context'].append("Established in 2008 under the Kenya Roads Act, 2007, which provides the legal framework for its mandate and functions. KeRRA operates under the Ministry of Roads and Transport and aligns its activities with national development strategies focused on rural infrastructure and socio-economic upliftment.")
process['stakeholders'].append({"stakeholder": "Rural Communities", "role": "Primary beneficiaries of improved rural road networks; often involved in road projects", "responsibilities": "(INFERRED) Advocating for road improvements, cooperating with construction activities, respecting road infrastructure."})
process['stakeholders'].append({"stakeholder": "Farmers (for market access)", "role": "Rely on rural roads for transporting agricultural produce to markets", "responsibilities": "(INFERRED) Contributing to food security, utilizing improved infrastructure for trade."})
process['stakeholders'].append({"stakeholder": "Transporters / Matatu Operators", "role": "Provide public and commercial transport services on rural roads", "responsibilities": "(INFERRED) Complying with traffic laws, ensuring safe operations, contributing to rural connectivity."})
process['stakeholders'].append({"stakeholder": "Local Contractors", "role": "Engaged by KeRRA for construction, rehabilitation, and maintenance of rural roads", "responsibilities": "(INFERRED) Delivering quality road works, adhering to contractual terms, employing local labor."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in local infrastructure development and planning; co-managers of some road classes", "responsibilities": "(INFERRED) Collaborating on road development plans, providing local support for projects."})
process['stakeholders'].append({"stakeholder": "National Government (Ministry of Roads and Transport)", "role": "Parent Ministry providing policy direction, funding, and oversight", "responsibilities": "(INFERRED) Formulating national roads policy, allocating resources to KeRRA."})
process['stakeholders'].append({"stakeholder": "Kenya National Highways Authority (KeNHA)", "role": "Manages national trunk roads; coordinates on interconnecting networks", "responsibilities": "(INFERRED) Collaborating on integrated road network planning, ensuring smooth transitions between road classes."})
process['stakeholders'].append({"stakeholder": "Kenya Urban Roads Authority (KURA)", "role": "Manages urban road networks; coordinates on interconnecting networks", "responsibilities": "(INFERRED) Collaborating on integrated road network planning, ensuring smooth transitions between road classes."})
process['stakeholders'].append({"stakeholder": "Road Users", "role": "General public using rural roads for various purposes", "responsibilities": "(INFERRED) Adhering to road safety rules, reporting road conditions."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical support for rural road projects", "responsibilities": "(INFERRED) Funding projects, sharing technical expertise for sustainable road development."})

process['as_is_narrative'] = "(INFERRED) KeRRA's operations involve a systematic approach to developing and maintaining the rural road network. This typically begins with planning and prioritizing road projects based on economic impact, connectivity needs, and community requests. The Authority then procures services from local contractors for the construction, upgrading, and rehabilitation of roads within its extensive jurisdiction. KeRRA engineers and technical staff supervise these road works, ensuring compliance with design specifications and quality standards. Routine maintenance activities, such as pothole patching, bush clearing, and drain cleaning, are continuously undertaken to keep the rural roads motorable. KeRRA also enforces axle load limits to prevent premature road damage and collects comprehensive data on road usage, traffic volumes, and road conditions to inform its planning and resource allocation. Furthermore, it actively collaborates with county governments, community leaders, and other road agencies (like KeNHA and KURA) to ensure an integrated and sustainable road network that effectively supports agricultural value chains, provides access to essential services, and stimulates economic growth in rural areas."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kerra.go.ke/",
    "https://saraka.info/", # Provided context
    "https://tenders.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixty-fourth process enriched and combined_data.json updated.")
