
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninety-fourth process (index 93)
process = data['processes'][93]

# Populate fields
process['executive_summary'] = "The Ministry of Education in Kenya, through its Basic Education functions, operates under a comprehensive mandate primarily enshrined in the Constitution of Kenya. It is responsible for ensuring the provision of quality basic education, encompassing Early Childhood, Primary, and Secondary education. This involves developing education policies, standards, and curriculum, and managing institutions. The Ministry aims to guarantee children's rights to free and compulsory education, promote ICT integration in learning, and foster a robust educational system that aligns with national development goals and produces skilled citizens."
process['process_overview']['process_objective'] = "To formulate and implement policies, strategies, and programs for Early Childhood Development, Primary, and Secondary education, and for teacher training; to supervise the management of Basic Education Service Provision Institutions; to establish and maintain a comprehensive Education Information Management System (database) for basic education; to facilitate the development of basic education and teacher training across all levels; to initiate and implement strategic international, national, and institutional collaborations and partnerships for interventions in Basic Education; to ensure the implementation of nomadic education and alternative provision to basic education policies; to ensure prudent management of finances and other resources in Basic Education Institutions; to ensure the registration of all schools and colleges; to manage national examinations and certification processes; and to manage teacher and student affairs, including quality assurance in education and curriculum development."
process['process_overview']['policy_legal_context'].append("The Ministry's mandate is primarily enshrined in the Constitution of Kenya, Chapter Four, particularly Articles 43, 53, 54, 55, 56, 57, and 59, guaranteeing children's rights to free and compulsory education, access to quality services, and educational institutions, including provisions for persons with disabilities. The Ministry operates under the Basic Education Act 2013 and other relevant education acts. Its functions are distributed between national and county governments as stipulated in the Constitution of Kenya Articles 185(2), 186(1), and 187(2).")
process['stakeholders'].append({"stakeholder": "Students (Early Childhood, Primary, Secondary)", "role": "Primary beneficiaries of the basic education system; their learning and development is the core focus", "responsibilities": "(INFERRED) Attending school, engaging in learning, adhering to school rules."})
process['stakeholders'].append({"stakeholder": "Teachers", "role": "Deliver the curriculum and mentor students; crucial for educational quality", "responsibilities": "(INFERRED) Teaching, guiding students, professional development, adhering to teaching standards."})
process['stakeholders'].append({"stakeholder": "Parents / Guardians", "role": "Key partners in children's education and well-being; responsible for ensuring school attendance and support", "responsibilities": "(INFERRED) Supporting learning, ensuring school attendance, engaging with schools, providing feedback."})
process['stakeholders'].append({"stakeholder": "Boards of Management (BOMs) / School Management Committees (SMCs)", "role": "Oversee the day-to-day management of individual schools", "responsibilities": "(INFERRED) Managing school resources, implementing school policies, ensuring quality education."})
process['stakeholders'].append({"stakeholder": "Kenya Institute of Curriculum Development (KICD)", "role": "Develops and reviews the national curriculum for basic education", "responsibilities": "(INFERRED) Developing relevant curricula, providing educational materials, advising on curriculum implementation."})
process['stakeholders'].append({"stakeholder": "Teachers Service Commission (TSC)", "role": "Manages the recruitment, registration, deployment, promotion, and discipline of teachers in public schools", "responsibilities": "(INFERRED) Managing teacher workforce, ensuring teacher welfare, maintaining teaching standards."})
process['stakeholders'].append({"stakeholder": "Kenya National Examinations Council (KNEC)", "role": "Administers national examinations and certifies academic achievements", "responsibilities": "(INFERRED) Setting examination standards, conducting examinations fairly, issuing certificates."})
process['stakeholders'].append({"stakeholder": "County Education Boards", "role": "Coordinate and oversee education matters at the county level, ensuring quality education delivery", "responsibilities": "(INFERRED) Implementing education policies locally, monitoring schools, coordinating with stakeholders."})
process['stakeholders'].append({"stakeholder": "County Governments (for pre-primary education)", "role": "Responsible for pre-primary education and some vocational training centers", "responsibilities": "(INFERRED) Funding pre-primary education, managing vocational training, supporting local education."})
process['stakeholders'].append({"stakeholder": "Educational Publishers", "role": "Develop and supply textbooks and other learning materials aligned with the curriculum", "responsibilities": "(INFERRED) Publishing quality educational materials, ensuring affordability and accessibility."})
process['stakeholders'].append({"stakeholder": "Private School Owners", "role": "Provide education services alongside public schools; regulated by the Ministry", "responsibilities": "(INFERRED) Providing education, complying with Ministry regulations, offering alternative educational choices."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support educational programs and reforms", "responsibilities": "(INFERRED) Funding educational projects, sharing expertise, supporting capacity building."})
process['stakeholders'].append({"stakeholder": "Religious Organizations (sponsoring schools)", "role": "Sponsor a significant number of basic education institutions", "responsibilities": "(INFERRED) Managing sponsored schools, promoting moral values, contributing to educational development."})

process['as_is_narrative'] = "(INFERRED) The Ministry of Education, through its Directorate of Basic Education, implements its mandate through a multi-layered approach to govern and manage the entire basic education sub-sector. This involves the continuous formulation and review of national education policies and legal frameworks to ensure they are responsive to societal needs and national development goals. In collaboration with the Kenya Institute of Curriculum Development (KICD), the Ministry oversees the development and implementation of curricula for Early Childhood Development, Primary, and Secondary education, including the competency-based curriculum (CBC). It registers and regulates all basic education and training institutions (both public and private) to ensure adherence to prescribed quality standards. The Ministry manages national examinations and certification processes through the Kenya National Examinations Council (KNEC), ensuring integrity and fairness. Teacher management, including recruitment, deployment, promotion, and discipline, is handled by the Teachers Service Commission (TSC), working closely with the Ministry to ensure adequate staffing and quality instruction. The Ministry oversees the allocation and utilization of financial resources, such as Free Primary Education (FPE) funds and capitation grants, to schools. It also implements special programs like nomadic education and alternative provision to basic education to ensure inclusivity. An extensive Education Information Management System (EMIS) is maintained to collect, analyze, and disseminate education data for informed decision-making. Furthermore, the Ministry fosters international and local partnerships for educational development and champions the integration of Information and Communication Technology (ICT) in teaching and learning to enhance access and quality across the basic education sector."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://teacher.co.ke/", # Provided context
    "https://devolution.go.ke/", # Provided context
    "https://sheriaplex.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninety-fourth process enriched and combined_data.json updated.")
