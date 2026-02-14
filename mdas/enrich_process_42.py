
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the forty-third process (index 42)
process = data['processes'][42]

# Populate fields
process['executive_summary'] = "The Energy and Petroleum Regulatory Authority (EPRA) is a statutory body in Kenya, established under the Energy Act of 2019. It is mandated to regulate the energy and petroleum sectors, encompassing electricity, renewable energy, petroleum (upstream, midstream, and downstream), and coal, with the objective of ensuring fair pricing, efficiency, quality, and sustainability within these vital sectors."
process['process_overview']['process_objective'] = "To regulate the generation, importation, exportation, transmission, distribution, supply, and use of electrical energy and petroleum products; issue licenses to operators; manage tariffs for electricity and petroleum; protect consumer rights; promote the development and use of renewable energy sources; ensure compliance with energy laws, regulations, and standards; and advise the government on energy sector matters for sustainable development."
process['process_overview']['policy_legal_context'].append("Established under the Energy Act of 2019, succeeding the Energy Regulatory Commission (ERC). Responsible for implementing the Petroleum Act (2019) and other related energy laws and regulations in Kenya.")
process['stakeholders'].append({"stakeholder": "Electricity Generators / Suppliers", "role": "Producers and distributors of electrical energy", "responsibilities": "(INFERRED) Complying with licensing conditions, ensuring reliable supply, adhering to quality standards."})
process['stakeholders'].append({"stakeholder": "Petroleum Importers / Distributors / Retailers", "role": "Entities involved in the supply chain of petroleum products", "responsibilities": "(INFERRED) Complying with regulations, ensuring product quality, adhering to pricing structures."})
process['stakeholders'].append({"stakeholder": "Renewable Energy Developers", "role": "Developers and operators of renewable energy projects", "responsibilities": "(INFERRED) Adhering to technical standards, promoting sustainable energy solutions."})
process['stakeholders'].append({"stakeholder": "Consumers (Electricity, Petroleum)", "role": "Users of energy and petroleum products", "responsibilities": "(INFERRED) Adhering to consumption guidelines, reporting grievances, engaging in energy conservation."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Energy)", "role": "Policy maker and oversight body for the energy sector", "responsibilities": "(INFERRED) Formulating energy policies, strategic guidance, resource allocation."})
process['stakeholders'].append({"stakeholder": "Investors in Energy Sector", "role": "Financial contributors to energy projects", "responsibilities": "(INFERRED) Adhering to investment regulations, contributing to sector growth."})
process['stakeholders'].append({"stakeholder": "Environmental Agencies", "role": "Partners in ensuring environmental compliance in energy projects", "responsibilities": "(INFERRED) Overseeing environmental impact assessments, enforcing environmental regulations."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Contributors to innovation and data for policy decisions", "responsibilities": "(INFERRED) Conducting research, providing expert advice on energy technologies."})

process['as_is_narrative'] = "(INFERRED) EPRA operates by issuing licenses and permits to energy and petroleum operators, regulating tariffs to ensure fair pricing, monitoring the quality of energy products and services, enforcing safety and environmental standards, promoting the adoption of renewable energy technologies, conducting research and data collection, and protecting consumer interests. It collaborates with various stakeholders and government agencies to ensure a secure, sustainable, and affordable energy supply in Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://epra.go.ke/",
    "https://saraka.info/", # Provided context
    "https://africa-energy-portal.org/", # Provided context
    "https://wikipedia.org/", # Provided context
    "https://worldbank.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Forty-third process enriched and combined_data.json updated.")
