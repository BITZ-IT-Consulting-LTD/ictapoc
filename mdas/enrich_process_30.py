
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirty-first process (index 30)
process = data['processes'][30]

# Populate fields
process['executive_summary'] = "The Kenya Bureau of Standards (KEBS) is a government agency established to provide Standardization, Metrology, and Conformity Assessment Services. Its core mandate is to safeguard consumers and facilitate trade for a sustainable future by promoting quality and safety in Kenyan industry and commerce."
process['process_overview']['process_objective'] = "To develop and promote national standards for industrial and commercial products, provide examination and testing facilities, certify industrial products and systems, maintain national measurement standards (metrology), and enforce compliance to enhance product quality, protect consumers, and facilitate fair trade practices in Kenya."
process['process_overview']['policy_legal_context'].append("Established by The Standards Act, Chapter 496 of the Laws of Kenya, which provides the foundational legal framework for its operations. Governs and maintains standards and practices of metrology in Kenya.")
process['stakeholders'].append({"stakeholder": "Kenyan Consumers", "role": "Beneficiaries of safe, quality products and services", "responsibilities": "(INFERRED) Demanding quality products, reporting non-compliant goods."})
process['stakeholders'].append({"stakeholder": "Industrial and Commercial Enterprises", "role": "Manufacturers, service providers, and businesses operating in Kenya; subjects of KEBS's standardization and conformity assessment", "responsibilities": "(INFERRED) Adhering to national standards, seeking product certification, improving quality processes."})
process['stakeholders'].append({"stakeholder": "Exporters and Importers", "role": "Entities involved in international trade of goods to and from Kenya", "responsibilities": "(INFERRED) Ensuring imported/exported goods meet KEBS standards, complying with trade regulations."})
process['stakeholders'].append({"stakeholder": "Government Agencies", "role": "Recipients of technical advice; partners in enforcement and policy implementation", "responsibilities": "(INFERRED) Collaborating on quality infrastructure, enforcing standards in their respective sectors."})
process['stakeholders'].append({"stakeholder": "International Standardization Organizations", "role": "Collaborators in harmonizing national and international standards", "responsibilities": "(INFERRED) Participating in international forums, adopting global best practices."})

process['as_is_narrative'] = "(INFERRED) KEBS operates by developing and reviewing national standards and codes of practice, providing comprehensive testing facilities for various commodities, offering product and system certification services, conducting quality inspection of imports at points of entry, maintaining and calibrating national measurement standards through metrology, performing market surveillance to ensure product compliance, providing technical advice and training to industry, and representing Kenya in international standardization bodies."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://kebs.go.ke/",
    "https://en.wikipedia.org/wiki/Kenya_Bureau_of_Standards", # Provided context
    "https://kebs.org/", # Provided context
    "https://afro.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirty-first process enriched and combined_data.json updated.")
