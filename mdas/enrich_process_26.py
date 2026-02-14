
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the twenty-seventh process (index 26)
process = data['processes'][26]

# Populate fields
process['executive_summary'] = "The Ministry of Energy and Petroleum Kenya is mandated to develop and implement policies that foster an efficient and growing energy sector. It sets strategic directions, ensures energy security, and provides a long-term vision for stakeholders in Kenya's energy (including petroleum) sector. Its mission is to facilitate access to reliable and competitive energy services through sustainable management and exploitation of energy resources."
process['process_overview']['process_objective'] = "To develop and manage national energy policy, promote various power developments (thermal, hydro, geothermal), oversee rural electrification, and encourage renewable energy sources for efficient operation and growth of the energy sector, aiming to facilitate access to reliable and competitive energy services for all Kenyans."
process['process_overview']['policy_legal_context'].append("Mandate derived from the President's Executive Order No. 1 of 2018 (Revised June 2018). Operates under a broad legal framework including acts related to energy regulation (e.g., Energy Act), petroleum exploration and production (e.g., Petroleum Act), and policies promoting renewable energy and rural electrification. (INFERRED: This forms the comprehensive legal framework for the energy sector.)")
process['stakeholders'].append({"stakeholder": "Energy Sector Investors", "role": "Contributors to energy infrastructure development and production", "responsibilities": "(INFERRED) Investing in energy projects, adhering to regulatory standards."})
process['stakeholders'].append({"stakeholder": "Power Generation Companies (e.g., KenGen)", "role": "Producers of electricity", "responsibilities": "(INFERRED) Generating power, maintaining infrastructure, complying with environmental standards."})
process['stakeholders'].append({"stakeholder": "Energy Regulatory Bodies (e.g., Energy and Petroleum Regulatory Authority - EPRA)", "role": "Regulators of the energy and petroleum sectors", "responsibilities": "(INFERRED) Licensing, setting tariffs, ensuring compliance with energy laws."})
process['stakeholders'].append({"stakeholder": "Rural Communities", "role": "Beneficiaries of rural electrification programs", "responsibilities": "(INFERRED) Connecting to the grid, utilizing electricity for development."})
process['stakeholders'].append({"stakeholder": "Consumers of Energy", "role": "Users of electricity and petroleum products", "responsibilities": "(INFERRED) Paying for services, practicing energy conservation."})
process['stakeholders'].append({"stakeholder": "Petroleum Sector Players", "role": "Entities involved in exploration, production, refining, and distribution of petroleum", "responsibilities": "(INFERRED) Complying with petroleum regulations, ensuring supply chain integrity."})
process['stakeholders'].append({"stakeholder": "International Energy Organizations", "role": "Partners in energy development, policy, and funding", "responsibilities": "(INFERRED) Providing technical assistance, supporting energy projects."})

process['as_is_narrative'] = "(INFERRED) The Ministry operates by formulating and reviewing national energy policies, overseeing the development and management of various power sources (thermal, hydro, geothermal, renewable), implementing rural electrification programs, regulating energy security and conservation, and engaging with stakeholders to facilitate the growth and efficient operation of both the energy and petroleum sectors in line with national development goals like Vision 2030."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions from official sources) / medium (inferred legal acts, responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://energy.go.ke/",
    "https://africa-eu-energy-partnership.org/", # Provided useful context in search
    "https://kengen.co.ke/" # Provided useful context in search
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Twenty-seventh process enriched and combined_data.json updated.")
