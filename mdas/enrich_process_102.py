
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and third process (index 102)
process = data['processes'][102]

# Populate fields
process['executive_summary'] = "The Central Rift Valley Water Works Development Agency (CRVWWDA) is one of nine Water Works Development Agencies in Kenya, established under Section 65 of the Water Act, 2016, through Kenya Gazette Notice No. 4 on February 7, 2020. Operating as a state corporation under the Ministry of Water & Sanitation and Irrigation, it is responsible for the development, maintenance, and management of national public water works within its jurisdiction, which includes Nakuru, Narok, Laikipia, Baringo, and Nyandarua counties. The Agency aims to plan, develop, and deliver efficient and reliable water and sanitation infrastructure to ensure sustainable access for all stakeholders."
process['process_overview']['process_objective'] = "To undertake the development, maintenance, and management of national public water works within its designated service area (Nakuru, Narok, Laikipia, Baringo, and Nyandarua counties); to operate water works as a water service provider until the responsibility for operation and management is handed over to a designated water services provider, county government, joint committee, or authority of county governments; to provide water services when ordered by the Regulatory Board, particularly in cases where a defaulting water services provider's functions are transferred; to offer technical services and capacity building to county governments and water services providers upon request; and to provide technical support to the Cabinet Secretary in discharging duties under the Constitution and the Water Act, 2016."
process['process_overview']['policy_legal_context'].append("Established under Section 65 of the Water Act, 2016, through Kenya Gazette Notice No. 4 on February 7, 2020. Its core mandate and functions are further provided by Section 68 of the Water Act, 2016. CRVWWDA operates as a state corporation under the Ministry of Water & Sanitation and Irrigation and aligns its activities with national water sector reforms, policies, and strategies aimed at enhancing access to safe, adequate, and affordable water and sanitation services for all Kenyans.")
process['stakeholders'].append({"stakeholder": "Residents / Consumers (in Nakuru, Narok, Laikipia, Baringo, and Nyandarua counties)", "role": "Primary beneficiaries of improved water and sanitation services provided by CRVWWDA's projects", "responsibilities": "(INFERRED) Paying for water services, conserving water, reporting service disruptions."})
process['stakeholders'].append({"stakeholder": "County Governments (Nakuru, Narok, Laikipia, Baringo, Nyandarua)", "role": "Partners in water and sanitation development; benefit from CRVWWDA's technical support and infrastructure", "responsibilities": "(INFERRED) Collaborating on water projects, providing local support, planning for water sector development."})
process['stakeholders'].append({"stakeholder": "Water Service Providers (WSPs)", "role": "Entities responsible for the retail provision of water and sanitation services; operate infrastructure developed by CRVWWDA", "responsibilities": "(INFERRED) Operating water works efficiently, ensuring service delivery, managing customer relations."})
process['stakeholders'].append({"stakeholder": "Ministry of Water & Sanitation and Irrigation", "role": "Parent Ministry providing policy direction, funding, and oversight to CRVWWDA", "responsibilities": "(INFERRED) Formulating national water policies, allocating resources, strategic guidance for the water sector."})
process['stakeholders'].append({"stakeholder": "Water Services Regulatory Board (WASREB)", "role": "Regulates water services in Kenya, including setting standards and tariffs; oversees WSPs and CRVWWDA's interim role as WSP", "responsibilities": "(INFERRED) Setting regulatory standards, monitoring performance, issuing directives."})
process['stakeholders'].append({"stakeholder": "National Treasury", "role": "Provides funding for CRVWWDA's projects and operations; oversees financial management of parastatals", "responsibilities": "(INFERRED) Allocating budgetary resources, ensuring financial accountability."})
process['stakeholders'].append({"stakeholder": "Environmental Management Agencies (e.g., NEMA)", "role": "Collaborators in ensuring environmental sustainability of water projects; ensure compliance with environmental regulations", "responsibilities": "(INFERRED) Conducting environmental impact assessments, enforcing environmental laws related to water resources."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Impacted by water projects; their participation and buy-in are important for project success and sustainability", "responsibilities": "(INFERRED) Participating in project planning, protecting water sources, engaging with CRVWWDA."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support water and sanitation infrastructure development", "responsibilities": "(INFERRED) Funding projects, sharing expertise in water resource management and engineering."})
process['stakeholders'].append({"stakeholder": "Contractors / Consultants", "role": "Engaged by CRVWWDA for the design, supervision, and construction of water and sanitation projects", "responsibilities": "(INFERRED) Delivering quality infrastructure, adhering to project specifications, complying with tender terms."})

process['as_is_narrative'] = "(INFERRED) The Central Rift Valley Water Works Development Agency (CRVWWDA) actively implements its mandate through a structured approach to water and sanitation infrastructure development. This involves identifying and prioritizing critical water supply and sewerage projects within its five-county jurisdiction (Nakuru, Narok, Laikipia, Baringo, and Nyandarua) based on needs assessments and national development plans. The Agency is responsible for the design, procurement, and supervision of the construction of new water supply schemes (including dams, boreholes, water treatment plants, and extensive distribution networks) and sewerage systems. It also undertakes the rehabilitation and expansion of existing water infrastructure to improve coverage, reliability, and water quality. In areas where designated Water Service Providers (WSPs) are not yet fully established or capable, CRVWWDA may temporarily operate water works as a water service provider, ensuring service continuity until handover. A key function involves providing technical assistance and capacity building to county governments and local WSPs, empowering them to better manage their water and sanitation services. CRVWWDA ensures strict adherence to water quality standards set by WASREB and environmental regulations by NEMA throughout its project lifecycle. It mobilizes financial resources for its projects from the National Treasury, development partners, and other sources. Through these integrated efforts, CRVWWDA aims to significantly increase access to safe and affordable water and sanitation services, contributing to public health improvement, economic development, and achieving Kenya's Vision 2030 goals in the water sector."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.crvwwda.go.ke/", # Official website
    "https://opportunitiesforyoungkenyans.co.ke/", # Provided context
    "https://mygov.go.ke/", # Provided context
    "https://tenders.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and third process enriched and combined_data.json updated.")
