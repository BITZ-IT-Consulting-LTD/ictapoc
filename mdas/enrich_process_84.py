
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighty-fifth process (index 84)
process = data['processes'][84]

# Populate fields
process['executive_summary'] = "The Agricultural Development Corporation (ADC) Kenya is a government parastatal established in 1965 under an Act of Parliament (Cap 444 of 1986). Its primary mandate is to promote and execute agricultural schemes and reconstruction in Kenya, facilitating the commercialization of agriculture, promoting agro-industrial ventures, and enhancing national food security. ADC plays a crucial role in the production of essential agricultural inputs, particularly quality seeds and pedigree and high-grade livestock, to support farmers and drive agricultural transformation."
process['process_overview']['process_objective'] = "To promote and execute agricultural schemes and reconstruction across Kenya; to initiate, assist, or expand agricultural undertakings and enterprises; to promote the production of essential agricultural inputs for Kenya, such as seeds and pedigree and high-grade livestock; to multiply basic seed to ensure the availability of sufficient quantities of high-quality seed for farmers; to act as the custodian of national livestock studs and work to preserve breeds; to facilitate the transfer of technology from research institutions to farmers; to serve as a testing ground for new agricultural technologies; to provide training to farmers and agribusinesses through various programs; to manage state farms and estates for the production of essential crops; to contribute significantly to national food security and poverty reduction; to support agro-industries that process agricultural goods; to provide financing, technical assistance, and support to farming operations; to support land development, irrigation projects, and improvements in farm infrastructure; to promote environmentally sustainable farming methods and practices; and to support marketing and distribution efforts for agricultural produce."
process['process_overview']['policy_legal_context'].append("Established in 1965 under an Act of Parliament (initially Cap 346, later revised to Cap 444 of 1986), which provides the legal framework for its mandate and functions. ADC operates under the Ministry of Agriculture, Livestock, Fisheries and Cooperatives (or the relevant government ministry responsible for agriculture) and is central to implementing national agricultural development policies and strategies, particularly those related to food security, commercial agriculture, and livestock development.")
process['stakeholders'].append({"stakeholder": "Farmers (small and large scale)", "role": "Primary beneficiaries of ADC's seed, livestock, and technology transfer programs; clients for training and support", "responsibilities": "(INFERRED) Utilizing improved inputs, adopting modern practices, participating in training."})
process['stakeholders'].append({"stakeholder": "Livestock Farmers", "role": "Beneficiaries of ADC's pedigree livestock and genetic improvement programs", "responsibilities": "(INFERRED) Improving their herds, utilizing artificial insemination services."})
process['stakeholders'].append({"stakeholder": "Seed Companies (e.g., Kenya Seed Company)", "role": "Partners in seed multiplication and distribution; often a major customer for ADC's basic seed", "responsibilities": "(INFERRED) Partnering with ADC, distributing quality seeds to farmers."})
process['stakeholders'].append({"stakeholder": "Agricultural Research Institutions (e.g., KALRO)", "role": "Sources of new agricultural technologies and improved varieties; collaborate with ADC on research and trials", "responsibilities": "(INFERRED) Developing new technologies, conducting research, collaborating on field trials."})
process['stakeholders'].append({"stakeholder": "Agro-industrial Processors", "role": "Process agricultural raw materials supplied by ADC and other farmers; clients for ADC's produce", "responsibilities": "(INFERRED) Processing agricultural goods, creating value-added products, supporting supply chains."})
process['stakeholders'].append({"stakeholder": "Ministry of Agriculture, Livestock, Fisheries and Cooperatives", "role": "Parent Ministry providing policy direction, funding, and oversight to ADC", "responsibilities": "(INFERRED) Formulating agricultural policies, allocating resources, strategic guidance for food security."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in local agricultural development and extension services", "responsibilities": "(INFERRED) Collaborating on agricultural programs, supporting local farmers, providing extension support."})
process['stakeholders'].append({"stakeholder": "Consumers (of agricultural products)", "role": "Beneficiaries of increased food production and stable prices", "responsibilities": "(INFERRED) Purchasing food products, benefiting from national food security."})
process['stakeholders'].append({"stakeholder": "Financial Institutions", "role": "Provide funding for ADC's projects and agricultural loans to farmers", "responsibilities": "(INFERRED) Offering agricultural financing, supporting ADC's operations."})
process['stakeholders'].append({"stakeholder": "Agricultural Input Suppliers", "role": "Provide farm inputs (fertilizers, chemicals, equipment) to ADC and other farmers", "responsibilities": "(INFERRED) Supplying quality inputs, collaborating on distribution."})
process['stakeholders'].append({"stakeholder": "Training Institutions", "role": "Collaborate with ADC on training programs for farmers and agribusiness professionals", "responsibilities": "(INFERRED) Developing training curricula, providing capacity building."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support agricultural development programs", "responsibilities": "(INFERRED) Funding projects, sharing expertise in agricultural best practices."})

process['as_is_narrative'] = "(INFERRED) The Agricultural Development Corporation (ADC) implements its mandate through extensive direct involvement in commercial agriculture and strategic support services. ADC manages vast tracts of agricultural land where it undertakes large-scale commercial farming of essential crops like maize, wheat, and potatoes. A critical function is the multiplication of basic seed for various crops, which is then supplied to seed companies (such as Kenya Seed Company) for further processing and distribution to farmers, thereby ensuring the availability of high-quality planting material and underpinning national food security. In the livestock sector, ADC acts as the custodian of national pedigree livestock studs, focusing on genetic improvement through breeding programs and artificial insemination services, and supplying high-grade animals to farmers. The Corporation serves as a vital conduit for agricultural technology transfer, conducting adaptive research and demonstrating improved farming practices from research institutions to the farming community through field days, agricultural shows, and direct farmer engagement. ADC operates several specialized agricultural schemes (e.g., large-scale dairy, horticulture) which serve as models for commercial viability and best practices. It contributes directly to national food reserves through its crop production and plays a role in supporting agro-industrial processors. Furthermore, ADC actively promotes sustainable agricultural practices, land development, and modern farm mechanization to enhance overall productivity and efficiency in the Kenyan agricultural sector."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://africa2trust.com/", # Provided context
    "https://saraka.info/", # Provided context
    "https://agrarian.co.ke/", # Provided context
    "https://youtube.com/", # Provided context
    "https://policyvault.africa/", # Provided context
    "https://fao.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighty-fifth process enriched and combined_data.json updated.")
