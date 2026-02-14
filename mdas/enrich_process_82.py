
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighty-third process (index 82)
process = data['processes'][82]

# Populate fields
process['executive_summary'] = "The Ministry of ASALs and Regional Development (previously known as the Ministry of Devolution and Arid and Semi-Arid Lands - ASALs) is a key government Ministry in Kenya. Established to coordinate the development of policies and programs for the sustainable development of Kenya's Arid and Semi-Arid Lands and regional authorities, it plays a crucial role in fostering economic growth, social inclusion, and environmental sustainability within these regions. The Ministry's work is vital for integrating marginalized areas into the national development agenda and improving livelihoods."
process['process_overview']['process_objective'] = "To coordinate the development of laws, policies, and guidelines for the effective management of devolution and the sustainable development of ASALs; to provide capacity building and technical assistance to counties, particularly those in ASAL regions; to facilitate harmonious intergovernmental relations between national and county governments, and among county governments; to promote public participation in policy and decision-making processes affecting ASALs and regional development; to track and monitor program implementation in counties to ensure alignment with national goals; to coordinate stakeholder engagement for integrated development; to oversee the management of public assets and liabilities at the county level; to facilitate the transfer of functions between national and county governments; to establish and promote systems for efficient and effective implementation of devolution and ASAL programs; to coordinate the implementation of targeted policy interventions for ASALs; to promote socio-economic development in ASALs; to undertake community mobilization for development initiatives; to manage food relief and emergency responses; and to implement special programs for the accelerated development of Northern Kenya and other Arid Lands."
process['process_overview']['policy_legal_context'].append("The Ministry operates under the relevant Executive Orders that establish government Ministries and define their functions (e.g., Executive Order No. 1 of January 2018). Its mandate is to provide leadership in the implementation of devolution and to coordinate the development of ASALs, guided by the Constitution of Kenya 2010, the County Governments Act, and national development strategies such as Vision 2030, particularly those targeting marginalized regions for equitable growth.")
process['stakeholders'].append({"stakeholder": "ASAL Communities", "role": "Primary beneficiaries of the Ministry's programs; their participation is crucial for sustainable development", "responsibilities": "(INFERRED) Engaging in development projects, adopting new technologies, providing local knowledge."})
process['stakeholders'].append({"stakeholder": "County Governments (in ASAL regions)", "role": "Partners in implementing development programs and service delivery at the local level", "responsibilities": "(INFERRED) Collaborating on development plans, allocating resources, implementing national policies locally."})
process['stakeholders'].append({"stakeholder": "National Government (various Ministries and Departments including Agriculture, Water, Education, Health)", "role": "Collaborators in cross-sectoral interventions in ASALs", "responsibilities": "(INFERRED) Integrating ASAL development into sector plans, providing specialized technical support, funding."})
process['stakeholders'].append({"stakeholder": "Regional Development Authorities (e.g., Kerio Valley Development Authority (KVDA), Tana and Athi Rivers Development Authority (TARDA))", "role": "Implement regional development projects; collaborate with the Ministry on specific initiatives", "responsibilities": "(INFERRED) Executing regional projects, coordinating with county governments, contributing to ASAL development."})
process['stakeholders'].append({"stakeholder": "Non-Governmental Organizations (NGOs) working in ASALs", "role": "Partners in service delivery, community mobilization, and advocacy in ASAL regions", "responsibilities": "(INFERRED) Implementing projects, providing humanitarian aid, advocating for ASAL communities."})
process['stakeholders'].append({"stakeholder": "Community-Based Organizations (CBOs)", "role": "Local partners in implementing grassroots development initiatives and community empowerment", "responsibilities": "(INFERRED) Mobilizing communities, managing local projects, providing feedback."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support ASAL development programs", "responsibilities": "(INFERRED) Funding projects, sharing expertise in arid land management and sustainable development."})
process['stakeholders'].append({"stakeholder": "Pastoralists / Farmers in ASALs", "role": "Primary target groups for agricultural and livestock development programs in ASALs", "responsibilities": "(INFERRED) Adopting sustainable land use, participating in livestock management programs."})
process['stakeholders'].append({"stakeholder": "Private Sector (involved in investments in ASALs)", "role": "Partners in economic development, job creation, and sustainable resource exploitation in ASALs", "responsibilities": "(INFERRED) Investing in ASALs, creating employment, adhering to sustainable practices."})

process['as_is_narrative'] = "(INFERRED) The Ministry of ASALs and Regional Development operates by formulating and reviewing policies, laws, and legal frameworks specifically tailored to address the unique challenges and opportunities in Kenya's Arid and Semi-Arid Lands, as well as to guide the effective implementation of devolution. It provides crucial technical and financial support to county governments within ASAL regions, assisting them in developing and implementing their development plans, enhancing service delivery, and building institutional capacity. The Ministry plays a vital coordinating role, bringing together various national government ministries and departments (e.g., Agriculture, Water, Education, Health) to ensure integrated and cross-sectoral interventions that address the multi-faceted development needs of ASAL communities. It actively facilitates dialogue and collaboration between national and county governments to ensure seamless service provision and policy alignment. Engaging local communities in development processes is a cornerstone of its approach, fostering ownership and sustainability of projects. During periods of drought or other crises, the Ministry is responsible for coordinating the management and distribution of food relief and other emergency aid. Furthermore, it actively promotes and attracts investment into ASAL regions, encouraging economic activities suitable for these environments, such as drought-resistant agriculture, livestock development, and renewable energy. The Ministry continuously monitors and evaluates the impact of development programs to ensure they are responsive to the unique needs of ASAL populations and contribute to equitable national development."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions from reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://africa2trust.com/", # Provided context
    "https://nyongesasande.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighty-third process enriched and combined_data.json updated.")
