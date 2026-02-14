
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirty-second process (index 31)
process = data['processes'][31]

# Populate fields
process['executive_summary'] = "The Kenya National Bureau of Statistics (KNBS) is a State Corporation established by the Statistics Act, 2006. It serves as the principal agency of the Government for collecting, analyzing, and disseminating statistical data in Kenya, and is the custodian of official statistical information, coordinating the national statistical system."
process['process_overview']['process_objective'] = "To provide, manage, and promote quality statistics on Kenya's society and economy through the utilization of best practices for data-driven decision-making, ensuring that statistical information is collected, compiled, analyzed, published, and disseminated effectively and reliably."
process['process_overview']['policy_legal_context'].append("Established by the Statistics Act, 2006, which provides the legal framework for its mandate as the principal agency for statistical information in Kenya and its role in coordinating the national statistical system.")
process['stakeholders'].append({"stakeholder": "Government (National and County)", "role": "Primary user of official statistics for policy formulation and planning", "responsibilities": "(INFERRED) Utilizing statistical data, providing input on data needs."})
process['stakeholders'].append({"stakeholder": "Researchers and Academics", "role": "Users of statistical data for studies and analysis", "responsibilities": "(INFERRED) Conducting research, contributing to knowledge base."})
process['stakeholders'].append({"stakeholder": "Businesses and Industries", "role": "Users of statistical data for market analysis and strategic planning", "responsibilities": "(INFERRED) Utilizing data for business decisions, providing relevant data to KNBS."})
process['stakeholders'].append({"stakeholder": "International Organizations", "role": "Users of statistical data for global comparisons and development programs", "responsibilities": "(INFERRED) Collaborating on statistical methodologies, supporting data initiatives."})
process['stakeholders'].append({"stakeholder": "Kenyan Public", "role": "Beneficiaries of transparent and reliable statistical information", "responsibilities": "(INFERRED) Accessing public data, participating in surveys/censuses."})

process['as_is_narrative'] = "(INFERRED) KNBS operates by conducting various surveys and censuses (e.g., population census, economic surveys) to collect raw data. This data is then compiled, rigorously analyzed, and presented in various statistical reports and publications (e.g., economic indicators, GDP reports). It also plays a coordinating role within the national statistical system, ensuring data quality and harmonization across different government entities for evidence-based decision-making."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://knbs.or.ke/"
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirty-second process enriched and combined_data.json updated.")
