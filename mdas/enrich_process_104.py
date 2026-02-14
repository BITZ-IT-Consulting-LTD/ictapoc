
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the hundred and fifth process (index 104)
process = data['processes'][104]

# Populate fields
process['executive_summary'] = "Chemelil Sugar Company Limited is a state-owned sugar milling company in Kenya, established in 1973 under the Companies Act (Cap 486) and becoming a parastatal in 1974. Its principal activity and mission are to manufacture sugar and co-products from sugarcane, and to establish and manage sugarcane plantations. Chemelil Sugar aims to be a preferred choice in sugar production and marketing, as well as in sugarcane development within the region, thereby contributing significantly to national self-sufficiency in sugar production and the economic well-being of sugarcane farmers and local communities."
process['process_overview']['process_objective'] = "To mill sugarcane into refined sugar for both domestic and industrial markets; to provide farmers with improved cane varieties, technical support, and agricultural inputs for sustainable sugarcane development; to promote and distribute sugar across local and regional markets; to offer financial assistance, extension services, and input provision to contracted sugarcane farmers; to generate direct and indirect employment opportunities within the factory, farms, and transportation sectors; to conduct research to develop better cane varieties, enhance disease resistance, and improve processing methods; to develop and maintain transport and logistical infrastructure to facilitate efficient cane delivery; to diversify its operations by exploring and producing by-products such as molasses and ethanol; to contribute to the national economy through sugar sales, tax revenue, and reducing sugar imports; to promote sustainable farming practices, waste recycling, and minimizing the environmental impact of its operations; and to implement and maintain quality management systems and adhere to corporate governance principles."
process['process_overview']['policy_legal_context'].append("Established in 1973 under the Companies Act (Cap 486) of Kenya, with its operations commencing in 1976, and became a parastatal in 1974. Chemelil Sugar operates under the Ministry of Agriculture, Livestock, Fisheries and Cooperatives (or the relevant government ministry responsible for agriculture and industrialization) and is central to implementing national agricultural and industrial policies aimed at achieving sugar self-sufficiency, enhancing farmer livelihoods, and promoting economic development in the sugar belt region. Its operations are also subject to regulatory oversight by the Sugar Directorate and environmental regulations.")
process['stakeholders'].append({"stakeholder": "Sugarcane Farmers (contracted and outgrowers)", "role": "Primary suppliers of sugarcane to the factory; beneficiaries of technical and financial support", "responsibilities": "(INFERRED) Cultivating sugarcane, supplying cane to the factory, adhering to contract terms, adopting improved farming practices."})
process['stakeholders'].append({"stakeholder": "Employees", "role": "Workforce contributing to Chemelil's production, farming, and administrative operations", "responsibilities": "(INFERRED) Performing duties, adhering to safety protocols, contributing to productivity."})
process['stakeholders'].append({"stakeholder": "Consumers of Sugar", "role": "End-users of Chemelil's refined sugar; benefit from local production and market stability", "responsibilities": "(INFERRED) Purchasing local sugar, benefiting from stable supply and prices."})
process['stakeholders'].append({"stakeholder": "Industrial Users of Sugar (e.g., beverage companies)", "role": "Commercial clients for Chemelil's sugar products", "responsibilities": "(INFERRED) Procuring sugar for industrial use, complying with quality standards."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (Ministry of Agriculture, Livestock, Fisheries and Cooperatives; National Treasury)", "role": "Owner and oversight body; provides policy direction, funding, and support to the sugar sector", "responsibilities": "(INFERRED) Formulating agricultural policies, allocating resources, ensuring food security, strategic guidance."})
process['stakeholders'].append({"stakeholder": "Sugar Directorate (regulator)", "role": "Regulates the sugar industry; collaborates with Chemelil on compliance and industry standards", "responsibilities": "(INFERRED) Setting industry standards, monitoring compliance, advising on sugar policy."})
process['stakeholders'].append({"stakeholder": "Kenya Bureau of Standards (KEBS)", "role": "Sets and enforces national quality standards for sugar and other products", "responsibilities": "(INFERRED) Ensuring product quality, conducting inspections, certifying products."})
process['stakeholders'].append({"stakeholder": "Environmental Management Agencies (e.g., NEMA)", "role": "Ensures Chemelil's operations comply with environmental regulations and promote sustainability", "responsibilities": "(INFERRED) Enforcing environmental laws, monitoring pollution, promoting sustainable practices."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Impacted by Chemelil's operations (employment, environment); beneficiaries of CSR activities", "responsibilities": "(INFERRED) Engaging with Chemelil, benefiting from employment and CSR, raising environmental concerns."})
process['stakeholders'].append({"stakeholder": "Transporters / Logistics Providers", "role": "Provide transportation services for sugarcane and sugar products", "responsibilities": "(INFERRED) Ensuring efficient and timely transport, adhering to logistics standards."})
process['stakeholders'].append({"stakeholder": "Financial Institutions", "role": "Provide funding for Chemelil's operations, expansion projects, and farmer financing", "responsibilities": "(INFERRED) Offering corporate financing, providing agricultural loans, supporting the sugar industry."})

process['as_is_narrative'] = "(INFERRED) Chemelil Sugar Company Limited actively manages its operations across the sugarcane value chain, integrating both farming and industrial processes. It operates extensive sugarcane plantations and closely coordinates with a network of contracted outgrower farmers, providing them with essential support services such as improved cane varieties, land preparation, agricultural inputs (fertilizers, chemicals), and expert extension advice to ensure a consistent and high-quality supply of sugarcane to the factory. The core of its operations involves milling the harvested sugarcane in its factory, employing advanced processes to extract refined sugar. During this process, valuable co-products like molasses and bagasse are also generated, with molasses often being further processed into ethanol or sold to other industries. Chemelil ensures that its processed sugar meets stringent national quality standards as set by the Kenya Bureau of Standards (KEBS) for both domestic consumption and industrial use. The company implements robust marketing and distribution strategies to ensure its sugar products reach consumers and industrial clients across Kenya and potentially the regional market. Continuous investment in research and development is undertaken to enhance cane productivity (e.g., disease-resistant varieties), improve processing efficiency, and explore further diversification opportunities into value-added by-products. Chemelil develops and maintains its network of internal roads and other logistical infrastructure to facilitate the efficient delivery of cane to the factory. The company is committed to environmental sustainability, implementing practices like waste management, effluent treatment, and pollution control in its farming and factory operations, and adheres to corporate governance codes (Mwongozo Code) and quality management systems (ISO standards) to ensure operational excellence and accountability."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.chemsugar.go.ke/", # Official website
    "https://parliament.go.ke/", # Provided context
    "https://saraka.info/", # Provided context
    "https://uonbi.ac.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Hundred and fifth process enriched and combined_data.json updated.")
