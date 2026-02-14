
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundredth process (index 99)
process = data['processes'][99]

# Populate fields
process['executive_summary'] = "Bukura Agricultural College is a key agricultural training institution in Kenya, established under the Bukura Agricultural College Act, Cap.348 of 1999. Its mandate is 'To provide Agricultural Training through the integration of Research and Extension'. The College aims to provide quality agricultural education, foster innovation, and conduct relevant research to improve agricultural productivity and livelihoods in Kenya. It plays a vital role in developing skilled human resources for the agricultural sector and contributing to national food security."
process['process_overview']['process_objective'] = "To provide quality agricultural education through comprehensive training, relevant research, practical innovations, and effective extension services; to improve agricultural productivity and livelihoods among farmers and communities; to offer education in agriculture and related subjects at various levels (e.g., diploma, certificate); to engage in the discovery, transmission, and preservation of agricultural knowledge; to conduct examinations and award diplomas and certificates to qualified graduates; and to collaborate with the government and other stakeholders on agricultural education development and policy implementation."
process['process_overview']['policy_legal_context'].append("Established under the Bukura Agricultural College Act, Cap.348 of 1999, which provides the legal framework for its establishment, mandate, and functions. The College operates under the Ministry of Agriculture, Livestock, Fisheries and Cooperatives (or the relevant government ministry responsible for agricultural training and research) and is central to implementing national agricultural development and food security policies through human resource development, skills transfer, and practical research.")
process['stakeholders'].append({"stakeholder": "Students (aspiring agricultural professionals)", "role": "Primary beneficiaries of the college's training programs; future workforce in agriculture", "responsibilities": "(INFERRED) Engaging in learning, participating in practical training, seeking knowledge."})
process['stakeholders'].append({"stakeholder": "Farmers (beneficiaries of extension services and trained personnel)", "role": "Recipients of technical advice, improved practices, and graduates from the college", "responsibilities": "(INFERRED) Adopting improved farming methods, collaborating with extension officers, providing feedback on needs."})
process['stakeholders'].append({"stakeholder": "Agricultural Research Institutions (e.g., KALRO)", "role": "Collaborators in applied research and integration of new technologies into training programs", "responsibilities": "(INFERRED) Partnering on research projects, sharing findings, advising on curriculum content."})
process['stakeholders'].append({"stakeholder": "Ministry of Agriculture, Livestock, Fisheries and Cooperatives", "role": "Parent Ministry providing policy direction, funding, and oversight to the College", "responsibilities": "(INFERRED) Formulating agricultural policies, allocating resources, strategic guidance for agricultural training."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in local agricultural extension services and development programs; potential employers of graduates", "responsibilities": "(INFERRED) Collaborating on agricultural programs, supporting local farmers, providing employment opportunities."})
process['stakeholders'].append({"stakeholder": "Agricultural Sector Development Partners", "role": "Provide financial and technical assistance to support agricultural training and research initiatives", "responsibilities": "(INFERRED) Funding projects, sharing expertise in agricultural education and development."})
process['stakeholders'].append({"stakeholder": "Agricultural Input Suppliers", "role": "Partners in demonstrating new agricultural technologies and products to students and farmers", "responsibilities": "(INFERRED) Collaborating on field trials, supplying inputs for practical training, demonstrating new products."})
process['stakeholders'].append({"stakeholder": "Agro-processing Industries", "role": "Potential employers of graduates; provide insights into market demands and value addition", "responsibilities": "(INFERRED) Employing graduates, advising on curriculum relevance, seeking skilled personnel."})
process['stakeholders'].append({"stakeholder": "Alumni", "role": "Former students who contribute to the college's reputation and often provide support and mentorship", "responsibilities": "(INFERRED) Mentoring current students, supporting college initiatives, networking."})
process['stakeholders'].append({"stakeholder": "Kenya National Examinations Council (KNEC) (for national examinations)", "role": "Administers national examinations for diploma and certificate courses offered by the college", "responsibilities": "(INFERRED) Setting examination standards, conducting examinations fairly, certifying graduates."})

process['as_is_narrative'] = "(INFERRED) Bukura Agricultural College actively fulfills its mandate by developing and delivering demand-driven curricula for diploma and certificate courses in a wide array of agricultural disciplines, including general agriculture, animal health, agricultural education, and agribusiness management. The college provides practical, hands-on training to its students through extensive farm-based activities, modern demonstration units (e.g., dairy units, horticulture blocks), and well-equipped laboratory facilities, ensuring graduates are competent and industry-ready. A core function involves conducting applied research relevant to local agricultural challenges, focusing on adaptive technologies and improved farming practices, and disseminating these findings to farmers through its integrated extension services and outreach programs. The college continuously reviews and updates its academic programs to align with national agricultural policies, the competency-based curriculum framework, and emerging industry needs. It collaborates closely with agricultural research organizations like KALRO to integrate new technologies and knowledge into its training and extension activities. Bukura Agricultural College partners with local communities and farmers through outreach initiatives, field days, and advisory services to demonstrate improved farming techniques, promote sustainable agriculture, and provide technical advice. It conducts examinations and certifies its graduates, who are equipped with the necessary skills and knowledge to contribute effectively to increased agricultural productivity, food security, and improved livelihoods in Kenya. The college actively participates in national agricultural development initiatives and contributes to policy discussions related to agricultural education and extension."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.bukuracollege.ac.ke/", # Official website
    "https://policyvault.africa/" # Provided context (Bukura Agricultural College Act)
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundredth process enriched and combined_data.json updated.")
