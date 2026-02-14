
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninety-ninth process (index 98)
process = data['processes'][98]

# Populate fields
process['executive_summary'] = "The Building Surveyors Registration Board is a regulatory body established under the Building Surveyors Act No. 19 of 2018 in Kenya. Its primary mandate is to promote the practice of building surveying in compliance with universally accepted norms and values, and to regulate the registration, licensing, and professional conduct of building surveyors. The Board ensures high standards for the built environment, safeguards public interest in the quality and safety of buildings, and contributes to the integrity of the construction sector in Kenya."
process['process_overview']['process_objective'] = "To establish and govern the Building Surveyors Registration Board, defining its composition and powers; to register and license building surveyors, maintaining an official register of all practicing professionals; to issue certificates of registration and annual practicing licenses to qualified building surveyors; to regulate the practice of building surveyors, including setting conditions and qualifications for registration; to handle the suspension, removal, and restoration of names on the register based on professional conduct; to establish procedures for inquiries and appeals related to the practice of building surveying; and to administer the Board's funds, manage its financial year, annual estimates, accounts, audit, and annual reports as stipulated by the Act."
process['process_overview']['policy_legal_context'].append("Established under the Building Surveyors Act No. 19 of 2018, which provides the comprehensive legal framework for the Board's regulatory functions over the building surveying profession in Kenya. The Board operates under the Ministry of Lands, Public Works, Housing and Urban Development (or the relevant government ministry responsible for built environment professionals) and is crucial for ensuring professional competence, ethical conduct, and public safety in building construction and maintenance, aligning with national goals for sustainable infrastructure development.")
process['stakeholders'].append({"stakeholder": "Building Surveyors (aspiring and registered)", "role": "Professionals whose training, registration, and practice are regulated by the Board", "responsibilities": "(INFERRED) Complying with the Act, adhering to professional standards, seeking registration/licensing, undertaking CPD."})
process['stakeholders'].append({"stakeholder": "Construction Industry Stakeholders (Developers, Contractors, Architects, Quantity Surveyors)", "role": "Collaborators in the built environment; utilize or interact with services of Building Surveyors", "responsibilities": "(INFERRED) Engaging registered professionals, complying with regulations, collaborating on project delivery."})
process['stakeholders'].append({"stakeholder": "Property Owners / Developers", "role": "Clients for building surveying services; beneficiaries of regulated professional standards", "responsibilities": "(INFERRED) Engaging qualified building surveyors, understanding building regulations."})
process['stakeholders'].append({"stakeholder": "Educational Institutions (offering Building Surveying programs)", "role": "Provide academic training for aspiring Building Surveyors; collaborate with the Board on curriculum standards", "responsibilities": "(INFERRED) Developing relevant curricula, ensuring quality education, aligning with Board standards."})
process['stakeholders'].append({"stakeholder": "Professional Associations (e.g., Institution of Surveyors of Kenya - ISK, Building Surveyors Chapter)", "role": "Represent the interests of their members; collaborate with the Board on professional development and standards", "responsibilities": "(INFERRED) Advocating for members, promoting ethical conduct, advising the Board."})
process['stakeholders'].append({"stakeholder": "National Construction Authority (NCA)", "role": "Broader industry regulator; collaborates with the Board on ensuring building quality and safety", "responsibilities": "(INFERRED) Ensuring project compliance, collaborating on regulatory frameworks."})
process['stakeholders'].append({"stakeholder": "BORAQS (Board of Registration of Architects and Quantity Surveyors) (as a related built environment regulator)", "role": "Regulates allied professions in the built environment; potential collaborator on inter-professional matters", "responsibilities": "(INFERRED) Collaborating on inter-professional standards, sharing best practices."})
process['stakeholders'].append({"stakeholder": "Local Authorities / County Governments (for building approvals/inspections)", "role": "Enforce building regulations and development control at the local level; interact with Building Surveyors", "responsibilities": "(INFERRED) Issuing building permits, conducting site inspections, collaborating with surveyors."})
process['stakeholders'].append({"stakeholder": "Public / Clients (consuming services)", "role": "Beneficiaries of regulated professional standards and ethical conduct in building surveying", "responsibilities": "(INFERRED) Engaging qualified building surveyors, seeking redress for misconduct."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Lands, Public Works, Housing and Urban Development)", "role": "Parent Ministry providing policy direction, funding, and oversight to the Board", "responsibilities": "(INFERRED) Formulating built environment policies, ensuring regulatory alignment, strategic guidance."})

process['as_is_narrative'] = "(INFERRED) The Building Surveyors Registration Board actively regulates the building surveying profession in Kenya through a systematic process. It receives and processes applications from individuals seeking registration and licensing as building surveyors, conducting thorough assessments of their academic qualifications, practical training, and professional experience to ensure they meet the rigorous standards prescribed by the Building Surveyors Act. The Board maintains an official, up-to-date register of all licensed building surveyors and issues certificates of registration and annual practicing licenses. A core function involves developing and enforcing a comprehensive code of conduct and ethical standards, which all registered building surveyors must adhere to. The Board is responsible for investigating complaints of professional misconduct, negligence, or non-compliance against registered surveyors, conducting disciplinary hearings, and imposing appropriate sanctions, which can include suspension or removal from the register. It collaborates with relevant government agencies (e.g., National Construction Authority, County Governments), educational institutions (those offering building surveying programs), and professional associations (like the Institution of Surveyors of Kenya) within the built environment to ensure that the standards of practice are maintained, continuously improved, and that curricula remain relevant. Through these regulatory and oversight functions, the Board plays a vital role in safeguarding public interest in the quality, safety, and compliance of buildings, thereby contributing to the integrity and sustainable development of Kenya's built environment."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from reliable sources outlining the Act) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://policyvault.africa/", # Provided context (Building Surveyors Act No. 19 of 2018)
    "https://uonbi.ac.ke/", # Provided context (general Built Environment info)
    "https://boraqs.or.ke/" # Provided context (related built environment regulator)
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninety-ninth process enriched and combined_data.json updated.")
