
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventy-first process (index 70)
process = data['processes'][70]

# Populate fields
process['executive_summary'] = "The National Construction Authority (NCA) is a state corporation established under Section 3 of the NCA Act No. 41 of 2011. Its primary mandate is to oversee, coordinate, regulate, and promote the development of a sustainable and vibrant construction industry in Kenya. NCA ensures quality, safety, and adherence to standards within Kenya's built environment, while also protecting consumers from substandard workmanship and fostering capacity building within the sector for both contractors and skilled labor."
process['process_overview']['process_objective'] = "To regulate the construction industry through the registration and certification of contractors, accreditation of skilled construction workers and site supervisors, and mandatory registration of construction projects; to enhance industry capacity through continuous professional development and training for all practitioners; to undertake or commission research related to the building sector and maintain a comprehensive construction industry information system; to encourage the standardization and improvement of construction techniques, technologies, and materials; to assist in the exportation of construction services; and to enforce building codes and industry regulations to ensure quality, safety, and sustainability in the built environment."
process['process_overview']['policy_legal_context'].append("Established under Section 3 of the NCA Act No. 41 of 2011, which provides the legal framework for its regulatory and promotional functions. NCA operates under the Ministry responsible for Construction (currently Ministry of Transport, Infrastructure, Housing and Urban Development, or its equivalent) and is instrumental in implementing national policies aimed at streamlining the construction sector, improving quality and safety standards, and fostering local content development in construction.")
process['stakeholders'].append({"stakeholder": "Contractors (National and International)", "role": "Primary subjects of NCA's registration, regulation, and capacity building efforts", "responsibilities": "(INFERRED) Registering with NCA, adhering to building codes, ensuring quality workmanship, participating in training."})
process['stakeholders'].append({"stakeholder": "Construction Workers / Artisans", "role": "Beneficiaries of accreditation, training, and safety regulations", "responsibilities": "(INFERRED) Seeking accreditation, participating in training, adhering to site safety protocols."})
process['stakeholders'].append({"stakeholder": "Developers / Clients", "role": "Commission construction projects; rely on NCA for quality assurance and dispute resolution", "responsibilities": "(INFERRED) Registering projects, ensuring engagement of registered contractors, complying with regulations."})
process['stakeholders'].append({"stakeholder": "Consultants (Architects, Engineers, Quantity Surveyors)", "role": "Design and supervise construction projects; interact with NCA on project compliance", "responsibilities": "(INFERRED) Adhering to professional standards, ensuring project designs comply with codes."})
process['stakeholders'].append({"stakeholder": "Construction Material Suppliers", "role": "Provide materials used in construction; affected by NCA's quality standards", "responsibilities": "(INFERRED) Supplying quality materials, ensuring materials meet required standards."})
process['stakeholders'].append({"stakeholder": "County Governments (for building approvals/inspections)", "role": "Partners in enforcing building regulations and development control at the local level", "responsibilities": "(INFERRED) Issuing building permits, conducting site inspections, collaborating with NCA."})
process['stakeholders'].append({"stakeholder": "National Government (Ministry responsible for Construction)", "role": "Parent Ministry providing policy direction, funding, and oversight", "responsibilities": "(INFERRED) Formulating construction policies, allocating resources, strategic guidance."})
process['stakeholders'].append({"stakeholder": "Professional Bodies (e.g., Architectural Association of Kenya (AAK), Engineers Board of Kenya (EBK), Institute of Quantity Surveyors of Kenya (IQSK))", "role": "Regulate specific construction professions; collaborate with NCA on industry standards", "responsibilities": "(INFERRED) Setting professional ethics, licensing professionals, collaborating on industry best practices."})
process['stakeholders'].append({"stakeholder": "Training Institutions (TVETs, Universities)", "role": "Provide education and training relevant to the construction industry workforce", "responsibilities": "(INFERRED) Developing relevant curricula, equipping future construction professionals."})
process['stakeholders'].append({"stakeholder": "Financial Institutions", "role": "Provide funding for construction projects and contractors", "responsibilities": "(INFERRED) Offering construction financing, assessing project viability."})
process['stakeholders'].append({"stakeholder": "Insurers", "role": "Provide insurance for construction projects, workers, and clients", "responsibilities": "(INFERRED) Offering relevant insurance products, assessing construction risks."})

process['as_is_narrative'] = "(INFERRED) The NCA's operations involve systematically registering and licensing contractors across various categories based on their technical and financial capacities, ensuring that only qualified entities undertake construction projects. It also plays a crucial role in accrediting skilled construction workers and site supervisors, standardizing their qualifications and promoting professionalism. All construction projects are mandatorily registered with the NCA, which then issues site compliance certificates and conducts regular, rigorous site inspections to ensure strict adherence to approved building plans, national building codes, environmental regulations, and occupational safety and health standards. The Authority implements various training and continuous professional development programs to uplift the skills and knowledge of industry practitioners. Furthermore, NCA actively undertakes and commissions research into construction materials, techniques, and sustainable building practices, maintaining a comprehensive industry information system to inform stakeholders and policy. It also collaborates closely with county governments, professional bodies, and other regulatory agencies to ensure a harmonized approach to construction regulation, dispute resolution, and the promotion of ethical practices, thereby safeguarding public interest and fostering a robust construction sector."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.nca.go.ke/",
    "https://nzangimuimi.com/", # Provided context
    "https://constructionkenya.com/", # Provided context
    "https://nestict.com/", # Provided context
    "https://timely.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventy-first process enriched and combined_data.json updated.")
