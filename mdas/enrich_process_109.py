
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and tenth process (index 109)
process = data['processes'][109]

# Populate fields
process['executive_summary'] = "The Co-operative University of Kenya (CUK) is a premier public university in Kenya, established with a mission to provide quality education, training, research, and consultancy, particularly in co-operative development, business, and related fields. CUK aims to be a leading institution in cooperative training, education, research, and innovation, nurturing an intellectual culture that combines theoretical understanding with practical application, innovation, and entrepreneurship. Through its specialized focus, CUK contributes significantly to national and global development by strengthening the cooperative movement and producing skilled human capital."
process['process_overview']['process_objective'] = "To provide quality university education, training, research, and consultancy in co-operative development, business, and related fields; to advance learning and knowledge through rigorous research and innovation; to offer comprehensive academic programs across Diploma, Undergraduate, and Postgraduate levels; to support student services including access to student portals, e-learning platforms, and library resources; to facilitate community engagement and outreach programs, empowering communities through specialized consultancy services; to disseminate knowledge for effective leadership in higher education, training, research, and outreach; and to foster an intellectual culture that combines theoretical understanding with practical application, innovation, and entrepreneurship, contributing to sustainable national and global development."
process['process_overview']['policy_legal_context'].append("Established as a public university under the Universities Act, 2012, and other relevant higher education regulations, which provide the legal and regulatory framework for its establishment and functions. CUK operates under the Ministry of Education and is crucial for implementing national development agendas, including Vision 2030, and policies aimed at strengthening the cooperative movement, enhancing financial inclusion, and promoting sustainable development in Kenya. The university is governed by its charter and council.")
process['stakeholders'].append({"stakeholder": "Students (Prospective and Current)", "role": "Primary beneficiaries of CUK's specialized education and training programs", "responsibilities": "(INFERRED) Engaging in academic pursuits, participating in research, contributing to university life, upholding academic integrity."})
process['stakeholders'].append({"stakeholder": "Faculty / Academic Staff", "role": "Deliver education, conduct research, and engage in consultancy and community service", "responsibilities": "(INFERRED) Teaching, mentoring students, conducting research, publishing scholarly work, professional development."})
process['stakeholders'].append({"stakeholder": "Non-Teaching Staff", "role": "Provide administrative and support services essential for the university's operations and student welfare", "responsibilities": "(INFERRED) Supporting academic programs, maintaining facilities, managing university resources, student support services."})
process['stakeholders'].append({"stakeholder": "Co-operative Sector (SACCOs, Cooperative Societies, Unions)", "role": "Key beneficiaries of CUK's research, training, and consultancy; partner in student attachments and employment", "responsibilities": "(INFERRED) Seeking training/consultancy, offering internships, employing graduates, collaborating on research."})
process['stakeholders'].append({"stakeholder": "Ministry of Co-operatives Development", "role": "Government Ministry providing policy direction and oversight for the cooperative sector; collaborates with CUK", "responsibilities": "(INFERRED) Formulating cooperative policies, allocating resources, strategic guidance for the cooperative movement."})
process['stakeholders'].append({"stakeholder": "Ministry of Education", "role": "Parent Ministry providing policy direction, funding, and oversight to universities", "responsibilities": "(INFERRED) Formulating education policies, allocating resources, strategic guidance for higher education."})
process['stakeholders'].append({"stakeholder": "Commission for University Education (CUE)", "role": "Regulatory body for university education in Kenya; ensures quality and accreditation of programs", "responsibilities": "(INFERRED) Setting academic standards, accrediting programs, monitoring compliance, licensing universities."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Collaborators on research projects and knowledge generation, particularly in cooperative development and agribusiness", "responsibilities": "(INFERRED) Partnering on research, sharing data, disseminating findings, collaborating on studies."})
process['stakeholders'].append({"stakeholder": "Industry / Employers", "role": "Potential employers of graduates; partners in curriculum development and internships", "responsibilities": "(INFERRED) Employing graduates, providing internships, advising on curriculum relevance, collaborating on research."})
process['stakeholders'].append({"stakeholder": "Alumni", "role": "Former students who contribute to the university's reputation and often provide support and mentorship", "responsibilities": "(INFERRED) Mentoring current students, donating to the university, promoting the institution."})
process['stakeholders'].append({"stakeholder": "Funding Agencies / Donors", "role": "Provide financial support for research, infrastructure, and student scholarships", "responsibilities": "(INFERRED) Funding projects, supporting educational initiatives, ensuring accountability."})
process['stakeholders'].append({"stakeholder": "Other Universities / Colleges", "role": "Collaborators on academic programs, research, and staff exchange; engage in benchmarking", "responsibilities": "(INFERRED) Partnering on joint programs, sharing best practices, fostering academic collaboration."})

process['as_is_narrative'] = "(INFERRED) The Co-operative University of Kenya (CUK) actively fulfills its specialized mandate by developing and delivering a wide range of academic programs (from diploma to PhD) in areas such as cooperative management, business administration, finance, education, information technology, and agribusiness, with a distinct emphasis on cooperative principles and practices. The university conducts impactful research in cooperative development, agribusiness, entrepreneurship, and sustainable development, generating new knowledge and disseminating findings to inform policy and practice within the cooperative sector and beyond. CUK provides practical and experiential learning opportunities for students through attachments, fieldwork, and industry partnerships, ensuring graduates are well-prepared for the job market. It engages in extensive community outreach and consultancy services, offering expertise to cooperative societies and local enterprises in areas such as governance, financial management, strategic planning, and capacity building. The university continuously evaluates and improves its academic programs and service delivery, adhering to quality assurance standards set by the Commission for University Education (CUE). CUK fosters a culture of innovation and entrepreneurship among its students and staff, encouraging the development of viable business solutions. Furthermore, it establishes collaborations with national and international partners, including other academic institutions, government ministries, and funding agencies, for academic exchange, joint research, and funding opportunities, thereby playing a pivotal role in strengthening the cooperative movement, promoting financial inclusion, and contributing to national economic growth and human capital development in Kenya and the region."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.cuk.ac.ke/", # Official website
    "https://devex.com/", # Provided context
    "https://youtube.com/", # Provided context
    "https://studzona.com/", # Provided context
    "https://unirank.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and tenth process enriched and combined_data.json updated.")
