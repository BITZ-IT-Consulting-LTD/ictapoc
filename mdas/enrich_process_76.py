
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventy-seventh process (index 76)
process = data['processes'][76]

# Populate fields
process['executive_summary'] = "The National Oil Corporation of Kenya (NOCK) is a state corporation established in 1981 with the mandate to participate in all aspects of the Kenyan petroleum industry. NOCK is strategically involved in upstream (oil and gas exploration), midstream (petroleum infrastructure development), and downstream (marketing and distribution of petroleum products) operations. Its core aim is to ensure Kenya's energy security, stabilize petroleum prices, and optimize the utilization of petroleum resources for national development, contributing to the country's economic stability and growth."
process['process_overview']['process_objective'] = "To actively participate in oil and gas exploration activities in Kenya, including marketing the country's exploration acreage, managing gas and exploration data, and operating its own exploration acreage; to develop robust petroleum infrastructure, encompassing projects like establishing an offshore floating jetty (Single Buoy Mooring - SBM), creating Strategic Petroleum Reserves (SPR), and formulating a comprehensive Petroleum Development Master Plan for Kenya; to efficiently market and distribute petroleum products through its nationwide retail network, supplying resellers, industrial clients, and government entities, and offering specialized products and services such as SupaGas (LPG), Supa lubricants, and the SupaCard electronic fuel management system; and fundamentally, to ensure Kenya's energy security by guaranteeing a stable supply of petroleum products and contributing to the stabilization of petroleum prices."
process['process_overview']['policy_legal_context'].append("Established in 1981, NOCK derives its mandate from its founding legal instruments and subsequent energy legislation, which empower it to participate across the entire petroleum value chain in Kenya. It operates under the Ministry of Energy and Petroleum (or the relevant government ministry responsible for energy matters) and is a key implementer of national energy policies aimed at ensuring energy security, promoting local content in the petroleum sector, and optimizing the exploration and utilization of the country's petroleum resources for sustainable development.")
process['stakeholders'].append({"stakeholder": "Kenyan Consumers (of petroleum products)", "role": "Primary end-users of NOCK's downstream products and beneficiaries of stable prices", "responsibilities": "(INFERRED) Purchasing petroleum products, adhering to safety guidelines."})
process['stakeholders'].append({"stakeholder": "Petroleum Industry Players (Oil Marketing Companies, independent dealers)", "role": "Competitors and partners in the downstream petroleum market", "responsibilities": "(INFERRED) Complying with industry regulations, engaging in fair market practices."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (Ministry of Energy and Petroleum, National Treasury)", "role": "Parent Ministry providing policy direction, funding, and oversight; owner of NOCK", "responsibilities": "(INFERRED) Formulating energy policies, allocating resources, strategic guidance for the petroleum sector."})
process['stakeholders'].append({"stakeholder": "International Oil Companies (IOCs) (for exploration partnerships)", "role": "Partners in oil and gas exploration and development projects", "responsibilities": "(INFERRED) Investing in exploration, sharing technical expertise, complying with local content rules."})
process['stakeholders'].append({"stakeholder": "Petroleum Regulatory Authority (EPRA)", "role": "Regulates the energy sector, including petroleum pricing and standards; collaborates with NOCK on compliance", "responsibilities": "(INFERRED) Setting petroleum standards, regulating prices, ensuring market stability."})
process['stakeholders'].append({"stakeholder": "Local Communities (in exploration/production areas)", "role": "Directly impacted by NOCK's upstream activities; potential beneficiaries of local content and CSR", "responsibilities": "(INFERRED) Engaging with NOCK, participating in CSR, seeking benefits from resource development."})
process['stakeholders'].append({"stakeholder": "Financial Institutions", "role": "Provide funding for NOCK's projects and operations across the value chain", "responsibilities": "(INFERRED) Offering project financing, supporting energy sector investments."})
process['stakeholders'].append({"stakeholder": "Transporters / Logistics Companies", "role": "Provide transportation services for crude oil and refined petroleum products", "responsibilities": "(INFERRED) Ensuring safe and efficient transportation, adhering to industry standards."})
process['stakeholders'].append({"stakeholder": "Suppliers of petroleum products and equipment", "role": "Provide NOCK with necessary inputs for its operations (e.g., crude oil, refined products, exploration equipment)", "responsibilities": "(INFERRED) Supplying quality products, adhering to contractual terms."})

process['as_is_narrative'] = "(INFERRED) The National Oil Corporation of Kenya (NOCK) actively participates across the entire petroleum value chain to fulfill its mandate. In the upstream sector, NOCK is involved in marketing Kenya's exploration acreage to attract international investors, manages critical geological and exploration data for informed decision-making, and directly operates its own exploration blocks (e.g., Block 14T). Midstream, NOCK plays a crucial role in developing strategic petroleum infrastructure, such as the Single Buoy Mooring (SBM) for efficient crude oil offloading and the establishment of Strategic Petroleum Reserves (SPR) to enhance national energy security. It also contributes to the formulation of Kenya's Petroleum Development Master Plan. In the downstream sector, NOCK manages an extensive nationwide retail network of over 99 service stations, ensuring widespread availability of petroleum products. It supplies fuel and lubricants to a diverse clientele, including resellers, industrial clients, and various government entities from its Nairobi National Terminal. NOCK markets specialized products like SupaGas (LPG) and Supa lubricants, and leverages technology through its SupaCard electronic fuel management system to improve efficiency. Through these integrated operations, NOCK works to stabilize domestic petroleum prices and guarantee a consistent supply of petroleum products across the country, all while striving to enhance efficiency and service delivery within the broader context of contributing to Kenya's energy security."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.nationaloil.co.ke/", # Official website
    "https://wikipedia.org/", # Provided context
    "https://africa2trust.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventy-seventh process enriched and combined_data.json updated.")
