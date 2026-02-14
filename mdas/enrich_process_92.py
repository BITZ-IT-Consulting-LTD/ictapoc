
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninety-third process (index 92)
process = data['processes'][92]

# Populate fields
process['executive_summary'] = "The Bandari Maritime Academy (BMA) in Kenya is a semi-autonomous government agency, established under a Presidential Order in November 2018. Its primary mandate is to develop academic and vocational skills and provide the maritime human resource necessary for the sustainable growth of the Blue Economy. BMA aims to be a world-class center for maritime education and training, offering excellence in teaching, training, scholarship, innovation, and research in maritime skills, thereby delivering the human capital needed to advance Kenya's maritime objectives and regional development."
process['process_overview']['process_objective'] = "To be an institution of excellence in teaching, training, scholarship, innovation, and research in maritime skills; to provide and advance education and training to qualified candidates, leading to the award of diplomas, certificates, and other qualifications as prescribed by the Board; to conduct examinations for academic awards; to implement government policy on maritime education and training; to ensure the highest international maritime standards in maritime human resource development; to recommend and advise the Government on relevant legislation to facilitate the successful implementation of maritime education and training; to serve as the Regional Maritime Centre of Excellence for training in ports, terminals, logistics, and maritime transport skills; to establish centers of excellence in maritime education and training based on international maritime standards; to partner with other institutions to further maritime education and training; and to serve as a national center for motion simulator training for seagoing competencies."
process['process_overview']['policy_legal_context'].append("Established under a Presidential Order of November 19, 2018, and published under Gazette Notice No. 233 dated November 28, 2018, which provides the legal and institutional framework for its operations. BMA operates under the Ministry of Transport (or the relevant government ministry responsible for maritime affairs) and its mandate is specified under clause 4(1) of this Presidential Order. It aligns its mission with the sustainable growth of the Blue Economy, Kenya's national development agenda (e.g., Vision 2030), and international maritime conventions and standards.")
process['stakeholders'].append({"stakeholder": "Students / Trainees (aspiring seafarers, maritime professionals)", "role": "Primary beneficiaries of BMA's education and training programs; future maritime workforce", "responsibilities": "(INFERRED) Engaging in training, adhering to maritime standards, pursuing maritime careers."})
process['stakeholders'].append({"stakeholder": "Kenya Ports Authority (KPA)", "role": "State corporation managing ports; collaborates on port-related training and employment opportunities", "responsibilities": "(INFERRED) Partnering on training programs, offering attachment opportunities, employing BMA graduates."})
process['stakeholders'].append({"stakeholder": "Kenya Maritime Authority (KMA)", "role": "Regulatory body for maritime sector; collaborates on standards, certification, and compliance", "responsibilities": "(INFERRED) Regulating maritime training, certifying seafarers, ensuring compliance with international conventions."})
process['stakeholders'].append({"stakeholder": "Ministry of Transport", "role": "Parent Ministry providing policy direction, funding, and oversight to BMA", "responsibilities": "(INFERRED) Formulating maritime policies, allocating resources, strategic guidance for the maritime sector."})
process['stakeholders'].append({"stakeholder": "Shipping Companies / Employers (Local and International)", "role": "Employers of BMA graduates; collaborate on curriculum development and provide practical experience", "responsibilities": "(INFERRED) Employing BMA graduates, providing sea-time opportunities, advising on industry needs."})
process['stakeholders'].append({"stakeholder": "International Maritime Organization (IMO)", "role": "Global regulatory body setting international standards for maritime safety, security, and pollution prevention; BMA adheres to IMO conventions (e.g., STCW)", "responsibilities": "(INFERRED) Setting international maritime standards, monitoring compliance, providing guidance."})
process['stakeholders'].append({"stakeholder": "Kenya Navy", "role": "Security force in Kenya's maritime domain; potential beneficiary of specialized training", "responsibilities": "(INFERRED) Collaborating on maritime security training, utilizing BMA facilities."})
process['stakeholders'].append({"stakeholder": "Kenya Coast Guard Service", "role": "Enforces maritime laws and ensures security in Kenya's territorial waters; potential beneficiary of specialized training", "responsibilities": "(INFERRED) Collaborating on maritime law enforcement training, utilizing BMA facilities."})
process['stakeholders'].append({"stakeholder": "Other Maritime Training Institutions", "role": "Collaborators on academic programs, research, and staff exchange", "responsibilities": "(INFERRED) Partnering on joint programs, sharing best practices, fostering academic collaboration."})
process['stakeholders'].append({"stakeholder": "Local Communities (Mombasa)", "role": "Beneficiaries of employment opportunities and socio-economic development fostered by BMA", "responsibilities": "(INFERRED) Supplying labor, benefiting from economic activities, engaging with BMA."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support BMA's programs and infrastructure development", "responsibilities": "(INFERRED) Funding maritime training initiatives, sharing expertise in maritime education."})

process['as_is_narrative'] = "(INFERRED) The Bandari Maritime Academy (BMA) actively fulfills its mandate by designing and delivering a comprehensive portfolio of academic and vocational courses, including diplomas, certificates, and specialized short courses, across key maritime disciplines such as nautical science, marine engineering, maritime transport operations, port logistics, and specialized port equipment operation. BMA utilizes state-of-the-art training facilities and equipment, notably including advanced motion simulators, to provide practical, hands-on experience that meets and exceeds the stringent requirements of international maritime standards, particularly those set by the International Convention on Standards of Training, Certification and Watchkeeping for Seafarers (STCW). The Academy conducts continuous assessments and examinations, leading to internationally recognized academic awards and certifications. BMA collaborates extensively with industry stakeholders, including shipping companies, port operators, and the Kenya Ports Authority, to ensure its curriculum remains relevant to industry needs and to facilitate opportunities for sea-time attachments and post-graduation employment for its trainees. It actively implements government policies related to maritime education and the broader Blue Economy agenda, undertaking applied research and innovation in maritime skills development. Furthermore, BMA engages in strategic national and regional partnerships, reinforcing its role as a designated Centre of Excellence in maritime education and training, contributing significantly to the development of a skilled maritime workforce for Kenya and the East African region."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.bma.ac.ke/", # Official website
    "https://scribd.com/", # Provided context
    "https://thecoast.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninety-third process enriched and combined_data.json updated.")
