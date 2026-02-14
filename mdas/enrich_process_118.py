
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and nineteenth process (index 118)
process = data['processes'][118]

# Populate fields
process['executive_summary'] = "The Counsellors and Psychologists Board in Kenya was established on August 5, 2022, under Section 3 of the Counsellors and Psychologists Act No. 14 of 2014. Its core mission is to regulate and streamline the counselling and psychology professions in Kenya, ensuring they adhere to the highest standards of professional practice and ethical conduct. The Board plays a crucial role in protecting consumers, building client trust, fostering the growth and development of these vital mental health professions, and promoting mental well-being in the country."
process['process_overview']['process_objective'] = "To regulate the education and professional standards of practice for counsellors and psychologists in Kenya; to register and license qualified counsellors and psychologists; to set benchmarks for excellence within the professions; to ensure consumer protection by safeguarding clients from unethical or incompetent practice; to promote professional conduct and ethical practice among all practitioners; to support continuous professional growth and provide ethical guidance to members; to offer online services for registration, Continuing Professional Development (CPD) training, practicing licenses, and the registration and licensing of counselling/psychological facilities; and to handle administrative matters, assurance services, public entities oversight, audit, legal & regulatory compliance, and steer reforms in governance and public service within the mental health sector."
process['process_overview']['policy_legal_context'].append("Established on August 5, 2022, under Section 3 of the Counsellors and Psychologists Act No. 14 of 2014, which provides the comprehensive legal and regulatory framework for the counselling and psychology professions in Kenya. The Board operates under the Ministry of Health (or the relevant government ministry responsible for mental health services) and is crucial for implementing national mental health policies, ensuring quality mental health services, and safeguarding public well-being through professional regulation and oversight.")
process['stakeholders'].append({"stakeholder": "Counsellors (aspiring and practicing)", "role": "Professionals whose training, registration, and practice are regulated by the Board", "responsibilities": "(INFERRED) Complying with the Act, adhering to professional standards, seeking registration/licensing, undertaking CPD."})
process['stakeholders'].append({"stakeholder": "Psychologists (aspiring and practicing)", "role": "Professionals whose training, registration, and practice are regulated by the Board", "responsibilities": "(INFERRED) Complying with the Act, adhering to professional standards, seeking registration/licensing, undertaking CPD."})
process['stakeholders'].append({"stakeholder": "Clients / Patients seeking counselling/psychological services", "role": "Primary beneficiaries of regulated and ethical mental health services; their well-being is protected by the Board", "responsibilities": "(INFERRED) Seeking professional help, providing feedback, exercising client rights."})
process['stakeholders'].append({"stakeholder": "Training Institutions (Universities, Colleges offering Counselling/Psychology programs)", "role": "Provide academic and practical training for aspiring counsellors and psychologists; approved by the Board", "responsibilities": "(INFERRED) Developing relevant curricula, ensuring quality education, aligning with Board standards."})
process['stakeholders'].append({"stakeholder": "Ministry of Health", "role": "Parent Ministry providing policy direction, funding, and oversight to the Board", "responsibilities": "(INFERRED) Formulating mental health policies, allocating resources, strategic guidance for mental health services."})
process['stakeholders'].append({"stakeholder": "Kenya Medical Practitioners and Dentists Council (KMPDC) (for collaboration)", "role": "Regulates medical doctors and dentists; collaborates with the Board on inter-professional matters in healthcare", "responsibilities": "(INFERRED) Collaborating on inter-professional standards, sharing best practices, ensuring coordinated healthcare."})
process['stakeholders'].append({"stakeholder": "National Nurses Council of Kenya (NNCK) (for collaboration)", "role": "Regulates nursing professionals; collaborates with the Board on inter-professional matters in healthcare", "responsibilities": "(INFERRED) Collaborating on inter-professional standards, sharing best practices, ensuring coordinated healthcare."})
process['stakeholders'].append({"stakeholder": "Kenya National Association of Counsellors and Psychologists (KNACP)", "role": "Professional association for counsellors and psychologists; collaborates with the Board on professional welfare and standards", "responsibilities": "(INFERRED) Advocating for members, promoting professional development, advising the Board."})
process['stakeholders'].append({"stakeholder": "Professional Associations / Societies", "role": "Represent specific interests within the counselling and psychology fields; collaborate with the Board", "responsibilities": "(INFERRED) Setting specialized standards, providing professional development, advising the Board."})
process['stakeholders'].append({"stakeholder": "Healthcare Facilities", "role": "Employ counsellors and psychologists and provide mental health services; impacted by the Board's standards", "responsibilities": "(INFERRED) Employing licensed professionals, providing mental health services, maintaining quality care."})
process['stakeholders'].append({"stakeholder": "Government Agencies (e.g., Department of Children Services, Judiciary)", "role": "Collaborators in providing holistic support and protection, especially for vulnerable populations", "responsibilities": "(INFERRED) Referring cases, collaborating on interventions, enforcing mental health-related laws."})
process['stakeholders'].append({"stakeholder": "Public", "role": "General public seeking mental health services or impacted by the professions", "responsibilities": "(INFERRED) Seeking mental health support, providing feedback, relying on regulated services."})

process['as_is_narrative'] = "(INFERRED) The Counsellors and Psychologists Board actively regulates the counselling and psychology professions in Kenya through a systematic and comprehensive framework. It establishes and enforces minimum education and training requirements for individuals aspiring to become counsellors and psychologists, ensuring they meet the necessary academic and practical qualifications. The Board receives and processes applications for registration and licensing from qualified individuals, conducting thorough vetting and, where applicable, administering examinations or assessments to ensure professional competence. It maintains a comprehensive and up-to-date register of all licensed practitioners and facilities, ensuring transparency and public accessibility. A core function involves developing and enforcing a strict code of ethical conduct and professional standards, which all registered counsellors and psychologists must adhere to, thereby safeguarding client well-being and building public trust. The Board actively investigates complaints of professional misconduct or negligence lodged against practitioners and initiates disciplinary actions, including suspension or revocation of licenses, as stipulated by the Counsellors and Psychologists Act. It promotes and accredits Continuous Professional Development (CPD) programs, compelling practitioners to stay abreast of new therapeutic techniques, research, and ethical guidelines. The Board advises the Ministry of Health on policy matters affecting counselling and psychology practice and collaborates closely with other healthcare regulatory bodies (e.g., KMPDC, NNCK) and professional associations (e.g., KNACP) to ensure a harmonized and high-quality mental health service delivery system. It also provides accessible online services for various regulatory processes, enhancing efficiency and transparency for practitioners and the public alike, ultimately strengthening mental health care in Kenya."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://cpb.health.go.ke/", # Official website
    "https://health.go.ke/", # Provided context
    "https://ecitizen.go.ke/", # Provided context
    "https://therapyroute.com/", # Provided context
    "https://wordpress.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and nineteenth process enriched and combined_data.json updated.")
