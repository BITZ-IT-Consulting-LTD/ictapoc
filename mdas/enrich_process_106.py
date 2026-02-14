
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and seventh process (index 106)
process = data['processes'][106]

# Populate fields
process['executive_summary'] = "Chuka University is a premier public university in Kenya, established with a mission to generate, preserve, and share knowledge for effective leadership in higher education, training, research, and outreach. It aims to deliver quality university education across technological, scientific, and professional fields, fostering an intellectual culture that combines theoretical understanding with practical application, innovation, and entrepreneurship. Chuka University contributes significantly to sustainable national and global development by producing skilled human resources, generating new knowledge, and engaging with communities to address societal challenges."
process['process_overview']['process_objective'] = "To provide facilities for quality university education across various disciplines, encompassing technological, scientific, and professional fields; to advance university education and training to qualified candidates, leading to the conferment of degrees, diplomas, and certificates, thereby contributing to sustainable national economic and social development; to offer programs, products, and services that uphold principles of equity and social justice; to facilitate the development and provision of relevant academic programs and community services; to maintain and enhance the quality of teaching, learning, research, creativity, innovation, and community outreach activities; and to expand its academic programs, particularly in science and technology (e.g., Food Science and Technology), to develop human resources capable of adding value to agricultural products and ensuring food and nutrition security in Kenya."
process['process_overview']['policy_legal_context'].append("Chuka University operates under the Universities Act, 2012, and other relevant higher education regulations, which provide the legal and regulatory framework for its establishment and functions. It aligns its mandates with Kenya's national development agenda, including Vision 2030, and national policies on education, science, technology, and innovation, contributing to the country's human capital development goals and the advancement of knowledge for societal benefit. The university is governed by its charter and council.")
process['stakeholders'].append({"stakeholder": "Students (Undergraduate, Postgraduate)", "role": "Primary beneficiaries of the university's education and training programs; future workforce and researchers", "responsibilities": "(INFERRED) Engaging in academic pursuits, participating in research, contributing to university life, upholding academic integrity."})
process['stakeholders'].append({"stakeholder": "Faculty / Academic Staff", "role": "Deliver education, conduct research, and engage in community service; crucial for academic excellence", "responsibilities": "(INFERRED) Teaching, mentoring students, conducting research, publishing scholarly work, professional development."})
process['stakeholders'].append({"stakeholder": "Non-Teaching Staff", "role": "Provide administrative and support services essential for the university's operations and student welfare", "responsibilities": "(INFERRED) Supporting academic programs, maintaining facilities, managing university resources, student support services."})
process['stakeholders'].append({"stakeholder": "Commission for University Education (CUE)", "role": "Regulatory body for university education in Kenya; ensures quality and accreditation of programs", "responsibilities": "(INFERRED) Setting academic standards, accrediting programs, monitoring compliance, licensing universities."})
process['stakeholders'].append({"stakeholder": "Ministry of Education", "role": "Parent Ministry providing policy direction, funding, and oversight to universities", "responsibilities": "(INFERRED) Formulating education policies, allocating resources, strategic guidance for higher education."})
process['stakeholders'].append({"stakeholder": "Local Communities (Tharaka Nithi County and surrounding regions)", "role": "Beneficiaries of community outreach programs, research findings, and employment opportunities", "responsibilities": "(INFERRED) Collaborating on community projects, utilizing university resources, providing feedback."})
process['stakeholders'].append({"stakeholder": "Employers / Industry", "role": "Potential employers of graduates; partners in curriculum development and internships; benefit from research", "responsibilities": "(INFERRED) Employing graduates, providing internships, advising on curriculum relevance, collaborating on research."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Collaborators on research projects and knowledge generation; partners in scientific inquiry", "responsibilities": "(INFERRED) Partnering on research, sharing data, disseminating findings, collaborating on studies."})
process['stakeholders'].append({"stakeholder": "Funding Agencies / Donors", "role": "Provide financial support for research, infrastructure, and student scholarships", "responsibilities": "(INFERRED) Funding projects, supporting educational initiatives, ensuring accountability."})
process['stakeholders'].append({"stakeholder": "Alumni", "role": "Former students who contribute to the university's reputation and often provide support and mentorship", "responsibilities": "(INFERRED) Mentoring current students, donating to the university, promoting the institution."})
process['stakeholders'].append({"stakeholder": "Other Universities / Colleges", "role": "Collaborators on academic programs, research, and staff exchange; engage in benchmarking", "responsibilities": "(INFERRED) Partnering on joint programs, sharing best practices, fostering academic collaboration."})

process['as_is_narrative'] = "(INFERRED) Chuka University actively fulfills its mandate by developing and delivering a diverse range of academic programs across its various schools, including Pure and Applied Sciences, Agriculture and Environmental Studies, Business and Economics, Education, and Arts and Social Sciences. The university is committed to providing quality education that integrates theoretical knowledge with practical skills, offering students access to well-equipped laboratories, library resources, and field-based learning opportunities. A significant focus is placed on scientific research, which generates new knowledge, addresses societal challenges, and contributes to innovation, particularly in areas relevant to food security, environmental sustainability, and regional development. Chuka University engages in robust community outreach and extension services, disseminating knowledge and providing solutions to local communities, for instance, through agricultural extension, public health campaigns, and entrepreneurial support. The university maintains a strong internal quality assurance system and undergoes regular evaluations by the Commission for University Education (CUE) to ensure continuous improvement of its academic programs and service delivery. It fosters a culture of innovation and entrepreneurship among its students, often through dedicated incubation centers and business support services. Furthermore, Chuka University actively establishes collaborations with national and international partners, including other academic institutions, industries, government agencies, and research organizations, for academic exchange, joint research projects, and funding opportunities, thereby playing a pivotal role in the human capital development and socio-economic transformation of its region and Kenya as a whole."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.chuka.ac.ke/" # Official website
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and seventh process enriched and combined_data.json updated.")
