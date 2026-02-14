
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninety-seventh process (index 96)
process = data['processes'][96]

# Populate fields
process['executive_summary'] = "Bomet University (formerly Bomet University College) is a public university in Kenya, established as a Constituent College of Moi University in 2017 and later granted a Charter on February 4, 2026, making it an independent university and the 36th public university in Kenya. It is the first public university in Bomet County. Its vision is to be a premier Green University fostering research excellence in Science, Technology, and Innovation for sustainability, providing quality education, and nurturing critical inquiry, creativity, and engagement for social transformation and the advancement of humanity."
process['process_overview']['process_objective'] = "To provide quality education and foster innovation across a diverse range of academic programs, including certificate, diploma, undergraduate, and postgraduate courses, in various schools such as Arts and Social Sciences, Pure & Applied Sciences, Business and Entrepreneurship, and Education; to develop creativity and innovation in students to prepare them for the job market; to adopt a practical learning approach emphasizing attachments and fieldwork, and integrating ICT into student training; to champion quality education, sustainability, and innovation within Kenya's higher education sector; to foster creative and critical thinking, contributing to the discovery, preservation, and dissemination of knowledge; to stimulate students' intellectual engagement in economic, socio-cultural, scientific, and technological development; and to operate with a niche in 'Green Economy for Sustainability' and a motto of 'Green University for Sustainability'."
process['process_overview']['policy_legal_context'].append("Established as a Constituent College of Moi University under Legal Notice Number 145 of July 27, 2017, and subsequently granted a Charter on February 4, 2026, making it an independent university. Bomet University operates under the Universities Act, 2012, and relevant higher education regulations. It aligns its mandates with Kenya's national development agenda, including Vision 2030 and the Bottom-Up Economic Transformation Agenda (BETA), with a specific focus on contributing to sustainable development through its 'Green Economy for Sustainability' niche.")
process['stakeholders'].append({"stakeholder": "Students (Prospective and Current)", "role": "Primary beneficiaries of the university's education and training programs; future workforce and researchers", "responsibilities": "(INFERRED) Engaging in academic pursuits, participating in research, contributing to university life, upholding academic integrity."})
process['stakeholders'].append({"stakeholder": "Faculty / Academic Staff", "role": "Deliver education, conduct research, and engage in community service; crucial for academic excellence", "responsibilities": "(INFERRED) Teaching, mentoring students, conducting research, publishing scholarly work, professional development."})
process['stakeholders'].append({"stakeholder": "Non-Teaching Staff", "role": "Provide administrative and support services essential for the university's operations and student welfare", "responsibilities": "(INFERRED) Supporting academic programs, maintaining facilities, managing university resources, student support services."})
process['stakeholders'].append({"stakeholder": "Moi University (former parent institution)", "role": "Provided mentorship and academic oversight during Bomet University College's establishment phase", "responsibilities": "(INFERRED) Collaborating on academic programs, institutional development, quality assurance."})
process['stakeholders'].append({"stakeholder": "Commission for University Education (CUE)", "role": "Regulatory body for university education in Kenya; ensures quality and accreditation of programs", "responsibilities": "(INFERRED) Setting academic standards, accrediting programs, monitoring compliance, licensing universities."})
process['stakeholders'].append({"stakeholder": "Bomet County Government", "role": "Local government partner; benefits from skilled human capital and research addressing local challenges", "responsibilities": "(INFERRED) Collaborating on local development projects, supporting university initiatives, utilizing research findings."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Beneficiaries of community outreach programs, research findings, and employment opportunities", "responsibilities": "(INFERRED) Collaborating on community projects, utilizing university resources, providing feedback."})
process['stakeholders'].append({"stakeholder": "Employers / Industry", "role": "Potential employers of graduates; partners in curriculum development and internships; benefit from research", "responsibilities": "(INFERRED) Employing graduates, providing internships, advising on curriculum relevance, collaborating on research."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Collaborators on research projects and knowledge generation, especially in sustainability and green economy", "responsibilities": "(INFERRED) Partnering on research, sharing data, disseminating findings, collaborating on studies."})
process['stakeholders'].append({"stakeholder": "Funding Agencies / Donors", "role": "Provide financial support for research, infrastructure, and student scholarships", "responsibilities": "(INFERRED) Funding projects, supporting educational initiatives, ensuring accountability."})
process['stakeholders'].append({"stakeholder": "Alumni", "role": "Former students who contribute to the university's reputation and often provide support and mentorship", "responsibilities": "(INFERRED) Mentoring current students, donating to the university, promoting the institution."})
process['stakeholders'].append({"stakeholder": "Other Universities", "role": "Collaborators on academic programs, research, and staff exchange; engage in benchmarking", "responsibilities": "(INFERRED) Partnering on joint programs, sharing best practices, fostering academic collaboration."})

process['as_is_narrative'] = "(INFERRED) Bomet University actively fulfills its mandate by developing and delivering a diverse range of academic programs from certificate to postgraduate levels, with a unique focus on 'Green Economy for Sustainability'. Its curriculum is designed to equip students with not only theoretical knowledge but also practical skills, emphasizing attachments, fieldwork, and the integration of Information and Communication Technology (ICT) to enhance their employability and entrepreneurial capabilities. The university conducts cutting-edge research in science, technology, and innovation, particularly focusing on sustainable solutions to local and national challenges, and disseminates this knowledge through publications, conferences, and community engagement. Bomet University is deeply involved in community outreach programs, applying academic expertise to address real-world problems in Bomet County and beyond, thereby fostering socio-economic development. It maintains rigorous internal quality assurance mechanisms, adhering to standards set by the Commission for University Education (CUE), and continuously evaluates and improves its academic programs and administrative processes. The university cultivates an environment that encourages creativity and critical thinking among its students and staff. Furthermore, Bomet University establishes strategic partnerships with industry, government agencies, and other academic institutions for collaborative research, student internships, and curriculum development, playing a pivotal role in the human capital development of its region and Kenya as a whole."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.bu.ac.ke/", # Official website
    "https://bomet.co.ke/", # Provided context
    "https://wikipedia.org/", # Provided context
    "https://somo.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninety-seventh process enriched and combined_data.json updated.")
