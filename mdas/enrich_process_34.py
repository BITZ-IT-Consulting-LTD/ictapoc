
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirty-fifth process (index 34)
process = data['processes'][34]

# Populate fields
process['executive_summary'] = "The Kenya Medical Supplies Authority (KEMSA) is a state corporation under the Ministry of Health, mandated to procure, warehouse, and distribute Health Products and Technologies (HPTs) for public health programs, national strategic stock reserves, and national referral hospitals. It plays a crucial role in ensuring the availability of HPTs and supporting Universal Health Coverage in Kenya."
process['process_overview']['process_objective'] = "To ensure the availability, accessibility, and affordability of quality Health Products and Technologies (HPTs) for public health programs, national strategic stock reserves, essential health packages, and health facilities across Kenya, thereby supporting the achievement of Universal Health Coverage."
process['process_overview']['policy_legal_context'].append("Established by the KEMSA Act 2013, which provides the legal framework for its mandate in managing the medical supply chain in Kenya. Operates under the Ministry of Health.")
process['stakeholders'].append({"stakeholder": "Ministry of Health", "role": "Parent Ministry providing policy direction and oversight", "responsibilities": "(INFERRED) Formulating health policies, setting healthcare priorities."})
process['stakeholders'].append({"stakeholder": "Public Health Facilities (Hospitals, Clinics)", "role": "Recipients of HPTs for patient care", "responsibilities": "(INFERRED) Managing HPT inventory, ensuring rational use, providing patient care."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in maintaining appropriate supply chain systems for drugs and medical supplies", "responsibilities": "(INFERRED) Managing county health services, collaborating on HPT distribution."})
process['stakeholders'].append({"stakeholder": "Non-Governmental Organizations (NGOs)", "role": "Partners in health service delivery and HPT distribution", "responsibilities": "(INFERRED) Providing healthcare, supporting public health programs."})
process['stakeholders'].append({"stakeholder": "Faith-Based Organizations (FBOs)", "role": "Partners in health service delivery and HPT distribution", "responsibilities": "(INFERRED) Providing healthcare, supporting public health programs."})
process['stakeholders'].append({"stakeholder": "Patients/Citizens", "role": "Ultimate beneficiaries of available and quality HPTs", "responsibilities": "(INFERRED) Accessing healthcare, adhering to prescribed treatments."})
process['stakeholders'].append({"stakeholder": "Suppliers of HPTs / Pharmaceutical Companies", "role": "Providers of Health Products and Technologies to KEMSA", "responsibilities": "(INFERRED) Ensuring quality products, complying with procurement regulations."})

process['as_is_narrative'] = "(INFERRED) KEMSA's operations involve strategically procuring Health Products and Technologies (HPTs) through competitive and commercial processes, managing extensive warehousing and storage facilities across its network, and distributing these HPTs efficiently to public health facilities, NGOs, FBOs, and national referral hospitals. It also provides technical guidance to county governments on supply chain management and implements rigorous quality assurance measures for all medical commodities handled."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://kemsa.co.ke/",
    "https://kemsa.go.ke/", # Both .co.ke and .go.ke domains appear relevant, consolidating here
    "https://en.wikipedia.org/wiki/Kenya_Medical_Supplies_Authority", # Provided context
    "https://deborahwando.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirty-fifth process enriched and combined_data.json updated.")
