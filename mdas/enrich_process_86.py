
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighty-seventh process (index 86)
process = data['processes'][86]

# Populate fields
process['executive_summary'] = "Ahero Rice Mills is a key rice processing facility in Kenya, operating under a tripartite agreement involving the Kisumu County Government, the National Irrigation Authority (NIA), and a private investor (Upland Crop Company). Its primary mandate is to revitalize rice processing, provide a competitive and profitable market for local rice farmers, particularly those in the Ahero, West Kano, and South West Kano irrigation schemes. The mill aims to significantly boost national rice production, contributing to Kenya's food security goals and socio-economic development in the Western Kenya region through value addition and job creation."
process['process_overview']['process_objective'] = "To process rice efficiently, utilizing modern facilities for sorting, grading, and packaging, with a capacity of 2.5 metric tons of rice per hour or approximately 60 tons daily; to offer a competitive and profitable market for small and medium-scale rice growers within Western Kenya's irrigation schemes (Ahero, West Kano, and South West Kano); to significantly increase local rice production, thereby helping to reduce Kenya's national rice deficit and aligning with government strategies such as the Bottom-Up Economic Transformation Agenda (BETA) and the National Rice Development Strategy II (2020–2030) for achieving rice self-sufficiency by 2030; to enhance the value of rice by providing advanced processing capabilities that address issues of selling lower-priced unmilled paddy; to connect local rice farmers with quality inputs and services, fostering the sustainable growth of the regional rice industry; and to create jobs and stimulate economic growth in the surrounding area."
process['process_overview']['policy_legal_context'].append("Ahero Rice Mills operates under a tripartite agreement involving the Kisumu County Government, the National Irrigation Authority (NIA), and a private investor (Upland Crop Company). Its establishment and functions are aligned with national food security policies and agricultural development strategies, particularly those aimed at achieving rice self-sufficiency and supporting smallholder farmers. NIA's role as a host and partner under the Irrigation Act 2019 provides a regulatory and operational context for the mill's integration within the broader irrigation scheme framework. The initiative is also a component of national economic development agendas like the Bottom-Up Economic Transformation Agenda (BETA).")
process['stakeholders'].append({"stakeholder": "Rice Farmers (in Ahero, West Kano, South West Kano schemes)", "role": "Primary suppliers of paddy rice to the mill; beneficiaries of a ready market and competitive prices", "responsibilities": "(INFERRED) Cultivating rice, supplying paddy to the mill, adopting improved farming practices."})
process['stakeholders'].append({"stakeholder": "Kisumu County Government", "role": "Partner in the tripartite agreement; supports local agricultural development and infrastructure", "responsibilities": "(INFERRED) Collaborating on agricultural policies, providing local support, promoting rice farming."})
process['stakeholders'].append({"stakeholder": "National Irrigation Authority (NIA)", "role": "Partner in the tripartite agreement; responsible for irrigation infrastructure and scheme productivity", "responsibilities": "(INFERRED) Ensuring efficient water management, maintaining irrigation infrastructure, supporting rice cultivation."})
process['stakeholders'].append({"stakeholder": "Upland Crop Company (private investor)", "role": "Private sector partner in the tripartite agreement; brings investment and operational expertise to the mill", "responsibilities": "(INFERRED) Operating the mill, managing commercial aspects, ensuring profitability."})
process['stakeholders'].append({"stakeholder": "Consumers of Rice", "role": "End-users of the processed rice; benefit from increased availability of locally produced rice", "responsibilities": "(INFERRED) Purchasing locally milled rice, supporting local agriculture."})
process['stakeholders'].append({"stakeholder": "Agricultural Input Suppliers", "role": "Provide essential inputs (seeds, fertilizers, pesticides) to rice farmers", "responsibilities": "(INFERRED) Supplying quality inputs, collaborating with farmers and partners."})
process['stakeholders'].append({"stakeholder": "Rice Traders / Marketers", "role": "Distribute milled rice to various markets; partners in the value chain", "responsibilities": "(INFERRED) Marketing and distributing milled rice, creating market linkages."})
process['stakeholders'].append({"stakeholder": "Financial Institutions", "role": "Provide financial services to farmers and the mill (e.g., loans, credit facilities)", "responsibilities": "(INFERRED) Offering agricultural financing, supporting mill operations."})
process['stakeholders'].append({"stakeholder": "Local Communities (for employment)", "role": "Beneficiaries of job creation and economic stimulation from the mill's operations", "responsibilities": "(INFERRED) Supplying labor, benefiting from economic activities."})
process['stakeholders'].append({"stakeholder": "Ministry of Agriculture, Livestock, Fisheries and Cooperatives", "role": "Provides policy guidance and support for agricultural development and food security initiatives", "responsibilities": "(INFERRED) Formulating agricultural policies, supporting rice sector development."})

process['as_is_narrative'] = "(INFERRED) Ahero Rice Mills functions as a critical component of the rice value chain in Western Kenya, primarily serving farmers from the Ahero, West Kano, and South West Kano irrigation schemes. The mill receives paddy rice directly from these farmers, providing them with a reliable and competitive market for their produce, which was previously a major challenge. Upon arrival, the paddy undergoes processing using modern milling machinery capable of handling 2.5 metric tons per hour. This process includes sorting, grading, and packaging the rice to high-quality standards, thereby enhancing its market value and reducing post-harvest losses. Operationally, the mill works closely with the National Irrigation Authority (NIA) to ensure the sustained productivity of the irrigation schemes, including efficient water management and farmer support. Concurrently, it engages with the Kisumu County Government on local agricultural development plans and market linkages for the milled rice. The private investor (Upland Crop Company) brings commercial expertise to optimize mill operations, supply chain management, and distribution to various markets. By offering advanced processing and a guaranteed market, Ahero Rice Mills encourages increased rice cultivation in the region, improves farmer incomes, and contributes significantly to the national objective of achieving rice self-sufficiency. Its presence also stimulates the local economy through job creation and supports allied industries, making it a pivotal agro-processing hub."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, operational structure from reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://mygov.go.ke/", # Provided context
    "https://kisumu.go.ke/", # Provided context
    "https://millingmea.com/", # Provided context
    "https://www.irrigationauthority.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighty-seventh process enriched and combined_data.json updated.")
