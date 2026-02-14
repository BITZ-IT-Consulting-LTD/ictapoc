
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and ninth process (index 108)
process = data['processes'][108]

# Populate fields
process['executive_summary'] = "The Clinical Officers Council of Kenya (COC) is a government agency established under the Clinical Officers (Training, Registration and Licensing) Act No. 20 of 2017. Its primary mandate is to regulate the training, registration, licensing, and practice of Clinical Officers in Kenya. The Council ensures high standards of education, professional competence, and ethical conduct in clinical medicine practice, thereby safeguarding public health and maintaining the integrity of the clinical officer profession in the country."
process['process_overview']['process_objective'] = "To advise the government on policy matters concerning clinical medicine practice; to prescribe the minimum educational entry requirements for individuals aspiring to be trained as clinical officers; to approve institutions for the training of clinical officers and establish, approve, and accredit clinical medicine programs and continuing professional education programs; to register and license clinical officers; to maintain a comprehensive register and records of all clinical officers registered by the Council; to publish the names of all registered clinical officers in the Kenya Gazette every calendar year; to promote the development and adoption of codes of practice; to regulate professional conduct and ensure the maintenance and improvement of the standards of practice of clinical medicine; to administer pre-internship/licensure examinations to ensure the competency of clinical officers; to collaborate with other medical professional associations, organizations, and relevant bodies; to assess the qualifications of clinical officers; and to consider and address any other matters related to clinical officers, including prescribing badges, insignia, or uniforms."
process['process_overview']['policy_legal_context'].append("Established under the Clinical Officers (Training, Registration and Licensing) Act No. 20 of 2017, which provides the comprehensive legal framework for the regulation of the clinical officer profession in Kenya. COC operates under the Ministry of Health (or the relevant government ministry responsible for healthcare services) and is crucial for upholding professional standards in healthcare delivery, protecting public health, and ensuring that competent clinical officers deliver essential medical services across Kenya in line with national health policies.")
process['stakeholders'].append({"stakeholder": "Clinical Officers (aspiring and practicing)", "role": "Professionals whose training, registration, and practice are regulated by the Council", "responsibilities": "(INFERRED) Complying with the Act, adhering to professional standards, seeking registration/licensing, undertaking CPD."})
process['stakeholders'].append({"stakeholder": "Clinical Officer Training Institutions (Universities, Colleges)", "role": "Provide academic and practical training for aspiring Clinical Officers; approved and accredited by COC", "responsibilities": "(INFERRED) Developing relevant curricula, ensuring quality education, aligning with COC standards."})
process['stakeholders'].append({"stakeholder": "Ministry of Health", "role": "Parent Ministry providing policy direction, funding, and oversight to COC", "responsibilities": "(INFERRED) Formulating health policies, allocating resources, strategic guidance for healthcare human resources."})
process['stakeholders'].append({"stakeholder": "Kenya Medical Practitioners and Dentists Council (KMPDC) (for collaboration/oversight)", "role": "Regulates medical doctors and dentists; collaborates with COC on inter-professional matters in healthcare", "responsibilities": "(INFERRED) Collaborating on inter-professional standards, sharing best practices, ensuring coordinated healthcare."})
process['stakeholders'].append({"stakeholder": "National Nurses Council of Kenya (NNCK) (for collaboration)", "role": "Regulates nursing professionals; collaborates with COC on inter-professional matters in healthcare", "responsibilities": "(INFERRED) Collaborating on inter-professional standards, sharing best practices, ensuring coordinated healthcare."})
process['stakeholders'].append({"stakeholder": "Kenya Medical Training College (KMTC)", "role": "Key institution for training clinical officers; its programs are approved by COC", "responsibilities": "(INFERRED) Providing quality training, adhering to COC accreditation standards."})
process['stakeholders'].append({"stakeholder": "Healthcare Facilities (Hospitals, Clinics)", "role": "Employ clinical officers and provide training sites for interns; impacted by COC's standards", "responsibilities": "(INFERRED) Employing licensed clinical officers, providing internship opportunities, maintaining quality healthcare services."})
process['stakeholders'].append({"stakeholder": "Patients / Public", "role": "Primary beneficiaries of regulated and competent clinical officer services; their health and safety are protected by COC", "responsibilities": "(INFERRED) Seeking healthcare services, providing feedback, exercising patient rights."})
process['stakeholders'].append({"stakeholder": "Clinical Officers' Associations (e.g., Kenya Union of Clinical Officers - KUCO)", "role": "Represent the interests of clinical officers; collaborate with COC on professional welfare and standards", "responsibilities": "(INFERRED) Advocating for members, promoting professional development, advising COC."})
process['stakeholders'].append({"stakeholder": "Kenya National Examinations Council (KNEC) (for national examinations/assessments)", "role": "May collaborate with COC on national assessments for clinical officer training programs", "responsibilities": "(INFERRED) Setting examination standards, conducting assessments."})

process['as_is_narrative'] = "(INFERRED) The Clinical Officers Council of Kenya (COC) actively regulates the clinical officer profession through a multi-stage and continuous process. It begins by establishing and periodically reviewing the minimum academic and professional requirements for individuals aspiring to train as clinical officers, ensuring that entry-level practitioners possess a strong foundation. The Council then rigorously approves and accredits clinical officer training institutions and their programs (diploma, higher diploma, degree levels), continuously monitoring their adherence to quality education standards. A critical step involves administering stringent pre-internship and/or licensure examinations to assess the competency and readiness of graduates for practice. COC maintains a comprehensive, up-to-date register of all qualified and licensed clinical officers in Kenya, which is also published annually in the Kenya Gazette for public verification. The Council develops and enforces a strict code of professional conduct and ethical guidelines, ensuring that clinical officers provide care with integrity and adhere to the highest ethical standards. It actively investigates complaints of professional misconduct or negligence lodged against clinical officers and initiates disciplinary actions, including suspension or revocation of licenses. To ensure practitioners stay abreast of medical advancements, COC promotes and approves Continuous Professional Development (CPD) programs. The Council advises the Ministry of Health on policy matters affecting clinical medicine practice and collaborates closely with other healthcare regulatory bodies (e.g., KMPDC, NNCK) and professional associations (e.g., KUCO) to foster a harmonized, high-quality healthcare system that effectively serves the Kenyan population."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.clinicalofficerscouncil.org/", # Official website
    "https://wikipedia.org/", # Provided context
    "https://business.blog/", # Provided context
    "https://www.who.int/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and ninth process enriched and combined_data.json updated.")
