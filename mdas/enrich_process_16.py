
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventeenth process (index 16)
process = data['processes'][16]

# Populate fields
process['executive_summary'] = "The State Department for Transport in Kenya operates under the Ministry of Roads and Transport, with a mandate encompassing transport policy management, rail and civil aviation infrastructure development, national transport safety, and oversight of key transport institutions. It aims to develop an integrated, efficient, effective, and sustainable transport system."
process['process_overview']['process_objective'] = "To formulate and manage transport policy, oversee rail transport and civil aviation, manage national transport safety, coordinate major transport corridor projects (Northern and LAPSSET), and regulate vehicle registration, inspection, and axle load control to ensure a safe, efficient, and sustainable transport system in Kenya."
process['process_overview']['policy_legal_context'].append("Mandate outlined in Executive Order No. 1 of 2023. Operates under a broad legal framework that includes acts related to civil aviation (e.g., Civil Aviation Act), rail transport (e.g., Kenya Railways Act), road safety (e.g., Traffic Act, NTSA Act), and maritime affairs, given its oversight over various transport authorities. (INFERRED: Specific acts are diverse and govern different transport sectors.)")
process['stakeholders'].append({"stakeholder": "Kenya Ports Authority (KPA)", "role": "State corporation responsible for port operations", "responsibilities": "(INFERRED) Managing and developing seaports, facilitating maritime trade."})
process['stakeholders'].append({"stakeholder": "National Transport and Safety Authority (NTSA)", "role": "Government agency responsible for road safety and transport regulation", "responsibilities": "(INFERRED) Vehicle registration, driver licensing, road safety campaigns."})
process['stakeholders'].append({"stakeholder": "Kenya Railways Corporation", "role": "State corporation managing railway transport services", "responsibilities": "(INFERRED) Operating and maintaining railway infrastructure, providing freight and passenger services."})
process['stakeholders'].append({"stakeholder": "Kenya Airports Authority (KAA)", "role": "State corporation responsible for airport management and development", "responsibilities": "(INFERRED) Managing airports, ensuring safety and efficiency of air travel."})
process['stakeholders'].append({"stakeholder": "Kenya Civil Aviation Authority (KCAA)", "role": "Regulatory body for civil aviation", "responsibilities": "(INFERRED) Licensing air operators, regulating air traffic services, investigating accidents."})
process['stakeholders'].append({"stakeholder": "Public Transport Users", "role": "Consumers of transport services", "responsibilities": "(INFERRED) Adhering to transport regulations, seeking safe and efficient transport options."})
process['stakeholders'].append({"stakeholder": "Transport Operators (Road, Rail, Air, Maritime)", "role": "Providers of transport services", "responsibilities": "(INFERRED) Complying with transport laws, ensuring safe operations, maintaining vehicles/vessels."})
process['stakeholders'].append({"stakeholder": "International Transport Bodies", "role": "Collaborators on international transport standards and agreements", "responsibilities": "(INFERRED) Harmonizing national transport policies with international best practices."})

process['as_is_narrative'] = "(INFERRED) The State Department operates by formulating and reviewing transport policies, managing and overseeing the development of rail and civil aviation infrastructure, implementing national transport safety programs including road safety management and axle load control, registering and inspecting motor vehicles, and coordinating major transport corridor projects like Northern and LAPSSET to enhance regional connectivity and trade."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from official sources) / medium (inferred legal acts, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://transport.go.ke/"
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventeenth process enriched and combined_data.json updated.")
