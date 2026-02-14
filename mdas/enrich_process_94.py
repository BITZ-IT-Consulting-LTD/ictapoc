
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninety-fifth process (index 94)
process = data['processes'][94]

# Populate fields
process['executive_summary'] = "The Board of Registration of Architects and Quantity Surveyors (BORAQS) is the primary regulatory body for the professions of Architecture and Quantity Surveying in Kenya. Established under an Act of Parliament, its core mandate is to regulate training, registration, and enhance ethical and professional practice within these fields. BORAQS plays a crucial role in ensuring high standards for the built environment, protecting public interest, and promoting competence among professionals in the construction industry."
process['process_overview']['process_objective'] = "To regulate and oversee the professions of Architecture and Quantity Surveying; to register Architects, Quantity Surveyors, and architectural/quantity surveying firms; to conduct and administer professional examinations for aspiring Architects and Quantity Surveyors; to organize and accredit Continuous Professional Development (CPD) seminars for registered professionals; to define professional conduct and make by-laws to address unprofessional conduct, including inquiry procedures and penalties; to set standards for the development and general practice of architecture and quantity surveying in Kenya; to advise on matters related to the welfare of practicing Architects and Quantity Surveyors, and on research and publication related to the practice; and to collaborate with training institutions (universities and colleges) to ensure quality education and training."
process['process_overview']['policy_legal_context'].append("Established under the Architects and Quantity Surveyors Act, Cap 525 of the Laws of Kenya (or relevant current legislation), which provides the legal framework for its mandate, functions, and the regulation of the professions. BORAQS operates under the Ministry of Lands, Public Works, Housing and Urban Development (or the relevant government ministry responsible for the built environment) and is crucial for upholding professional standards, ensuring public safety, and contributing to the integrity and quality of construction and infrastructure development in Kenya.")
process['stakeholders'].append({"stakeholder": "Architects (registered and aspiring)", "role": "Practicing professionals and candidates who must comply with BORAQS's regulations and licensing requirements", "responsibilities": "(INFERRED) Registering with BORAQS, adhering to professional ethics, undertaking CPD, providing architectural services."})
process['stakeholders'].append({"stakeholder": "Quantity Surveyors (registered and aspiring)", "role": "Practicing professionals and candidates who must comply with BORAQS's regulations and licensing requirements", "responsibilities": "(INFERRED) Registering with BORAQS, adhering to professional ethics, undertaking CPD, providing quantity surveying services."})
process['stakeholders'].append({"stakeholder": "Architectural Firms", "role": "Companies providing architectural services; registered by BORAQS", "responsibilities": "(INFERRED) Employing registered architects, complying with firm registration requirements."})
process['stakeholders'].append({"stakeholder": "Quantity Surveying Firms", "role": "Companies providing quantity surveying services; registered by BORAQS", "responsibilities": "(INFERRED) Employing registered quantity surveyors, complying with firm registration requirements."})
process['stakeholders'].append({"stakeholder": "Construction Industry Stakeholders (Clients, Contractors, Developers)", "role": "Utilize services of Architects and Quantity Surveyors; affected by professional standards and ethics", "responsibilities": "(INFERRED) Engaging registered professionals, complying with contracts, adhering to industry best practices."})
process['stakeholders'].append({"stakeholder": "National Construction Authority (NCA)", "role": "Collaborates with BORAQS on regulating the broader construction industry and project oversight", "responsibilities": "(INFERRED) Ensuring project compliance, collaborating on regulatory frameworks."})
process['stakeholders'].append({"stakeholder": "Kenya National Bureau of Statistics (KNBS) (for industry data)", "role": "Collects data relevant to the construction sector; potentially utilizes BORAQS data", "responsibilities": "(INFERRED) Collecting and disseminating statistical data relevant to economic sectors."})
process['stakeholders'].append({"stakeholder": "Training Institutions (Universities, Colleges offering Arch/QS programs)", "role": "Educate and train aspiring Architects and Quantity Surveyors; collaborate with BORAQS on curriculum standards", "responsibilities": "(INFERRED) Developing relevant curricula, providing quality education, aligning with BORAQS standards."})
process['stakeholders'].append({"stakeholder": "Professional Associations (e.g., Architectural Association of Kenya (AAK), Institute of Quantity Surveyors of Kenya (IQSK))", "role": "Represent the interests of their members; collaborate with BORAQS on professional standards and welfare", "responsibilities": "(INFERRED) Advocating for members, promoting professional development, advising BORAQS."})
process['stakeholders'].append({"stakeholder": "Public / Clients (consuming services)", "role": "Beneficiaries of high professional standards and ethical conduct in the built environment", "responsibilities": "(INFERRED) Engaging qualified professionals, seeking redress for misconduct."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Lands, Public Works, Housing and Urban Development)", "role": "Parent Ministry providing policy direction, funding, and oversight to BORAQS", "responsibilities": "(INFERRED) Formulating built environment policies, ensuring regulatory alignment, strategic guidance."})

process['as_is_narrative'] = "(INFERRED) The Board of Registration of Architects and Quantity Surveyors (BORAQS) ensures the highest standards in the architectural and quantity surveying professions through a multi-stage regulatory process. It meticulously reviews the academic qualifications and practical experience of individuals applying for registration, followed by the administration of rigorous professional examinations for aspiring architects and quantity surveyors to assess their competence. Upon successful completion, BORAQS issues and annually renews practicing licenses for qualified individuals and firms. A core function is the development, dissemination, and enforcement of a comprehensive code of ethics and professional conduct, which guides the practice of its registered members. The Board actively investigates complaints of professional misconduct or negligence lodged by clients or other stakeholders and takes appropriate disciplinary actions, ranging from reprimands to suspension or revocation of licenses, to protect the public interest. BORAQS organizes and accredits Continuous Professional Development (CPD) programs, compelling its members to stay abreast of new technologies, regulations, and best practices in the dynamic construction industry. It establishes and maintains standards and guidelines for various aspects of architectural and quantity surveying practice, including fees and scope of services. The Board advises the government on policy and legislative matters impacting the built environment professions, maintains an official public register of all licensed professionals and firms for transparency, and collaborates closely with universities and professional associations to ensure that educational curricula meet industry needs and foster a pipeline of competent professionals."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.boraqs.or.ke/", # Official website
    "https://investkenya.go.ke/", # Provided context
    "https://constructionreviewonline.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninety-fifth process enriched and combined_data.json updated.")
