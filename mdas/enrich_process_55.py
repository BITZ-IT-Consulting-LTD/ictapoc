
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifty-sixth process (index 55)
process = data['processes'][55]

# Populate fields
process['executive_summary'] = "The Kenya Meat Commission (KMC) is a state-owned enterprise established in 1950 under the Kenya Meat Commission Act. Its primary mandate is to provide a ready and reliable market for livestock farmers and to process and supply high-quality meat and meat products to consumers both domestically and for export. KMC aims to enhance Kenya's meat industry through efficient operations, quality assurance, and value addition, contributing significantly to national food security and economic development."
process['process_overview']['process_objective'] = "To operate modern abattoirs and meat processing facilities for local and export markets; to ensure and maintain high standards of meat quality, safety, and hygiene through rigorous inspection and grading; to purchase livestock from farmers to stabilize market prices and stimulate production; to promote and facilitate the export of processed meat products; to conduct research and development to improve meat production and processing techniques; to provide advisory services and support to livestock farmers; and to act as a buyer of last resort during livestock crises to prevent losses and ensure food security."
process['process_overview']['policy_legal_context'].append("Established under the Kenya Meat Commission Act (1950), which provides its legal framework. Its mission is aligned with contributing to national food security, improving livelihoods, and achieving financial self-sustainability within the meat sector. Operates under the relevant government ministry responsible for agriculture and livestock development.")
process['stakeholders'].append({"stakeholder": "Livestock Farmers", "role": "Primary suppliers of livestock to KMC; beneficiaries of a stable market", "responsibilities": "(INFERRED) Rearing healthy livestock, adhering to animal husbandry standards, supplying animals to KMC."})
process['stakeholders'].append({"stakeholder": "Consumers", "role": "Recipients of KMC's meat and meat products", "responsibilities": "(INFERRED) Purchasing and consuming KMC products, providing feedback on quality."})
process['stakeholders'].append({"stakeholder": "Meat Traders / Butchers", "role": "Distributors and retailers of meat products", "responsibilities": "(INFERRED) Buying from KMC, adhering to meat handling standards."})
process['stakeholders'].append({"stakeholder": "Meat Processors (other private entities)", "role": "Competitors and potential collaborators in the meat industry", "responsibilities": "(INFERRED) Complying with industry regulations, contributing to market competition."})
process['stakeholders'].append({"stakeholder": "Veterinary Services", "role": "Ensure animal health and compliance with meat safety standards", "responsibilities": "(INFERRED) Inspecting livestock and meat, controlling diseases."})
process['stakeholders'].append({"stakeholder": "Ministry of Agriculture and Livestock Development", "role": "Oversight ministry providing policy direction and strategic guidance", "responsibilities": "(INFERRED) Formulating livestock policies, ensuring sector development."})
process['stakeholders'].append({"stakeholder": "Export Markets / International Buyers", "role": "Consumers of KMC's export-grade meat products", "responsibilities": "(INFERRED) Meeting international quality standards, facilitating trade."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Partners in improving livestock production and meat processing techniques", "responsibilities": "(INFERRED) Conducting research, providing scientific advice."})
process['stakeholders'].append({"stakeholder": "Animal Welfare Organizations", "role": "Advocates for humane treatment of livestock", "responsibilities": "(INFERRED) Monitoring KMC practices, advocating for animal welfare standards."})

process['as_is_narrative'] = "(INFERRED) KMC's operations begin with the strategic procurement of livestock from various farmers across Kenya, often acting as a stabilizing force in the market and providing a guaranteed off-take. The acquired animals are then processed in KMC's modern abattoirs and processing plants, where stringent quality control measures, including veterinary inspections and grading, are applied to ensure product safety and adherence to national and international standards. The Commission engages in value addition activities, transforming raw meat into various processed products. These products are then marketed and distributed to domestic consumers and also targeted for export. KMC also invests in research and development to innovate processing techniques and product lines, provides advisory services to farmers to enhance livestock quality and productivity, and plays a critical role during national emergencies by stabilizing livestock prices and preventing losses, thereby securing the country's meat supply chain and supporting farmer livelihoods."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://kenyameat.co.ke/",
    "https://saraka.info/", # Provided context
    "https://agrarian.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifty-sixth process enriched and combined_data.json updated.")
