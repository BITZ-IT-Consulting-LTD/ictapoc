
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifty-seventh process (index 56)
process = data['processes'][56]

# Populate fields
process['executive_summary'] = "The Kenya Medical Supplies Authority (KEMSA) is a state corporation under the Ministry of Health, established by the KEMSA Act 2013. Its primary mandate is to procure, warehouse, and distribute Health Products and Technologies (HPTs), including drugs, vaccines, and medical equipment, to public health facilities across Kenya. KEMSA plays a crucial role in supporting the implementation of Universal Health Coverage (UHC) by ensuring the availability, accessibility, and affordability of quality medical supplies nationwide."
process['process_overview']['process_objective'] = "To ensure the availability, accessibility, and affordability of quality Health Products and Technologies (HPTs) for all Kenyans; to procure medical supplies for prescribed public health programs, national strategic stock reserves, and national referral hospitals; to provide efficient and secure warehousing and distribution services for medical commodities; to enforce stringent quality assurance measures for all procured supplies; to offer technical guidance to health management boards and county governments on cost-effective procurement and rational use of medicines; and to support various national health programs (e.g., TB, HIV/AIDS, Malaria Control)."
process['process_overview']['policy_legal_context'].append("Established under the Kenya Medical Supplies Authority Act 2013, which provides the legal framework for its operations. It operates under the oversight of the Ministry of Health and is a key implementing agency for the government's Universal Health Coverage (UHC) initiatives. KEMSA's activities are guided by national health policies and international procurement standards.")
process['stakeholders'].append({"stakeholder": "Public Health Facilities (Hospitals, Health Centers, Dispensaries)", "role": "Recipients and users of medical supplies distributed by KEMSA", "responsibilities": "(INFERRED) Ordering supplies, ensuring proper storage and utilization, providing patient care."})
process['stakeholders'].append({"stakeholder": "Ministry of Health", "role": "Parent Ministry providing policy direction, oversight, and funding", "responsibilities": "(INFERRED) Formulating health policies, setting national health priorities, funding KEMSA operations."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Responsible for devolved health services; partners in HPT distribution", "responsibilities": "(INFERRED) Managing county health facilities, budgeting for medical supplies, collaborating with KEMSA."})
process['stakeholders'].append({"stakeholder": "Patients / General Public", "role": "Ultimate beneficiaries of KEMSA's services (access to quality medicines)", "responsibilities": "(INFERRED) Accessing prescribed medicines, providing feedback on availability."})
process['stakeholders'].append({"stakeholder": "Medical Suppliers / Manufacturers", "role": "Providers of Health Products and Technologies to KEMSA", "responsibilities": "(INFERRED) Supplying quality products, adhering to KEMSA's tender requirements."})
process['stakeholders'].append({"stakeholder": "National Quality Control Laboratory", "role": "Collaborator in ensuring quality standards of medical supplies", "responsibilities": "(INFERRED) Testing and certifying medical products, providing quality assurance reports."})
process['stakeholders'].append({"stakeholder": "Pharmacy and Poisons Board", "role": "Regulatory body for pharmaceutical products", "responsibilities": "(INFERRED) Registering medical products, enforcing drug quality and safety standards."})
process['stakeholders'].append({"stakeholder": "National Health Programs (e.g., TB, HIV/AIDS, Malaria Control)", "role": "Recipients of specialized HPTs for disease management", "responsibilities": "(INFERRED) Implementing disease control strategies, managing program-specific supplies."})
process['stakeholders'].append({"stakeholder": "Development Partners / Donors", "role": "Contributors to health funding and procurement support", "responsibilities": "(INFERRED) Providing financial and technical assistance for HPT procurement."})

process['as_is_narrative'] = "(INFERRED) KEMSA operates a centralized and transparent procurement system for Health Products and Technologies (HPTs), leveraging economies of scale to achieve cost-effectiveness. Once procured, these supplies are efficiently received, stored in modern, temperature-controlled warehouses, and managed through sophisticated logistics and inventory systems. KEMSA then distributes these HPTs to thousands of public health facilities across all 47 counties of Kenya, ensuring a last-mile delivery. A core aspect of its operations is rigorous quality control, involving inspection, testing, and certification of all medical products in collaboration with regulatory bodies. KEMSA also provides valuable technical advisory services to county health management teams on supply chain management, rational drug use, and procurement planning. Furthermore, it actively supports various national vertical health programs by managing their specific HPT requirements, and it maintains both a non-commercial supply system for public facilities and a competitive commercial division to enhance its reach and sustainability."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kemsa.co.ke/",
    "https://kemsa.go.ke/", # Provided context (alternative domain)
    "https://wikipedia.org/", # Provided context
    "https://majira.co.ke/", # Provided context
    "https://deborahwando.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifty-seventh process enriched and combined_data.json updated.")
