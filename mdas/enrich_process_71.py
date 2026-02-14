
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventy-second process (index 71)
process = data['processes'][71]

# Populate fields
process['executive_summary'] = "The National Employment Authority (NEA) in Kenya is a state agency established in 2016 by the National Employment Authority Act, 2016, and became operational in May 2019. It provides a comprehensive institutional framework for employment management, with a primary mandate to regulate and promote employment services, skills development, and labor market information. NEA focuses on facilitating job placement for individuals, both locally and internationally, and particularly for youth, minorities, and marginalized groups, thereby contributing to national economic growth and poverty reduction."
process['process_overview']['process_objective'] = "To register individuals seeking employment and facilitate their placement in various forms of employment; to maintain an integrated and up-to-date database of all job seekers; to enhance employment promotion interventions and increase access to employment for youth, minorities, and marginalized groups; to circulate job vacancies to job seekers through multiple channels; to require employers to comply with the National Employment Authority Act, including filing annual returns, notifying vacancies, and reporting employee terminations and internship opportunities; to protect the unemployed against any form of abuse or exploitation; to facilitate the implementation of national policies on employment and advise the Cabinet Secretary on employment-related matters; to undertake due diligence, facilitate training, and provide counseling related to employment; and to take steps to encourage equal opportunity employment practices across the country."
process['process_overview']['policy_legal_context'].append("Established by the National Employment Authority Act, 2016 (Act No. 3 of 2016), which came into operation in May 2019, providing the legal and institutional framework for its operations. NEA operates under the Ministry of Labour and Social Protection (or the relevant government ministry responsible for labour affairs) and is crucial for implementing national labour policies, ensuring fair employment practices, and addressing unemployment challenges in Kenya.")
process['stakeholders'].append({"stakeholder": "Job Seekers (Unemployed, Youth, Graduates, Minorities, Marginalized Groups)", "role": "Primary beneficiaries of NEA's services for registration, placement, and protection", "responsibilities": "(INFERRED) Registering with NEA, actively seeking employment, participating in training programs, adhering to employment terms."})
process['stakeholders'].append({"stakeholder": "Employers (Public and Private Sector)", "role": "Partners in job creation and placement; required to comply with NEA Act provisions", "responsibilities": "(INFERRED) Notifying NEA of vacancies, filing annual returns, complying with employment laws, providing internship opportunities."})
process['stakeholders'].append({"stakeholder": "Training Institutions (TVETs, Universities, Colleges)", "role": "Provide skills development and vocational training; collaborate with NEA to match skills with labor market needs", "responsibilities": "(INFERRED) Developing market-relevant curricula, providing quality training, collaborating on skills audits."})
process['stakeholders'].append({"stakeholder": "Government Ministries and Departments (e.g., Labour, Education, Youth Affairs)", "role": "Collaborators in policy formulation, resource allocation, and program implementation for employment", "responsibilities": "(INFERRED) Aligning policies, providing sector-specific support, coordinating initiatives."})
process['stakeholders'].append({"stakeholder": "Recruitment Agencies", "role": "Intermediaries in the labor market; registered and regulated by NEA", "responsibilities": "(INFERRED) Complying with NEA regulations, ethical recruitment, facilitating local and international placements."})
process['stakeholders'].append({"stakeholder": "Labor Unions", "role": "Represent workers' interests; engage with NEA on labor market issues and worker protection", "responsibilities": "(INFERRED) Advocating for fair labor practices, collaborating on employment standards."})
process['stakeholders'].append({"stakeholder": "International Organizations (e.g., ILO)", "role": "Provide technical assistance, funding, and international best practices in employment management", "responsibilities": "(INFERRED) Supporting national employment programs, sharing global labor market insights."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support employment initiatives and capacity building", "responsibilities": "(INFERRED) Funding employment projects, sharing expertise."})

process['as_is_narrative'] = "(INFERRED) The National Employment Authority operates through a multi-faceted approach to address employment challenges in Kenya. A core function involves maintaining and operating the National Employment Authority Integrated Management System (NEAMIS) portal, where job seekers register their profiles, skills, and qualifications, and employers post vacancies. NEA actively gathers, analyzes, and disseminates comprehensive labor market information, including skills gaps and industry trends, to inform policy development and guide job seekers and training institutions. It ensures employer compliance with the NEA Act by mandating the filing of annual returns, notification of vacancies, new hires, terminations, and internship opportunities. The Authority conducts skills assessments, provides career counseling, and facilitates various training programs to enhance employability. NEA also promotes fair labor practices, investigates complaints of exploitation, and takes steps to protect vulnerable job seekers. Furthermore, it plays a key role in facilitating safe and regulated overseas employment opportunities for Kenyans and continually advises the Cabinet Secretary on employment policies and strategies to foster a dynamic, inclusive, and responsive labor market that contributes to sustainable economic development."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from reliable sources including official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.labourmarket.go.ke/", # Official website identified in search results
    "https://mman.co.ke/", # Provided context
    "https://cmadvocates.com/", # Provided context
    "https://ey.com/", # Provided context
    "https://chebetlaw.africa/", # Provided context
    "https://nairobileo.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventy-second process enriched and combined_data.json updated.")
