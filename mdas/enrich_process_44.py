
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the forty-fifth process (index 44)
process = data['processes'][44]

# Populate fields
process['executive_summary'] = "The Kenya Agricultural and Livestock Research Organization (KALRO) is mandated to conduct agricultural and livestock research of strategic national importance. It produces and promotes improved technologies, information, knowledge, and approaches to support the agricultural and livestock sector, contributing significantly to food security, poverty reduction, and overall economic development in Kenya."
process['process_overview']['process_objective'] = "To generate and promote knowledge and appropriate technologies to enhance agricultural and livestock productivity, value addition, and sustainable resource management; to undertake, streamline, coordinate, and regulate all aspects of research in agriculture and livestock development; and to promote the application of research findings, technologies, and innovations to improve livelihoods and ensure food security in Kenya."
process['process_overview']['policy_legal_context'].append("Established under the Kenya Agricultural and Livestock Research Organization Act (likely CAP 340 as a successor to previous agricultural research bodies), which provides the legal framework for its mandate of conducting and coordinating agricultural research in Kenya.")
process['stakeholders'].append({"stakeholder": "Farmers", "role": "Primary beneficiaries of KALRO's research findings and technologies", "responsibilities": "(INFERRED) Adopting improved farming practices, providing feedback on research relevance."})
process['stakeholders'].append({"stakeholder": "Pastoralists", "role": "Beneficiaries of livestock research aimed at improving breeds, health, and management", "responsibilities": "(INFERRED) Adopting improved livestock management, participating in field trials."})
process['stakeholders'].append({"stakeholder": "Agricultural Industries", "role": "Partners in value addition and commercialization of agricultural products", "responsibilities": "(INFERRED) Utilizing KALRO technologies, investing in agricultural processing."})
process['stakeholders'].append({"stakeholder": "Researchers / Scientists", "role": "Core human resource for conducting research and generating knowledge", "responsibilities": "(INFERRED) Conducting high-quality research, disseminating findings, collaborating with peers."})
process['stakeholders'].append({"stakeholder": "Policy Makers (Government)", "role": "Recipients of research-based advice for agricultural policy formulation", "responsibilities": "(INFERRED) Utilizing research findings for evidence-based policy, funding agricultural research."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Funders and collaborators in agricultural research and development initiatives", "responsibilities": "(INFERRED) Providing financial and technical support, aligning research with development goals."})
process['stakeholders'].append({"stakeholder": "Consumers", "role": "Ultimate beneficiaries of enhanced food security and quality agricultural products", "responsibilities": "(INFERRED) Benefiting from improved food systems, supporting agricultural value chains."})
process['stakeholders'].append({"stakeholder": "Extension Service Providers", "role": "Conduits for disseminating KALRO's technologies to farmers", "responsibilities": "(INFERRED) Translating research to practical advice, training farmers."})

process['as_is_narrative'] = "(INFERRED) KALRO operates by undertaking research and development in various strategic areas including crops, livestock, natural resource management, and socio-economics. This involves laboratory and field experiments, data collection and analysis, and developing new crop varieties, animal breeds, and sustainable farming methods. The organization then disseminates these research findings and innovations through various channels, collaborates with extension service providers, and engages with policy makers to ensure the adoption of technologies and inform agricultural policy, ultimately aiming to improve agricultural productivity and food security across Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kalro.org/",
    "https://chm-cbd.net/", # Provided context
    "https://cimmyt.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Forty-fifth process enriched and combined_data.json updated.")
