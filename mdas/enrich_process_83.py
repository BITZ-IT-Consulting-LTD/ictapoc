
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighty-fourth process (index 83)
process = data['processes'][83]

# Populate fields
process['executive_summary'] = "Agri and Cooperative Training and Consultancy Services Limited (ATC) is a capacity development and consultancy services provider wholly owned by the Co-operative University of Kenya (CUK). Its primary mandate is to extend the academic knowledge and expertise of CUK to various groups within and outside the co-operative movement and the agricultural sector. ATC offers specialized training, consultancy, and research services aimed at enhancing businesses and improving interventions in agribusiness and rural development. Operating on a commercial and cost-recovery basis, ATC delivers competitive and cost-effective solutions aligned with Kenya's national development needs."
process['process_overview']['process_objective'] = "To extend academic knowledge in agribusiness, co-operative rural development, and related economic sectors to various stakeholders; to enhance businesses by offering comprehensive capacity development, training, consultancy, and research services; to offer quality and specialized short courses for farmers, small-scale entrepreneurs, co-operative societies (including SACCOs), and other relevant stakeholders; to provide training in diverse fields such as agriculture, ICT, monitoring and evaluation, project management, food security, leadership, climate change, and GIS & remote sensing; to conduct consultancies focused on improving interventions and providing business solutions in agriculture and rural development, aligning with national goals like Kenya Vision 2030 and the Agricultural Sector Development Strategy; and to collaborate with clients and provide scientific research findings to aid in informed decision-making within the sector."
process['process_overview']['policy_legal_context'].append("ATC is wholly owned by the Co-operative University of Kenya (CUK), operating as its commercial arm for training and consultancy. Its services are aligned with national development goals such as Kenya Vision 2030, the Agricultural Sector Development Strategy, and policies aimed at enhancing food security and economic empowerment through cooperative development. ATC operates on a commercial and cost-recovery basis, enjoying institutional autonomy to deliver competitive and cost-effective services within its specialized fields.")
process['stakeholders'].append({"stakeholder": "Farmers", "role": "Recipients of specialized training and consultancy to improve agricultural practices and yields", "responsibilities": "(INFERRED) Adopting improved farming methods, participating in training, utilizing consultancy advice."})
process['stakeholders'].append({"stakeholder": "Small-scale Entrepreneurs", "role": "Beneficiaries of training and business development services in agribusiness and related sectors", "responsibilities": "(INFERRED) Developing business skills, seeking market linkages, improving enterprise management."})
process['stakeholders'].append({"stakeholder": "Co-operative Societies (SACCOs, producer co-ops)", "role": "Clients for training and consultancy services in governance, management, and financial operations", "responsibilities": "(INFERRED) Seeking capacity building, improving member services, strengthening cooperative governance."})
process['stakeholders'].append({"stakeholder": "Co-operative University of Kenya (CUK) (parent institution)", "role": "Owner of ATC; provides academic backing and expertise for training and consultancy", "responsibilities": "(INFERRED) Providing academic oversight, leveraging faculty expertise, ensuring quality standards."})
process['stakeholders'].append({"stakeholder": "Government Ministries (e.g., Agriculture, Co-operatives)", "role": "Collaborators on national development initiatives in agriculture and co-operatives; clients for training/consultancy", "responsibilities": "(INFERRED) Formulating policies, seeking technical advice, supporting sector development."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in implementing local agricultural and cooperative development programs", "responsibilities": "(INFERRED) Supporting local farmers/co-ops, seeking technical assistance, collaborating on projects."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support capacity building in agriculture and co-operatives", "responsibilities": "(INFERRED) Funding training programs, sharing expertise in rural development."})
process['stakeholders'].append({"stakeholder": "NGOs in Agriculture / Rural Development", "role": "Collaborators in implementing grassroots development initiatives", "responsibilities": "(INFERRED) Partnering on projects, seeking training for beneficiaries, advocating for rural communities."})
process['stakeholders'].append({"stakeholder": "Financial Institutions (serving co-ops)", "role": "Provide financial services to co-operative societies; may seek training for their clients", "responsibilities": "(INFERRED) Offering financial products, collaborating on financial literacy programs."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Collaborators in conducting scientific research in agriculture and co-operatives", "responsibilities": "(INFERRED) Sharing research findings, collaborating on studies, advising on best practices."})
process['stakeholders'].append({"stakeholder": "Students / Trainees", "role": "Individuals attending ATC's training programs and courses", "responsibilities": "(INFERRED) Engaging in learning, applying acquired knowledge, seeking professional development."})

process['as_is_narrative'] = "(INFERRED) Agri and Cooperative Training and Consultancy Services Limited (ATC) functions as a dynamic interface between academic knowledge and practical application in the agricultural and cooperative sectors. It actively designs and delivers customized training programs, ranging from short courses to specialized workshops, covering topics such as agribusiness management, financial literacy for SACCOs, project planning and management, climate-smart agriculture, and leadership skills. These programs target diverse groups, including individual farmers, small-scale entrepreneurs, and officials from cooperative societies. ATC undertakes various consultancy assignments, which include conducting feasibility studies for agricultural projects, market research for cooperative products, strategic planning for co-operative societies, and developing capacity-building frameworks for rural development initiatives. It collaborates closely with its parent institution, the Co-operative University of Kenya, leveraging faculty expertise and research capabilities to provide evidence-based solutions. ATC also conducts applied research to generate scientific findings that inform decision-making for its clients and contribute to policy development in the sector. Operating on a commercial basis, ATC seeks to offer competitive and cost-effective services, aiming for financial sustainability while contributing to the growth of the agricultural and cooperative sectors, thereby aligning with national priorities for food security and economic empowerment."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.atc.co.ke/", # Official website
    "https://parliament.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighty-fourth process enriched and combined_data.json updated.")
