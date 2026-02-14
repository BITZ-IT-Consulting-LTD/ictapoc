
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eightieth process (index 79)
process = data['processes'][79]

# Populate fields
process['executive_summary'] = "The National Youth Service (NYS) is a semi-autonomous state corporation in Kenya, established in 1964 and transformed in 2019 following the enactment of the NYS Act, 2018. Its core mandate is to instill discipline, patriotism, and practical skills in Kenyan youth through rigorous paramilitary training, engagement in national service projects, and provision of Technical and Vocational Education and Training (TVET). NYS aims to develop a disciplined, skilled, and organized human resource pool to support national development programs, foster social cohesion, and enhance youth employability and self-reliance, while also contributing to national security and disaster response."
process['process_overview']['process_objective'] = "To train and mentor Kenyan youth, imparting paramilitary and vocational skills (including construction, engineering, hospitality, agriculture, textiles, and security) to enhance their employability, discipline, patriotism, and self-reliance; to engage youth in community service and public projects, such as infrastructure development (roads, housing), environmental conservation (reforestation, waste management), slum upgrading programs, traffic control, and agriculture; to provide rapid deployment for emergency relief and disaster management, and offer support to security agencies during national emergencies; to foster national unity, civic pride, leadership skills, and promote cross-cultural integration among youth; and to undertake viable commercial enterprises to generate revenue and ensure the sustainability of its operations and programs."
process['process_overview']['policy_legal_context'].append("Established in 1964, the National Youth Service was transformed into a semi-autonomous state corporation in 2019 following the enactment of the NYS Act, 2018, which provides the legal and institutional framework for its operations. NYS operates under the Ministry of Public Service, Youth and Gender Affairs (or the relevant government ministry responsible for youth affairs) and is central to implementing national youth empowerment and development policies, strategies for human resource development, and initiatives aimed at fostering national cohesion and security.")
process['stakeholders'].append({"stakeholder": "Kenyan Youth (aged 18-22/24)", "role": "Primary beneficiaries of NYS training, skills development, and national service programs", "responsibilities": "(INFERRED) Enrolling in NYS, participating in training and national service, adhering to discipline."})
process['stakeholders'].append({"stakeholder": "Government Ministries, Departments, and Agencies (beneficiaries of NYS services/labor)", "role": "Recipients of NYS services in public works, disaster response, and security support", "responsibilities": "(INFERRED) Collaborating on development projects, utilizing NYS resources, providing project oversight."})
process['stakeholders'].append({"stakeholder": "Local Communities (beneficiaries of NYS projects)", "role": "Direct beneficiaries of community service programs, infrastructure development, and disaster relief", "responsibilities": "(INFERRED) Participating in community projects, collaborating with NYS personnel, supporting national development efforts."})
process['stakeholders'].append({"stakeholder": "Employers (private and public sector)", "role": "Potential employers of NYS graduates; recognize NYS training for discipline and skills", "responsibilities": "(INFERRED) Employing NYS graduates, recognizing NYS training, collaborating on skills development."})
process['stakeholders'].append({"stakeholder": "Technical and Vocational Education and Training (TVET) Institutions", "role": "Partners in providing vocational training and certification for NYS servicemen and women", "responsibilities": "(INFERRED) Collaborating on curriculum development, providing specialized training, certifying skills."})
process['stakeholders'].append({"stakeholder": "Security Agencies (Kenya Defence Forces, National Police Service)", "role": "Collaborate with NYS on paramilitary training, security operations, and national emergencies", "responsibilities": "(INFERRED) Providing training expertise, collaborating on security missions, assisting in national emergencies."})
process['stakeholders'].append({"stakeholder": "Humanitarian Organizations (for disaster response)", "role": "Partners in emergency relief and disaster management efforts", "responsibilities": "(INFERRED) Collaborating on disaster response, providing humanitarian aid, coordinating efforts."})
process['stakeholders'].append({"stakeholder": "National Treasury", "role": "Provides funding and financial oversight for NYS operations and projects", "responsibilities": "(INFERRED) Allocating budgetary resources, ensuring financial accountability."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support NYS programs and capacity building", "responsibilities": "(INFERRED) Funding youth development initiatives, sharing expertise in youth empowerment."})

process['as_is_narrative'] = "(INFERRED) The National Youth Service (NYS) actively recruits young Kenyans, typically aged between 18 and 24, who undergo a rigorous multi-phase training program. This begins with a foundational paramilitary training component designed to instill discipline, patriotism, and physical fitness. Following this, the servicemen and women receive technical and vocational training (TVET) in various trades such as construction, engineering, hospitality, agriculture, and security at NYS training colleges, equipping them with practical and marketable skills. A core aspect of NYS operations involves deploying these trained youth to participate in national development projects across the country, which include the construction and rehabilitation of roads, dams, and public facilities, large-scale agricultural projects, environmental conservation initiatives like reforestation and waste management, and urban renewal programs such as slum upgrading. NYS also serves as a rapid response unit, providing crucial support during national emergencies, disasters (e.g., floods, droughts), and assists other security agencies in maintaining public security. To foster self-reliance and sustainability, NYS runs various income-generating commercial ventures in sectors like farming, construction, and garment manufacturing, which also provide practical skills application for the recruits. These comprehensive activities aim to transform Kenyan youth into disciplined, skilled, and patriotic citizens ready to contribute to national progress and secure gainful employment."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.nys.go.ke/", # Official website
    "https://ecitizen.go.ke/", # Provided context
    "https://scribd.com/", # Provided context
    "https://saraka.info/", # Provided context
    "https://lawguide.co.ke/", # Provided context
    "https://youtube.com/", # Provided context
    "https://advance-africa.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eightieth process enriched and combined_data.json updated.")
