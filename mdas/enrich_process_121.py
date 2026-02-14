
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and twenty-second process (index 121)
process = data['processes'][121]

# Populate fields
process['executive_summary'] = "Dedan Kimathi University of Technology (DeKUT) is a premier technological university in Kenya, operating under the motto 'Better Life through Technology'. Its vision is to excel in quality education, research, and technology transfer for national development. DeKUT's mission is to provide an academically stimulating, culturally diverse, and quality learning environment that fosters research, innovation, and technology development, ultimately producing relevant technical and managerial human resources and leaders who significantly contribute to the attainment of national development goals, particularly in industrialization and technological advancement."
process['process_overview']['process_objective'] = "To provide quality education through an academically stimulating, culturally diverse, and quality learning environment; to foster research, innovation, and technology development; to contribute to national development through the transfer of technology; to produce relevant technical and managerial human resources; and to nurture leaders who can contribute to the attainment of national development goals, particularly in areas of science, engineering, and technology."
process['process_overview']['policy_legal_context'].append("Dedan Kimathi University of Technology operates as a public technological university established under the Universities Act, 2012, and governed by its charter and university council. DeKUT operates under the Ministry of Education and aligns its mandates with national development agendas, particularly Kenya Vision 2030, the Science, Technology, and Innovation Act, and policies aimed at industrialization, technological advancement, and human capital development. It plays a crucial role in realizing the country's aspiration to become a newly industrialized nation.")
process['stakeholders'].append({"stakeholder": "Students (Prospective and Current)", "role": "Primary beneficiaries of DeKUT's specialized technological education and training programs; future workforce and innovators", "responsibilities": "(INFERRED) Engaging in academic pursuits, participating in research, contributing to university life, upholding academic integrity."})
process['stakeholders'].append({"stakeholder": "Faculty / Academic Staff", "role": "Deliver education, conduct research, and engage in technology transfer; crucial for academic excellence and innovation", "responsibilities": "(INFERRED) Teaching, mentoring students, conducting research, publishing scholarly work, professional development."})
process['stakeholders'].append({"stakeholder": "Non-Teaching Staff", "role": "Provide administrative and support services essential for the university's operations and student welfare", "responsibilities": "(INFERRED) Supporting academic programs, maintaining facilities, managing university resources, student support services."})
process['stakeholders'].append({"stakeholder": "Commission for University Education (CUE)", "role": "Regulatory body for university education in Kenya; ensures quality and accreditation of programs", "responsibilities": "(INFERRED) Setting academic standards, accrediting programs, monitoring compliance, licensing universities."})
process['stakeholders'].append({"stakeholder": "Ministry of Education", "role": "Parent Ministry providing policy direction, funding, and oversight to universities, especially technological ones", "responsibilities": "(INFERRED) Formulating education policies, allocating resources, strategic guidance for higher education and technology."})
process['stakeholders'].append({"stakeholder": "Industry / Employers", "role": "Potential employers of DeKUT graduates; partners in curriculum development, applied research, and technology commercialization", "responsibilities": "(INFERRED) Employing graduates, providing internships, advising on curriculum relevance, collaborating on research and innovation."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Collaborators on research projects and knowledge generation, particularly in science, engineering, and technology", "responsibilities": "(INFERRED) Partnering on research, sharing data, disseminating findings, collaborating on studies."})
process['stakeholders'].append({"stakeholder": "Funding Agencies / Donors", "role": "Provide financial support for research, infrastructure development, and student scholarships", "responsibilities": "(INFERRED) Funding projects, supporting educational initiatives, ensuring accountability."})
process['stakeholders'].append({"stakeholder": "Alumni", "role": "Former students who contribute to the university's reputation and often provide support and mentorship", "responsibilities": "(INFERRED) Mentoring current students, donating to the university, promoting the institution, acting as industry ambassadors."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Beneficiaries of community outreach programs, technology transfer, and employment opportunities", "responsibilities": "(INFERRED) Collaborating on community projects, utilizing university resources, providing feedback."})
process['stakeholders'].append({"stakeholder": "Other Universities / Colleges", "role": "Collaborators on academic programs, research, and staff exchange; engage in benchmarking", "responsibilities": "(INFERRED) Partnering on joint programs, sharing best practices, fostering academic collaboration."})

process['as_is_narrative'] = "(INFERRED) Dedan Kimathi University of Technology (DeKUT) actively fulfills its mandate by designing and delivering a wide array of specialized academic programs across its various faculties and institutes, with a strong focus on engineering, technology, applied sciences, business, and humanities. The university emphasizes practical and hands-on learning, providing students with access to state-of-the-art laboratories, workshops, and specialized equipment to ensure they acquire relevant technical skills. A core function involves conducting cutting-edge research and development in areas of national and global relevance, such as renewable energy, sustainable agriculture, materials science, and information and communication technology (ICT), often attracting external funding and partnerships. DeKUT fosters a vibrant culture of innovation and entrepreneurship, operating dedicated incubation centers that support students and faculty in developing viable technological solutions and commercializing research outputs. The university plays a crucial role in technology transfer, actively engaging with industries and communities to disseminate developed technologies, provide technical consultancy, and build local capacity. It also engages in various community outreach programs, applying its technical expertise to address local socio-economic challenges. DeKUT continuously evaluates and improves its academic programs and service delivery, adhering to quality assurance standards set by the Commission for University Education (CUE). It establishes strong partnerships with industry players for curriculum development, student internships, and graduate employment, thereby playing a pivotal role in producing a skilled workforce and innovative solutions vital for Kenya's industrialization and technological advancement, in line with its 'Better Life through Technology' motto."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.dkut.ac.ke/" # Official website
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and twenty-second process enriched and combined_data.json updated.")
