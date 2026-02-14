
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventy-fifth process (index 74)
process = data['processes'][74]

# Populate fields
process['executive_summary'] = "The National Irrigation Authority (NIA) is a state corporation in Kenya operating under the Irrigation Act 2019. Its primary mandate is to foster sustainable food security and socio-economic development through the development, expansion, management, oversight, and regulation of irrigation practices and infrastructure across the country. NIA plays a crucial role in increasing agricultural productivity, mitigating the effects of climate change, and improving the livelihoods of farming communities by ensuring efficient and reliable water use for agriculture."
process['process_overview']['process_objective'] = "To develop and enhance irrigation infrastructure for both national and public schemes; to offer irrigation support services to private medium and smallholder schemes in collaboration with county governments and other relevant parties; to provide technical advisory services for irrigation schemes covering design, construction supervision, administration, operation, and maintenance; to advise the Cabinet Secretary on matters related to the development, maintenance, expansion, and availability of irrigation support services; to allocate land within national irrigation schemes for public use; to promote the marketing, safe storage, and processing of agricultural products from irrigation schemes in partnership with county governments and other agencies; to conduct research to recommend fair prices for agricultural products from irrigation schemes; to facilitate the establishment and strengthening of irrigation water users' associations and scheme management committees for effective operation and management; to coordinate and plan settlement on national or public irrigation schemes and determine settler numbers; and to offer commercial technical advisory services on irrigation water management, including water harvesting, storage, and wastewater recycling."
process['process_overview']['policy_legal_context'].append("Established under the Irrigation Act 2019, which provides the legal framework for its mandate and functions. NIA operates under the Ministry of Water, Sanitation and Irrigation (or the relevant government ministry responsible for irrigation and water resources) and is central to achieving Kenya's food security goals, supporting agricultural transformation, and adapting to climate change impacts through improved water management in agriculture.")
process['stakeholders'].append({"stakeholder": "Irrigation Farmers / Water Users", "role": "Primary beneficiaries of irrigation schemes; participate in scheme management", "responsibilities": "(INFERRED) Adhering to water use regulations, cultivating crops, participating in Water Users' Associations (WUAs)."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in irrigation development and implementation of agricultural policies at the local level", "responsibilities": "(INFERRED) Collaborating on scheme development, providing agricultural extension services, supporting farmers."})
process['stakeholders'].append({"stakeholder": "Ministry of Water, Sanitation and Irrigation", "role": "Parent Ministry providing policy direction, funding, and oversight", "responsibilities": "(INFERRED) Formulating national water and irrigation policies, allocating resources, strategic guidance."})
process['stakeholders'].append({"stakeholder": "Ministry of Agriculture, Livestock, Fisheries and Cooperatives", "role": "Collaborates on agricultural policies, research, and market linkages for irrigated produce", "responsibilities": "(INFERRED) Providing agricultural expertise, supporting research, facilitating market access."})
process['stakeholders'].append({"stakeholder": "Water Resource Management Authority (WRMA)", "role": "Regulates water resources; collaborates on water abstraction for irrigation", "responsibilities": "(INFERRED) Issuing water permits, monitoring water abstraction, ensuring sustainable water use."})
process['stakeholders'].append({"stakeholder": "Research Institutions (e.g., KALRO)", "role": "Provide scientific research and improved crop varieties suitable for irrigated agriculture", "responsibilities": "(INFERRED) Conducting agricultural research, developing resilient crop varieties, advising on irrigation technologies."})
process['stakeholders'].append({"stakeholder": "Agricultural Produce Marketers / Processors", "role": "Partners in promoting value addition and market access for irrigated agricultural products", "responsibilities": "(INFERRED) Buying and processing produce, developing market linkages."})
process['stakeholders'].append({"stakeholder": "Financial Institutions", "role": "Provide funding for irrigation projects and agricultural loans to farmers", "responsibilities": "(INFERRED) Offering agricultural financing, supporting irrigation infrastructure investments."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Directly impacted by irrigation projects; beneficiaries of improved livelihoods and food security", "responsibilities": "(INFERRED) Participating in project planning, providing labor, practicing sustainable agriculture."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support irrigation programs and infrastructure development", "responsibilities": "(INFERRED) Funding irrigation projects, sharing expertise in water management and agricultural development."})

process['as_is_narrative'] = "(INFERRED) The National Irrigation Authority (NIA) implements its mandate through a structured approach to irrigation development and management. This involves identifying viable areas for irrigation, conducting feasibility studies, and then designing and constructing new irrigation infrastructure, including dams, water diversion structures, primary and secondary canals, furrows, and pumping stations. NIA is also responsible for the rehabilitation, modernization, and expansion of existing irrigation schemes to enhance efficiency and productivity. Technical support is a core service, where NIA provides expertise to farmers and scheme management committees on irrigation best practices, water use efficiency, crop selection, and soil management. It actively trains and builds the capacity of Water Users' Associations (WUAs) in scheme operation, maintenance, and governance to ensure sustainable management. NIA collaborates extensively with county governments to support smallholder irrigation initiatives and promote climate-smart agriculture. Research activities focus on identifying improved crop varieties suitable for irrigated conditions and analyzing market dynamics to ensure profitability for farmers. NIA regulates water abstraction for irrigation purposes, ensuring equitable distribution and sustainable resource utilization. Furthermore, it promotes post-harvest handling, value addition, and market linkages for produce from irrigation schemes. For national schemes, NIA coordinates the planning and settlement of farmers, ensuring equitable land allocation and adherence to sustainable farming practices."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.irrigationauthority.go.ke/", # Official website
    "https://devex.com/", # Provided context
    "https://aiap.or.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventy-fifth process enriched and combined_data.json updated.")
