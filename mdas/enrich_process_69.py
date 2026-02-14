
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventieth process (index 69)
process = data['processes'][69]

# Populate fields
process['executive_summary'] = "The National Cereals and Produce Board (NCPB) is a commercial State Corporation in Kenya operating under the Ministry of Agriculture, Livestock, Fisheries and Cooperatives. Its primary mandate is to provide logistics support services to the government on food security matters and to carry out market intervention for grains and farm inputs on behalf of the government. Additionally, NCPB engages in commercial trading of agricultural commodities, especially cereals, and is responsible for managing the National Food Reserves (NFR), playing a critical role in stabilizing food supply and prices across the nation."
process['process_overview']['process_objective'] = "To ensure national food security through efficient strategic grain reserve management; to stabilize cereal prices by managing market interventions to protect farmers and ensure affordable food for consumers; to regulate the cereal and produce market by setting quality standards, monitoring market trends, and enforcing fair trade practices; to supply essential farm inputs such as fertilizers and seeds to enhance agricultural productivity; to offer comprehensive post-harvest services including drying, cleaning, storage, and fumigation to farmers and other clients; to facilitate the marketing and export of cereals and produce to regional and international markets; to conduct research and development activities to improve agricultural practices and enhance produce quality; to provide capacity building for farmers, traders, and other stakeholders; to operate a robust Warehouse Receipt System (WRS); and to offer clearing and forwarding services for grain imports and exports."
process['process_overview']['policy_legal_context'].append("Established as a commercial State Corporation operating under the Ministry of Agriculture, Livestock, Fisheries and Cooperatives. Its mandate is derived from national policies aimed at ensuring food security, supporting agricultural markets, and stabilizing prices. NCPB's operations are guided by relevant agricultural acts and regulations, and it plays a key role in implementing government food security strategies, including managing the National Food Reserves.")
process['stakeholders'].append({"stakeholder": "Cereal Farmers (especially maize farmers)", "role": "Suppliers of cereals to NCPB; beneficiaries of price stabilization and input programs", "responsibilities": "(INFERRED) Producing cereals, selling produce to NCPB, utilizing inputs and post-harvest services."})
process['stakeholders'].append({"stakeholder": "Consumers", "role": "Beneficiaries of stable food prices and guaranteed food supply", "responsibilities": "(INFERRED) Purchasing cereals at fair prices, relying on NCPB for food security."})
process['stakeholders'].append({"stakeholder": "Grain Traders / Millers", "role": "Commercial partners in the cereal value chain; interact with NCPB for supply and market information", "responsibilities": "(INFERRED) Procuring grains, processing cereals, participating in open market trade."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (Ministry of Agriculture, Livestock, Fisheries and Cooperatives; National Treasury)", "role": "Provides policy direction, oversight, and funding for food security initiatives", "responsibilities": "(INFERRED) Formulating food security policies, allocating resources to NCPB, monitoring performance."})
process['stakeholders'].append({"stakeholder": "Local and International Buyers / Exporters", "role": "Engage with NCPB for commercial trading and export of cereals", "responsibilities": "(INFERRED) Purchasing cereals for various markets, complying with trade regulations."})
process['stakeholders'].append({"stakeholder": "Agricultural Input Suppliers", "role": "Partners in providing fertilizers, seeds, and other farm inputs to farmers through NCPB channels", "responsibilities": "(INFERRED) Supplying quality inputs, collaborating on distribution networks."})
process['stakeholders'].append({"stakeholder": "Financial Institutions (for WRS)", "role": "Collaborate with NCPB to provide credit facilities against warehouse receipts for farmers", "responsibilities": "(INFERRED) Offering financial products, supporting agricultural financing schemes."})
process['stakeholders'].append({"stakeholder": "Research Institutions (e.g., KALRO)", "role": "Provide scientific research and improved crop varieties to enhance agricultural productivity", "responsibilities": "(INFERRED) Conducting agricultural research, advising on best practices."})
process['stakeholders'].append({"stakeholder": "Transporters / Logistics Providers", "role": "Provide transportation services for movement of grains and inputs to and from NCPB depots", "responsibilities": "(INFERRED) Ensuring timely and efficient delivery, adhering to logistics standards."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in local agricultural development and food security initiatives", "responsibilities": "(INFERRED) Collaborating on agricultural programs, supporting local farmers."})

process['as_is_narrative'] = "(INFERRED) NCPB's operational framework is centered on its dual role of strategic food reserve management and commercial trading. During harvest seasons, NCPB actively procures cereals, primarily maize, directly from farmers at government-set prices to build up the National Food Reserves and for its commercial stock. These cereals are then stored in NCPB's extensive network of depots across the country, utilizing advanced storage techniques to minimize post-harvest losses. NCPB also offers critical post-harvest services like drying, cleaning, and fumigation to farmers and other clients, enhancing the quality and shelf-life of their produce. In times of food scarcity or high prices, NCPB releases grains from its reserves to stabilize the market and ensure availability at affordable prices. Its commercial arm engages in buying and selling grains at market rates, ensuring a steady supply. NCPB plays a key role in the distribution of subsidized agricultural inputs, such as fertilizers and seeds, to farmers, aiming to boost production. Furthermore, it operates a certified Warehouse Receipt System, allowing farmers to deposit their produce and obtain a receipt that can be used as collateral for loans, thereby improving access to finance. NCPB also facilitates both local and export marketing of cereals, ensuring that Kenyan produce reaches diverse markets."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.ncpb.co.ke/",
    "https://ecitizen.go.ke/", # Provided context
    "https://gauthmath.com/", # Provided context
    "https://saraka.info/", # Provided context
    "https://devex.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventieth process enriched and combined_data.json updated.")
