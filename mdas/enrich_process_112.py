
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and thirteenth process (index 112)
process = data['processes'][112]

# Populate fields
process['executive_summary'] = "The Commission for University Education (CUE) Kenya is a statutory body established under the Universities Act No. 42 of 2012, becoming fully operational in 2013 as the successor to the Commission for Higher Education (CHE). CUE's primary mandate is to promote the objectives of university education by regulating and assuring the quality of university education in Kenya, including accreditation of universities and their programs. It plays a crucial role in protecting the interests of students and the public, ensuring that universities provide relevant and high-quality education aligned with national development priorities."
process['process_overview']['process_objective'] = "To promote the objectives of university education; to advise the Cabinet Secretary on policy matters related to university education; to promote, advance, publicize, and set standards relevant to the quality of university education, including supporting internationally recognized standards; to regulate university education in Kenya by setting frameworks for governance, curriculum delivery, and academic services; to accredit universities in Kenya by granting Charters or Letters of Interim Authority, and approving and inspecting university programs; to monitor and evaluate the state of university education systems in relation to national development goals, assessing program quality, and teaching methodologies; to license student recruitment agencies operating in Kenya and activities by foreign institutions; to develop policy for criteria and requirements for admission to universities; to recognize and equate degrees, diplomas, and certificates conferred or awarded by foreign universities and institutions according to established standards and guidelines; to undertake regular inspections, monitoring, and evaluation of universities to ensure compliance with the provisions of the Universities Act; to collect, disseminate, and maintain data on university education; and to promote quality research and innovation within universities."
process['process_overview']['policy_legal_context'].append("Established under the Universities Act No. 42 of 2012 (fully operational in 2013), which provides the comprehensive legal and regulatory framework for university education in Kenya. CUE operates under the Ministry of Education and is crucial for implementing national higher education policies, ensuring quality assurance, and aligning university education with national development priorities (e.g., Vision 2030) and international standards. It plays a central role in the governance and development of the university sector.")
process['stakeholders'].append({"stakeholder": "Universities (Public and Private in Kenya)", "role": "Institutions offering university education; subject to CUE's regulation, accreditation, and quality assurance", "responsibilities": "(INFERRED) Complying with CUE standards, seeking accreditation, providing quality education."})
process['stakeholders'].append({"stakeholder": "University Students (Prospective and Current)", "role": "Primary beneficiaries of quality university education; their interests are protected by CUE", "responsibilities": "(INFERRED) Engaging in learning, understanding program requirements, providing feedback on quality."})
process['stakeholders'].append({"stakeholder": "Ministry of Education", "role": "Parent Ministry providing policy direction, funding, and oversight to the university sector", "responsibilities": "(INFERRED) Formulating education policies, allocating resources, strategic guidance for higher education."})
process['stakeholders'].append({"stakeholder": "National Treasury", "role": "Provides funding to public universities and CUE; involved in higher education financing policies", "responsibilities": "(INFERRED) Allocating budgetary resources, ensuring financial accountability in higher education."})
process['stakeholders'].append({"stakeholder": "Kenya National Examinations Council (KNEC)", "role": "Administers national examinations at various levels; CUE may collaborate on assessment standards", "responsibilities": "(INFERRED) Setting examination standards, collaborating on assessment quality."})
process['stakeholders'].append({"stakeholder": "Teachers Service Commission (TSC)", "role": "Manages teachers in basic education; CUE may collaborate on teacher training programs at universities", "responsibilities": "(INFERRED) Managing teacher workforce, ensuring quality teacher training."})
process['stakeholders'].append({"stakeholder": "Kenya Institute of Curriculum Development (KICD)", "role": "Develops curriculum for basic education; CUE ensures university curricula align with national needs", "responsibilities": "(INFERRED) Developing curricula, ensuring alignment with higher education."})
process['stakeholders'].append({"stakeholder": "Professional Bodies (e.g., KMPDC, EBK, BORAQS)", "role": "Regulate specific professions; collaborate with CUE on curriculum relevance and professional recognition of university programs", "responsibilities": "(INFERRED) Setting professional standards, advising on curriculum content, accrediting professionals."})
process['stakeholders'].append({"stakeholder": "Employers / Industry", "role": "Consumers of university graduates; partners in curriculum development and research", "responsibilities": "(INFERRED) Employing graduates, providing internships, advising on curriculum relevance, collaborating on research."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Collaborators on research projects and knowledge generation; may host university students/faculty", "responsibilities": "(INFERRED) Partnering on research, sharing data, disseminating findings."})
process['stakeholders'].append({"stakeholder": "Parents / Guardians", "role": "Stakeholders interested in the quality and relevance of university education for their children", "responsibilities": "(INFERRED) Funding university education, providing support to students."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support university education and research initiatives", "responsibilities": "(INFERRED) Funding projects, supporting educational reforms, capacity building."})
process['stakeholders'].append({"stakeholder": "Foreign Universities / Institutions", "role": "May collaborate with Kenyan universities or have their qualifications recognized by CUE", "responsibilities": "(INFERRED) Collaborating on academic programs, seeking recognition for qualifications."})

process['as_is_narrative'] = "(INFERRED) The Commission for University Education (CUE) implements its extensive mandate through a continuous cycle of regulation, quality assurance, and promotion of university education. Its operations commence with the rigorous evaluation of applications for the establishment of new universities and the granting of charters or letters of interim authority. CUE develops, reviews, and enforces stringent standards and guidelines that govern all aspects of university operations, including governance structures, academic programs, student admissions, staff qualifications, research infrastructure, and quality assurance mechanisms. A core function involves receiving, evaluating, and accrediting new academic programs and conducting periodic reviews of existing ones to ensure their relevance, quality, and alignment with national and international benchmarks. CUE undertakes regular inspections, monitoring visits, and quality audits of universities across the country to verify compliance with the Universities Act and CUE standards, taking corrective actions where necessary. The Commission serves as a key advisor to the Cabinet Secretary on policy matters affecting university education, contributing significantly to the formulation of national higher education strategies and reforms. It collects, analyzes, and disseminates comprehensive data on university education, which is vital for national planning and decision-making. CUE is also responsible for recognizing and equating degrees, diplomas, and certificates awarded by foreign universities, ensuring their comparability to Kenyan qualifications. Furthermore, it actively promotes quality research and innovation within the university system and investigates complaints lodged against universities or their programs, mediating disputes and taking enforcement actions against institutions found to be in breach of regulations, thereby safeguarding the interests of students and the public."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.cue.or.ke/", # Official website
    "https://unirank.org/", # Provided context
    "https://businessradar.co.ke/", # Provided context
    "https://wikipedia.org/", # Provided context
    "https://institutiontoday.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and thirteenth process enriched and combined_data.json updated.")
