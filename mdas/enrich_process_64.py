
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixty-fifth process (index 64)
process = data['processes'][64]

# Populate fields
process['executive_summary'] = "The Kenya Tourism Board (KTB) is a state corporation established under Kenya's Tourism Act No. 28 of 2011. Its primary objective is to market Kenya as a premier and diverse tourist destination at local, national, regional, and international levels. By developing and implementing strategic marketing initiatives, KTB aims to attract a wide range of visitors, thereby boosting the tourism sector's economic contribution, creating employment opportunities, and supporting sustainable tourism development across the country."
process['process_overview']['process_objective'] = "To develop, implement, and coordinate a comprehensive national tourism marketing strategy; to effectively market Kenya globally through various channels and platforms; to identify emerging tourism market needs and trends and advise stakeholders accordingly; to undertake branding initiatives such as 'Magical Kenya' to enhance Kenya's image; to support sustainable and responsible tourism practices; and to conduct robust market research and analysis to inform and evaluate marketing strategies and product development."
process['process_overview']['policy_legal_context'].append("Established under Kenya's Tourism Act No. 28 of 2011, which provides the legal framework for its mandate and operations. KTB functions under the oversight of the Ministry of Tourism, Wildlife and Heritage, and aligns its marketing strategies with national development blueprints and international tourism best practices. Its work is critical to achieving economic growth and job creation targets set for the tourism sector.")
process['stakeholders'].append({"stakeholder": "Tourists (Domestic and International)", "role": "Primary consumers of Kenya's tourism products and services", "responsibilities": "(INFERRED) Visiting Kenya, adhering to travel regulations, respecting local culture and environment."})
process['stakeholders'].append({"stakeholder": "Tour Operators / Travel Agents", "role": "Distributors of Kenya's tourism products; partners in marketing and package development", "responsibilities": "(INFERRED) Selling Kenya as a destination, developing attractive tour packages, providing quality services."})
process['stakeholders'].append({"stakeholder": "Hoteliers / Accommodation Providers", "role": "Offer lodging and hospitality services to tourists", "responsibilities": "(INFERRED) Providing quality accommodation, adhering to hospitality standards, ensuring guest satisfaction."})
process['stakeholders'].append({"stakeholder": "Airlines / Transport Providers", "role": "Facilitate travel to and within Kenya for tourists", "responsibilities": "(INFERRED) Providing safe and efficient transport, coordinating with tourism stakeholders."})
process['stakeholders'].append({"stakeholder": "National Parks and Wildlife Conservancies", "role": "Key attractions for wildlife tourism; managed by KWS and other entities", "responsibilities": "(INFERRED) Conserving wildlife, providing memorable safari experiences, ensuring visitor safety."})
process['stakeholders'].append({"stakeholder": "Local Communities", "role": "Benefit from community-based tourism initiatives and employment opportunities", "responsibilities": "(INFERRED) Engaging in tourism activities, preserving cultural heritage, welcoming visitors."})
process['stakeholders'].append({"stakeholder": "Ministry of Tourism, Wildlife and Heritage", "role": "Parent Ministry providing policy direction and oversight", "responsibilities": "(INFERRED) Formulating tourism policies, allocating resources, regulating the sector."})
process['stakeholders'].append({"stakeholder": "Kenya Association of Tour Operators (KATO)", "role": "Represents tour operators; partners with KTB on marketing initiatives", "responsibilities": "(INFERRED) Advocating for industry interests, ensuring ethical practices, collaborating on destination promotion."})
process['stakeholders'].append({"stakeholder": "Kenya Coast Tourist Association (KCTA)", "role": "Promotes tourism in the coastal region; partners with KTB", "responsibilities": "(INFERRED) Marketing coastal attractions, collaborating on regional tourism development."})
process['stakeholders'].append({"stakeholder": "Other Tourism Associations", "role": "Various industry bodies representing specific tourism sub-sectors", "responsibilities": "(INFERRED) Promoting niche tourism, collaborating on sector-specific marketing."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical support for tourism development and marketing", "responsibilities": "(INFERRED) Funding tourism projects, sharing expertise in destination management."})

process['as_is_narrative'] = "(INFERRED) KTB's operations are centered around comprehensive destination marketing. This includes developing and executing multi-channel marketing campaigns across digital platforms, social media, print, and broadcast media, targeting key source markets internationally and domestically. KTB actively participates in major international travel fairs, exhibitions, and roadshows to engage with travel trade partners and consumers. It organizes familiarization trips for international media and travel agents to showcase Kenya's diverse tourism products, from wildlife safaris to beach holidays and cultural experiences. The Board conducts ongoing market research and intelligence gathering to identify emerging trends, new niche markets, and potential product development opportunities. KTB collaborates extensively with various tourism stakeholders, including tour operators, hoteliers, airlines, and conservation organizations, to develop compelling promotional packages and ensure a consistent destination message. Furthermore, KTB continuously monitors and evaluates the effectiveness of its marketing strategies, adapting its approaches to ensure Kenya remains a competitive and attractive global tourist destination."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.ktb.go.ke/",
    "https://wordpress.com/", # Provided context
    "https://saraka.info/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixty-fifth process enriched and combined_data.json updated.")
