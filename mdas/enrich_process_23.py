
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the twenty-fourth process (index 23)
process = data['processes'][23]

# Populate fields
process['executive_summary'] = "The Energy and Petroleum Regulatory Authority (EPRA) is an independent regulatory body in Kenya, responsible for the technical and economic regulation of the electricity, petroleum, and renewable energy subsectors. It aims to ensure safe, efficient, and sustainable energy operations, protect consumer rights, and promote energy efficiency and renewable energy adoption."
process['process_overview']['process_objective'] = "To establish and enforce regulations for the electricity, petroleum, and renewable energy sectors; issue licenses to operators; safeguard consumer rights; monitor compliance with energy laws; promote renewable energy development; and advance energy efficiency initiatives across Kenya to ensure a secure, sustainable, and affordable energy supply."
process['process_overview']['policy_legal_context'].append("Established under the Energy Act of 2019, which provides the legal framework for its regulatory functions. Operates under various regulations including the Energy (Energy Management) Regulations 2012 and the Energy (Appliances' Energy Performance and Labeling) Regulations 2016.")
process['stakeholders'].append({"stakeholder": "Electricity Consumers", "role": "Users of electricity services; beneficiaries of fair pricing and quality standards", "responsibilities": "(INFERRED) Conserving energy, reporting issues, paying for services."})
process['stakeholders'].append({"stakeholder": "Petroleum Consumers", "role": "Users of petroleum products; beneficiaries of regulated prices and quality", "responsibilities": "(INFERRED) Adhering to safety standards, reporting malpractices."})
process['stakeholders'].append({"stakeholder": "Energy Operators (Electricity, Petroleum, Renewable Energy)", "role": "Entities licensed and regulated by EPRA for energy production, transmission, distribution, or marketing", "responsibilities": "(INFERRED) Complying with licenses, adhering to technical/safety standards, providing quality service."})
process['stakeholders'].append({"stakeholder": "Government Agencies (e.g., Ministry of Energy and Petroleum)", "role": "Policy formulators and strategic partners in the energy sector", "responsibilities": "(INFERRED) Providing policy direction, collaborating on sector development."})
process['stakeholders'].append({"stakeholder": "Energy Sector Investors", "role": "Entities funding energy projects and infrastructure", "responsibilities": "(INFERRED) Investing in compliant and sustainable energy projects."})

process['as_is_narrative'] = "(INFERRED) EPRA's operations involve issuing and renewing licenses for energy and petroleum operators, monitoring adherence to legal and safety standards, setting tariffs and prices for energy products, conducting research and analysis on energy trends, promoting public awareness on energy conservation, investigating complaints, and collaborating with stakeholders to improve energy service delivery and advance sustainable energy solutions."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://epra.go.ke/",
    "https://en.wikipedia.org/wiki/Energy_and_Petroleum_Regulatory_Authority" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Twenty-fourth process enriched and combined_data.json updated.")
