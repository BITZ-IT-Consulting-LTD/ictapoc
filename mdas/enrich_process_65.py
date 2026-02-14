
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixty-sixth process (index 65)
process = data['processes'][65]

# Populate fields
process['executive_summary'] = "The Kenya Trade Network Agency (KenTrade) is a state corporation operating under Kenya's National Treasury, established in January 2011. Its core mandate is to establish, implement, and manage the National Electronic Single Window System (NESWS), commonly known as the Kenya TradeNet System. This system is designed to streamline cross-border trade, simplify import and export procedures, and significantly reduce associated paperwork and processing times, thereby enhancing Kenya's efficiency and competitiveness in international trade."
process['process_overview']['process_objective'] = "To establish, implement, and manage the National Electronic Single Window System (NESWS) to facilitate international trade; to integrate the electronic systems of public and private entities involved in international trade transactions; to develop, manage, and promote the efficient exchange of electronic data to facilitate trade; to conduct and coordinate research in e-commerce to simplify and standardize trade documentation; to maintain an electronic database of all imported and exported goods and services; to provide training programs to ensure adherence to international trade norms; and to offer services such as the Trade Facilitation Platform and the InfoTrade Kenya Portal for procedural guidance and stakeholder education."
process['process_overview']['policy_legal_context'].append("Established in January 2011 and its core mandate is outlined in the National Electronic Single Window System Act of 2022. KenTrade operates under the oversight of the National Treasury and is crucial for implementing national trade facilitation policies and international commitments related to trade efficiency and ease of doing business.")
process['stakeholders'].append({"stakeholder": "Importers / Exporters", "role": "Primary users of the Single Window System for trade transactions", "responsibilities": "(INFERRED) Submitting trade documents electronically, complying with trade regulations."})
process['stakeholders'].append({"stakeholder": "Customs Authorities (KRA Customs)", "role": "Key government agency integrated into the Single Window for revenue collection and trade control", "responsibilities": "(INFERRED) Processing declarations, collecting duties, enforcing customs laws electronically."})
process['stakeholders'].append({"stakeholder": "Other Government Agencies (involved in trade permits/licenses, e.g., KEBS, Port Health, etc.)", "role": "Provide various permits, licenses, and certifications required for trade through the Single Window", "responsibilities": "(INFERRED) Issuing permits electronically, ensuring compliance with relevant regulations."})
process['stakeholders'].append({"stakeholder": "Clearing and Forwarding Agents", "role": "Facilitate customs clearance and logistics on behalf of importers/exporters", "responsibilities": "(INFERRED) Submitting documents, coordinating cargo movement, ensuring compliance."})
process['stakeholders'].append({"stakeholder": "Shipping Lines / Airlines", "role": "Providers of international transport services for goods", "responsibilities": "(INFERRED) Providing cargo manifests, adhering to port/airport procedures."})
process['stakeholders'].append({"stakeholder": "Banks / Financial Institutions", "role": "Facilitate payments for duties, fees, and other trade-related transactions", "responsibilities": "(INFERRED) Processing electronic payments, providing financial services for trade."})
process['stakeholders'].append({"stakeholder": "Kenya Ports Authority (KPA)", "role": "Manages sea ports; integrated into the Single Window for cargo release", "responsibilities": "(INFERRED) Managing port operations, providing cargo data electronically."})
process['stakeholders'].append({"stakeholder": "Kenya Civil Aviation Authority (KCAA)", "role": "Regulates air transport; integrated for air cargo procedures", "responsibilities": "(INFERRED) Regulating air cargo, coordinating with KenTrade on air freight."})
process['stakeholders'].append({"stakeholder": "Local and International Traders", "role": "The broader community involved in commercial activities facilitated by KenTrade", "responsibilities": "(INFERRED) Engaging in trade, utilizing the Single Window System."})

process['as_is_narrative'] = "(INFERRED) KenTrade's operations revolve around the continuous development, maintenance, and enhancement of the Kenya TradeNet System, a sophisticated electronic single window platform. This system acts as a central hub where traders can submit all required regulatory documents (permits, licenses, declarations) electronically, and various government agencies (Customs, KEBS, Port Health, etc.) can process these documents and effect payment of duties and fees online. KenTrade actively integrates the electronic systems of over 30 public and private entities to achieve seamless information exchange and reduce duplication. It also conducts ongoing research in e-commerce and trade facilitation to identify bottlenecks and implement solutions, such as optimizing trade documentation. KenTrade manages the InfoTrade Kenya Portal, which provides comprehensive information on import/export procedures and requirements, and an e-Learning Portal for stakeholder capacity building. Through these efforts, KenTrade significantly reduces trade transaction time and costs, promotes transparency, and streamlines the movement of goods across Kenya's borders, aiming to make Kenya a global leader in trade facilitation."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kentrade.go.ke/",
    "https://grokipedia.com/", # Provided context
    "https://wikipedia.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixty-sixth process enriched and combined_data.json updated.")
