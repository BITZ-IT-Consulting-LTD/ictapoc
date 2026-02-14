
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and eighteenth process (index 117)
process = data['processes'][117]

# Populate fields
process['executive_summary'] = "The Council of Legal Education (CLE) in Kenya is a state corporation established in 2014 under the Legal Education Act No. 27 of 2012. Its primary mandate is to regulate legal education and training offered by legal education providers in Kenya, including licensing and supervising these providers, advising the Government on legal education matters, and administering the Advocates Training Programme (ATP) examination. CLE plays a critical role in ensuring high standards of legal training and professional competence, thereby upholding the integrity of the legal profession and ensuring access to justice in the country."
process['process_overview']['process_objective'] = "To regulate legal education and training offered by legal education providers in Kenya; to license and supervise legal education providers; to advise the Government on matters related to legal education and training; to recognize and approve qualifications obtained outside Kenya for admission to the Roll of Advocates; to administer the Advocates Training Programme (ATP) examination; to make regulations concerning admission requirements for legal education programs; to establish criteria for recognizing and equating academic qualifications in legal education; to formulate a system for recognizing prior learning and experience in law; to establish a system of equivalencies for legal educational qualifications and credit transfers; and to oversee the accreditation of legal education providers, curricula and mode of instruction, mode and quality of examinations, harmonization of legal education programs, and monitoring and evaluation of providers and programs."
process['process_overview']['policy_legal_context'].append("Established in 2014 under the Legal Education Act No. 27 of 2012, which provides the comprehensive legal framework for the regulation of legal education and training in Kenya. CLE operates under the State Law Office in the Office of the Attorney General and Department of Justice and is crucial for implementing national policies on legal education, ensuring quality legal training, and upholding the integrity of the legal profession in Kenya, thereby contributing to the rule of law and access to justice.")
process['stakeholders'].append({"stakeholder": "Legal Education Providers (Universities, Kenya School of Law)", "role": "Institutions offering legal education and training; licensed and supervised by CLE", "responsibilities": "(INFERRED) Developing curricula, providing quality legal education, seeking accreditation, complying with CLE standards."})
process['stakeholders'].append({"stakeholder": "Law Students (Prospective and Current)", "role": "Primary beneficiaries of regulated legal education and training; aspiring legal practitioners", "responsibilities": "(INFERRED) Engaging in legal studies, meeting admission requirements, preparing for ATP examinations."})
process['stakeholders'].append({"stakeholder": "Legal Practitioners (Advocates)", "role": "Professionals who have undergone CLE-regulated training; their competence is assured by CLE's oversight", "responsibilities": "(INFERRED) Adhering to professional ethics, undertaking continuing legal education, contributing to the legal profession."})
process['stakeholders'].append({"stakeholder": "Judiciary", "role": "Utilizes legal professionals trained and regulated under CLE's framework; benefits from competent legal services", "responsibilities": "(INFERRED) Administering justice, providing input on legal education needs, collaborating on legal reforms."})
process['stakeholders'].append({"stakeholder": "Office of the Attorney General and Department of Justice", "role": "Parent body for CLE; provides policy direction and oversight", "responsibilities": "(INFERRED) Formulating legal policies, strategic guidance for legal education and justice sector."})
process['stakeholders'].append({"stakeholder": "Law Society of Kenya (LSK)", "role": "Professional body for advocates; collaborates with CLE on professional standards and entry to the Bar", "responsibilities": "(INFERRED) Regulating advocates' conduct, advocating for legal profession, collaborating on legal education."})
process['stakeholders'].append({"stakeholder": "Commission for University Education (CUE)", "role": "Regulatory body for university education; collaborates with CLE on university law programs", "responsibilities": "(INFERRED) Accrediting university programs, ensuring quality higher education."})
process['stakeholders'].append({"stakeholder": "Kenya National Examinations Council (KNEC)", "role": "May collaborate with CLE on national assessments or examinations", "responsibilities": "(INFERRED) Setting examination standards, conducting assessments."})
process['stakeholders'].append({"stakeholder": "International Legal Education Bodies", "role": "Sources of global best practices in legal education; CLE collaborates on international standards and recognition", "responsibilities": "(INFERRED) Setting global legal education standards, facilitating international cooperation."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Education)", "role": "Provides policy guidance and support for education sector, including legal education", "responsibilities": "(INFERRED) Formulating education policies, allocating resources."})
process['stakeholders'].append({"stakeholder": "Public / Clients of Legal Services", "role": "Beneficiaries of competent and ethical legal professionals trained under CLE's framework", "responsibilities": "(INFERRED) Seeking legal services, expecting ethical and competent representation."})

process['as_is_narrative'] = "(INFERRED) The Council of Legal Education (CLE) actively implements its mandate through a multi-faceted regulatory framework to ensure the quality and integrity of legal education and training in Kenya. It establishes and enforces minimum admission requirements for all legal education programs, ensuring that only qualified candidates are admitted. CLE rigorously approves and licenses institutions (both universities and the Kenya School of Law) that offer legal education, and continuously monitors their compliance with prescribed standards for curricula, mode of instruction, and examinations. A critical function involves administering the Advocates Training Programme (ATP) examination, which assesses the practical competence of aspiring advocates before they can be admitted to the Roll of Advocates. CLE maintains a comprehensive database of legal education providers and their accredited programs, providing transparency and information to the public. It advises the Government on policy and legislative matters pertaining to legal education and training, contributing to the development of national strategies for the legal sector. The Council collaborates closely with regulatory bodies such as the Law Society of Kenya (LSK) and the Judiciary to ensure harmonization of legal education with professional practice requirements. Furthermore, CLE is responsible for recognizing and equating foreign legal qualifications, ensuring that those trained outside Kenya meet local standards for practice. It also formulates systems for recognizing prior learning and experience in law and for credit transfers, promoting flexibility and accessibility in legal education. Through these activities, CLE plays a vital role in upholding the standards of legal professionalism and ultimately ensuring access to competent legal services and justice in Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.cle.or.ke/", # Official website
    "https://afro.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and eighteenth process enriched and combined_data.json updated.")
