import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirtieth process (index 28)
process = data['processes'][28]

# Populate fields
process['executive_summary'] = "The Energy and Petroleum Regulatory Authority (EPRA) is a statutory body in Kenya, established under the Energy Act of 2019. It is responsible for the economic and technical regulation of Kenya's electricity, renewable energy, petroleum, and coal subsectors, ensuring sustainable energy supply, fair pricing, and consumer protection."
process['process_overview']['process_objective'] = "To establish and enforce regulations for the electricity, petroleum, and renewable energy sectors; issue licenses to operators; set tariffs; safeguard consumer rights; monitor compliance with energy laws and standards; promote renewable energy development and utilization; and advance energy efficiency initiatives across Kenya for a secure, sustainable, and affordable energy supply."
process['process_overview']['policy_legal_context'].append("Established under the Energy Act of 2019, which provides the primary legal framework for its regulatory functions. Also responsible for implementing the Petroleum Act (2019). Operates under various regulations including the Energy (Energy Management) Regulations 2012 and the Energy (Appliances' Energy Performance and Labeling) Regulations 2016.")
process['stakeholders'].append({"stakeholder": "Electricity Consumers", "role": "Users of electricity services; beneficiaries of regulated prices and quality standards", "responsibilities": "(INFERRED) Conserving energy, reporting issues, adhering to safety guidelines."})
process['stakeholders'].append({"stakeholder": "Petroleum Consumers", "role": "Users of petroleum products; beneficiaries of regulated prices and quality", "responsibilities": "(INFERRED) Adhering to safety standards, reporting malpractices, consuming responsibly."})
process['stakeholders'].append({"stakeholder": "Energy Operators (Generation, Transmission, Distribution, Marketing)", "role": "Entities licensed and regulated by EPRA for energy production, supply, and related services", "responsibilities": "(INFERRED) Complying with licenses, adhering to technical/safety standards, providing quality service."})
process['stakeholders'].append({"stakeholder": "Petroleum Operators (Importation, Refining, Transportation, Storage, Sale)", "role": "Entities licensed and regulated by EPRA for petroleum sector activities", "responsibilities": "(INFERRED) Complying with regulations, ensuring supply chain integrity, adhering to safety standards."})
process['stakeholders'].append({"stakeholder": "Government Agencies (e.g., Ministry of Energy and Petroleum)", "role": "Policy formulators and strategic partners in the energy sector", "responsibilities": "(INFERRED) Providing policy direction, collaborating on sector development, ensuring national energy goals are met."})
process['stakeholders'].append({"stakeholder": "Energy Sector Investors", "role": "Entities funding energy projects and infrastructure development", "responsibilities": "(INFERRED) Investing in compliant and sustainable energy projects, contributing to sector growth."})
process['stakeholders'].append({"stakeholder": "Renewable Energy Developers", "role": "Entities involved in developing and utilizing renewable energy sources", "responsibilities": "(INFERRED) Innovating, deploying sustainable energy solutions, complying with regulatory frameworks."})

process['as_is_narrative'] = "(INFERRED) EPRA's operations involve issuing and revoking licenses for electricity, renewable energy, and petroleum operators, setting and reviewing tariffs for electricity and petroleum products, monitoring compliance with energy laws and standards, investigating consumer complaints, conducting research and analysis on energy trends, promoting public awareness on energy conservation and renewable energy, and collaborating with stakeholders to improve service delivery and advance sustainable energy solutions across Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://epra.go.ke/",
    "https://saraka.info/", # Provided context
    "https://worldbank.org/", # Provided context
    "https://en.wikipedia.org/wiki/Energy_and_Petroleum_Regulatory_Authority" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Twenty-ninth process enriched and combined_data.json updated.")