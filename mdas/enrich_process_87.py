
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighty-eighth process (index 87)
process = data['processes'][87]

# Populate fields
process['executive_summary'] = "Alupe University, formerly Alupe University College, is a Kenyan institution of higher learning with a comprehensive mandate focused on education, research, and community outreach. It provides high-quality undergraduate, postgraduate, and professional programs across various fields, conducts research that addresses societal challenges and promotes innovation, and actively engages with local communities to foster socio-economic development. Alupe University contributes significantly to national development agendas like Kenya Vision 2030 and the Bottom-Up Economic Transformation Agenda (BETA) by producing skilled human capital and generating knowledge for sustainable growth."
process['process_overview']['process_objective'] = "To provide high-quality undergraduate, postgraduate, and professional programs across various fields, including health sciences, science, education, social sciences, and business; to conduct research that addresses societal challenges, promotes innovation, and contributes to sustainable development through the discovery, transmission, preservation, and enhancement of knowledge; to actively engage with local communities to foster socio-economic development through education, outreach programs, and research initiatives; to ensure the continuous improvement of academic programs and uphold high standards of teaching, learning, and research; to enhance skills and knowledge among its students and the broader community through capacity building initiatives; to foster entrepreneurship and innovation among students to stimulate job creation and economic growth; to establish partnerships with national and international institutions, businesses, and organizations to enhance research and academic exchange; to contribute to national and international policy development and advocacy in education, development, and research; to promote sustainability and environmental stewardship through research, education, and community projects focused on environmental conservation; and to develop leadership skills in students, preparing them for effective roles in society and the workforce."
process['process_overview']['policy_legal_context'].append("Alupe University operates as a public university under relevant Kenyan university acts and higher education regulations, including the Universities Act, No. 42 of 2012. It is governed by its charter and university council. The university aligns its mandates with national development agendas, including Kenya Vision 2030 and the Bottom-Up Economic Transformation Agenda (BETA), focusing on human capital development, research-driven solutions, and community service to address the unique needs of its region and the country.")
process['stakeholders'].append({"stakeholder": "Students (Undergraduate, Postgraduate)", "role": "Primary beneficiaries of the university's education and training programs", "responsibilities": "(INFERRED) Engaging in academic pursuits, participating in research, contributing to university life."})
process['stakeholders'].append({"stakeholder": "Faculty / Academic Staff", "role": "Deliver education, conduct research, and engage in community service", "responsibilities": "(INFERRED) Teaching, mentoring students, conducting research, publishing scholarly work."})
process['stakeholders'].append({"stakeholder": "Non-Teaching Staff", "role": "Provide administrative and support services essential for the university's operations", "responsibilities": "(INFERRED) Supporting academic programs, maintaining facilities, managing university resources."})
process['stakeholders'].append({"stakeholder": "Local Communities (Busia County and Western Kenya region)", "role": "Beneficiaries of community outreach programs, research findings, and employment opportunities", "responsibilities": "(INFERRED) Collaborating on community projects, utilizing university resources, providing feedback."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (Ministry of Education, Ministry of Health, Ministry of Agriculture, etc.)", "role": "Provides policy direction, funding, and oversight; benefits from skilled graduates and research output", "responsibilities": "(INFERRED) Formulating education policies, allocating resources, utilizing research findings."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Collaborators on research projects and knowledge generation", "responsibilities": "(INFERRED) Partnering on research, sharing data, disseminating findings."})
process['stakeholders'].append({"stakeholder": "Industry / Employers", "role": "Potential employers of graduates; partners in curriculum development and internships", "responsibilities": "(INFERRED) Employing graduates, providing internships, advising on curriculum relevance."})
process['stakeholders'].append({"stakeholder": "Alumni", "role": "Former students who contribute to the university's reputation and often provide support", "responsibilities": "(INFERRED) Mentoring current students, donating to the university, promoting the institution."})
process['stakeholders'].append({"stakeholder": "Funding Agencies / Donors", "role": "Provide financial support for research, infrastructure, and student scholarships", "responsibilities": "(INFERRED) Funding projects, supporting educational initiatives, ensuring accountability."})
process['stakeholders'].append({"stakeholder": "Other Universities / Colleges", "role": "Collaborators on academic programs, research, and staff exchange", "responsibilities": "(INFERRED) Partnering on joint programs, sharing best practices, fostering academic collaboration."})
process['stakeholders'].append({"stakeholder": "Regulatory Bodies (e.g., Commission for University Education (CUE))", "role": "Ensure quality assurance and accreditation of university programs and institutions", "responsibilities": "(INFERRED) Setting academic standards, accrediting programs, monitoring compliance."})

process['as_is_narrative'] = "(INFERRED) Alupe University delivers its mandate through a robust framework of academic instruction, research, and community engagement. It develops and continuously reviews undergraduate, postgraduate, and professional curricula in diverse fields such as health sciences, pure and applied sciences, education, social sciences, and business, ensuring relevance to national and global needs. The university employs a dedicated faculty to deliver high-quality teaching and mentorship to its students. A core function involves conducting both basic and applied research across its various departments, with a strong emphasis on generating knowledge and providing innovative solutions to local and national challenges, particularly those pertinent to Western Kenya. Alupe University actively engages in community outreach programs, transferring knowledge and expertise through initiatives like agricultural extension services, public health awareness campaigns, and adult education. The university maintains rigorous internal quality assurance mechanisms and adheres to standards set by the Commission for University Education (CUE). It fosters a vibrant culture of innovation and entrepreneurship, often through dedicated centers that support students in developing viable business ideas. Collaboration is key, with the university forming partnerships with other academic institutions, research bodies, industries, and government agencies to enhance research funding, student internships, and curriculum development, thereby contributing significantly to regional human capital development and socio-economic transformation."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.alupe.ac.ke/", # Official website
    "https://saraka.info/", # Provided context
    "https://parliament.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighty-eighth process enriched and combined_data.json updated.")
