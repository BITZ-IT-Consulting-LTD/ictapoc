
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighty-ninth process (index 88)
process = data['processes'][88]

# Populate fields
process['executive_summary'] = "Animal health technicians in Kenya operate under the regulatory framework of the Kenya Veterinary Board (KVB), which is established by the Veterinary Surgeons' and Veterinary Para-professionals (VSVP) Act No. 29 of 2011. While there isn't a distinct 'Animal Technicians Council Kenya' as a direct MDA, their professional practice, standards, and registration are governed by KVB. These veterinary para-professionals play a crucial role in supporting veterinary surgeons, implementing national and regional animal health programs, providing essential extension services to farmers, and contributing significantly to livestock development and food security in Kenya."
process['process_overview']['process_objective'] = "To provide essential support to veterinary surgeons in clinical, diagnostic, and surgical procedures; to implement national and regional animal health programs, including mass vaccination campaigns, parasite control programs, and disease surveillance; to conduct inspections of livestock, poultry, and game, and report on disease outbreaks; to provide crucial extension services and training to farmers and community members on basic animal husbandry, disease prevention, nutrition, and hygiene; to collect, capture, and evaluate animal health data, and assist in epidemiological and research projects; and to carry out delegated duties related to veterinary public health, such as abattoir and meat inspections, ensuring the safety of animal products for human consumption."
process['process_overview']['policy_legal_context'].append("The regulation of animal technicians, categorized as veterinary para-professionals, falls under the **Kenya Veterinary Board (KVB)**, which is established by the **Veterinary Surgeons' and Veterinary Para-professionals (VSVP) Act No. 29 of 2011**. This Act provides the comprehensive legal framework that governs the training, registration, licensing, and professional practice of all veterinary professionals, including animal health technicians, in Kenya. Their work aligns with national policies on livestock development, animal health, food safety, and agricultural extension services under the Ministry of Agriculture, Livestock, Fisheries and Cooperatives.")
process['stakeholders'].append({"stakeholder": "Animal Health Technicians / Veterinary Para-professionals", "role": "Practicing professionals who deliver primary animal health services and support; regulated by KVB", "responsibilities": "(INFERRED) Providing animal health services, adhering to professional ethics, continuous professional development."})
process['stakeholders'].append({"stakeholder": "Kenya Veterinary Board (KVB)", "role": "Regulatory body responsible for the registration, licensing, and professional conduct of animal health technicians", "responsibilities": "(INFERRED) Setting standards, conducting examinations, enforcing the VSVP Act, maintaining a register of professionals."})
process['stakeholders'].append({"stakeholder": "Farmers / Livestock Keepers", "role": "Primary clients and beneficiaries of animal health services provided by technicians", "responsibilities": "(INFERRED) Seeking animal health services, implementing advice, participating in animal health programs."})
process['stakeholders'].append({"stakeholder": "Veterinary Surgeons", "role": "Supervisors and collaborators for animal health technicians in complex cases and specialized procedures", "responsibilities": "(INFERRED) Providing oversight, delegating tasks, collaborating on animal health management."})
process['stakeholders'].append({"stakeholder": "Animal Technicians and Technologists Association of Kenya (ATTAK)", "role": "Professional body representing the interests of animal technicians; works with KVB on professional development", "responsibilities": "(INFERRED) Advocating for members, promoting professional standards, organizing training."})
process['stakeholders'].append({"stakeholder": "Ministry of Agriculture, Livestock, Fisheries and Cooperatives", "role": "Provides policy direction for livestock development, animal health, and food security", "responsibilities": "(INFERRED) Formulating livestock policies, funding animal health programs, strategic guidance."})
process['stakeholders'].append({"stakeholder": "Research Institutions (e.g., Kenya Agricultural and Livestock Research Organization (KALRO), International Livestock Research Institute (ILRI))", "role": "Sources of new knowledge and technologies for animal health and livestock production; collaborate with technicians on field data collection", "responsibilities": "(INFERRED) Conducting research, developing improved animal health practices, providing technical support."})
process['stakeholders'].append({"stakeholder": "Slaughterhouses / Abattoirs", "role": "Sites where animal health technicians perform meat inspection and public health duties", "responsibilities": "(INFERRED) Complying with public health regulations, facilitating inspections."})
process['stakeholders'].append({"stakeholder": "Consumers of Animal Products", "role": "Beneficiaries of safe and healthy animal products due to technician inspections and health programs", "responsibilities": "(INFERRED) Consuming safe animal products, relying on quality assurance systems."})
process['stakeholders'].append({"stakeholder": "Training Institutions (for animal health programs)", "role": "Provide education and training for aspiring animal health technicians", "responsibilities": "(INFERRED) Developing relevant curricula, training future professionals, ensuring quality education."})

process['as_is_narrative'] = "(INFERRED) Animal health technicians in Kenya, operating under the regulatory guidance of the Kenya Veterinary Board (KVB), are frontline providers of animal health services, particularly in rural and marginalized areas. Their daily activities involve a wide range of tasks, including assisting veterinary surgeons during complex clinical examinations, surgical operations, and post-operative care. A significant portion of their work focuses on implementing extensive national animal health programs, such as coordinating and conducting mass vaccination campaigns against prevalent livestock diseases (e.g., Foot and Mouth Disease, Contagious Bovine Pleuropneumonia) and implementing parasite control strategies through dipping and deworming. They are crucial for disease surveillance, reporting suspected outbreaks, and collecting samples for laboratory diagnostics. Animal health technicians regularly conduct on-farm visits to inspect livestock and poultry, providing farmers with critical extension services and training on basic animal husbandry, nutrition, breeding, and disease prevention strategies. In line with veterinary public health, they perform delegated duties such as ante-mortem and post-mortem inspections at local slaughterhouses and abattoirs to ensure the safety and wholesomeness of meat and other animal products for human consumption. Furthermore, they play a vital role in collecting and evaluating animal health data, assisting in epidemiological investigations, and contributing to field-based research projects, all while adhering to the professional standards and ethical guidelines set forth by the VSVP Act and KVB."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from reliable sources, including KVB) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kenyavetboard.or.ke/", # Official KVB website
    "https://www.savc.org.za/", # Provided context (general description of AHT roles)
    "https://kilimo.go.ke/" # Provided context (ATTAK mentioned)
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighty-ninth process enriched and combined_data.json updated.")
