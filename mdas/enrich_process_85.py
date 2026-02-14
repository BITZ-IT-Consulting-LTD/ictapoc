
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the eighty-sixth process (index 85)
process = data['processes'][85]

# Populate fields
process['executive_summary'] = "The Agro-Chemical and Food Company Limited (ACFC) in Kenya was established in 1978 as a joint venture between the private sector and the Government of Kenya. Its initial mandate was to produce power alcohol from sugarcane molasses. ACFC has since diversified its operations to focus on the production of various grades of spirits (potable, industrial, and pharmaceutical), baker's yeast (as the sole producer in East and Central Africa), and beverage-grade liquefied carbon dioxide (LCO2). The company continuously embraces technological advancements to meet customer needs, ensures consistent profitability, and practices environmental stewardship within its purview."
process['process_overview']['process_objective'] = "To produce various grades of spirits for potable, industrial, and domestic applications, including Extra Neutral Spirit, Kenya Methylated Spirit, Industrial Methylated Spirit, potable bottled spirits, pharmaceutical spirits (e.g., surgical spirit, instant hand sanitizer), and denatured ethyl alcohol; to be the sole producer of baker's yeast (Active Dry Yeast and Wet Yeast) in East and Central Africa, satisfying various market segments; to produce beverage-grade liquefied carbon dioxide (LCO2); to efficiently utilize sugarcane molasses procured from various sugar factories as a primary raw material; to continuously embrace technological dynamics to meet customer needs and ensure consistent growth in profitability; and to control, maintain, and improve the environment under its purview, with a strong focus on pollution prevention, regulatory compliance, and addressing customer environmental concerns."
process['process_overview']['policy_legal_context'].append("Established in 1978 as a joint venture between the private sector and the Government of Kenya. ACFC operates under the Ministry of Industrialization, Trade and Enterprise Development (or the relevant government ministry responsible for industrial development and manufacturing) and its operations are guided by national industrial production policies, environmental regulations, food safety standards, and specific legislation governing the production and sale of spirits and other agro-based products.")
process['stakeholders'].append({"stakeholder": "Sugarcane Farmers / Sugar Factories (for molasses supply)", "role": "Primary suppliers of molasses, the key raw material for ACFC's production", "responsibilities": "(INFERRED) Supplying quality molasses, adhering to contractual terms, ensuring sustainable sugarcane farming."})
process['stakeholders'].append({"stakeholder": "Beverage Industry (for LCO2)", "role": "Clients for beverage-grade liquefied carbon dioxide", "responsibilities": "(INFERRED) Procuring LCO2, utilizing it in beverage production, complying with quality standards."})
process['stakeholders'].append({"stakeholder": "Bakers / Food Industry (for yeast)", "role": "Clients for baker's yeast (Active Dry Yeast and Wet Yeast)", "responsibilities": "(INFERRED) Procuring yeast, utilizing it in food production, ensuring product quality."})
process['stakeholders'].append({"stakeholder": "Pharmaceutical Companies (for spirits)", "role": "Clients for pharmaceutical-grade spirits (e.g., surgical spirit, denatured ethyl alcohol)", "responsibilities": "(INFERRED) Procuring spirits, utilizing them in pharmaceutical production, complying with industry standards."})
process['stakeholders'].append({"stakeholder": "Industrial Users (for spirits)", "role": "Clients for industrial-grade spirits (e.g., methylated spirits)", "responsibilities": "(INFERRED) Procuring spirits, utilizing them in various industrial processes, adhering to safety regulations."})
process['stakeholders'].append({"stakeholder": "Consumers (of spirits, sanitizers)", "role": "End-users of ACFC's bottled spirits and pharmaceutical products like hand sanitizers", "responsibilities": "(INFERRED) Purchasing products, using them responsibly, providing feedback."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (shareholder, Ministry of Industrialization, Trade and Enterprise Development)", "role": "Co-owner and oversight body; provides policy direction and ensures compliance with national industrialization goals", "responsibilities": "(INFERRED) Strategic guidance, policy formulation, regulatory oversight."})
process['stakeholders'].append({"stakeholder": "Regulatory Bodies (e.g., Kenya Bureau of Standards (KEBS), National Environment Management Authority (NEMA), Kenya Revenue Authority (KRA))", "role": "Ensure product quality, environmental compliance, and tax collection", "responsibilities": "(INFERRED) Setting standards, conducting inspections, enforcing regulations, collecting taxes."})
process['stakeholders'].append({"stakeholder": "Employees", "role": "Workforce contributing to ACFC's production and operations", "responsibilities": "(INFERRED) Performing duties, adhering to safety protocols, contributing to productivity."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Impacted by ACFC's operations (e.g., environmental, employment); beneficiaries of CSR", "responsibilities": "(INFERRED) Engaging with ACFC, benefiting from employment and CSR, raising concerns."})

process['as_is_narrative'] = "(INFERRED) The Agro-Chemical and Food Company Limited (ACFC) operates as a significant industrial producer within Kenya's agro-processing sector. Its production cycle typically begins with the procurement of large quantities of sugarcane molasses from various sugar factories across the country, which serves as the primary raw material. ACFC then utilizes advanced fermentation and distillation processes in its specialized plants to produce a diverse range of spirits, carefully separating and refining them into different grades suitable for potable consumption, industrial applications, and pharmaceutical use. Concurrently, through dedicated production lines, ACFC manufactures baker's yeast, serving as the sole regional supplier, and produces beverage-grade liquefied carbon dioxide as a by-product of fermentation. The company maintains stringent quality control measures at every stage of production to ensure its products meet national and international standards (e.g., KEBS certification). Distribution channels span across Kenya and extend into the East and Central African region, catering to a wide array of clients in the beverage, food, pharmaceutical, and industrial sectors, as well as general consumers for bottled spirits and sanitizers. ACFC demonstrates a commitment to environmental stewardship by implementing environmental management systems focused on pollution prevention, waste treatment, and adherence to NEMA regulations. The company continuously invests in research and development to optimize production processes, improve product quality, and explore opportunities for diversification and market expansion, leveraging its technological capabilities to maintain its competitive edge and ensure sustainable growth."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.acfc.co.ke/", # Official website
    "https://businesslist.co.ke/", # Provided context
    "https://parliament.go.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Eighty-sixth process enriched and combined_data.json updated.")
