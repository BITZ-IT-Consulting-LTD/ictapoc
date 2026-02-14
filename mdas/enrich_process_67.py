
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixty-eighth process (index 67)
process = data['processes'][67]

# Populate fields
process['executive_summary'] = "The Kenya Wildlife Service (KWS) is a state corporation responsible for the conservation and management of Kenya's wildlife and its habitats. Established under the Wildlife Conservation and Management Act of 2013, KWS is mandated to protect wildlife and visitors within national parks and reserves, conduct research, engage communities, enforce wildlife laws, and mitigate human-wildlife conflicts. Its vision is to ensure thriving wildlife and healthy habitats for all, forever, contributing significantly to Kenya's natural heritage and tourism sector."
process['process_overview']['process_objective'] = "To sustainably conserve Kenya's wildlife heritage and its habitats for the well-being of nature and people; to provide security for both wildlife and visitors within national parks, wildlife conservation areas, and sanctuaries; to effectively protect and manage national parks, reserves, sanctuaries, and marine parks; to conduct and coordinate research activities in wildlife conservation and management; to promote and undertake extension service programs to enhance wildlife conservation, education, and training; to enforce the provisions of the Wildlife Conservation and Management Act (WCMA, 2013); to undertake wildlife rescue and rehabilitation of orphaned or confiscated wildlife; to mitigate human-wildlife conflicts; to foster partnerships and collaboration with local and international stakeholders; and to contribute to national security through wildlife protection."
process['process_overview']['policy_legal_context'].append("Established under the Wildlife Conservation and Management Act of 2013, which provides the comprehensive legal framework for wildlife conservation and management in Kenya. KWS operates under the Ministry of Tourism, Wildlife and Heritage, and its functions are central to achieving national biodiversity conservation goals, supporting the vital tourism sector, and contributing to sustainable development.")
process['stakeholders'].append({"stakeholder": "Wildlife (as beneficiaries)", "role": "Primary subjects of conservation efforts; integral to Kenya's natural heritage and tourism", "responsibilities": "(INFERRED) Contributing to ecosystem health, serving as tourist attractions."})
process['stakeholders'].append({"stakeholder": "Local Communities (living adjacent to wildlife areas)", "role": "Directly affected by wildlife activities; partners in conservation and beneficiaries of wildlife resources", "responsibilities": "(INFERRED) Co-existing with wildlife, participating in community conservation, benefiting from revenue sharing."})
process['stakeholders'].append({"stakeholder": "Tourists / Visitors", "role": "Consumers of wildlife-based tourism products; contribute revenue to conservation", "responsibilities": "(INFERRED) Adhering to park rules, supporting ecotourism, respecting wildlife and environment."})
process['stakeholders'].append({"stakeholder": "Tour Operators / Safari Companies", "role": "Organize and facilitate wildlife tourism experiences; partners in promoting Kenya", "responsibilities": "(INFERRED) Marketing Kenya's wildlife, providing quality tourist services, adhering to regulations."})
process['stakeholders'].append({"stakeholder": "Conservation Organizations (Local and International)", "role": "Provide technical, financial, and advocacy support for wildlife conservation", "responsibilities": "(INFERRED) Funding projects, conducting research, advocating for policy changes."})
process['stakeholders'].append({"stakeholder": "Kenya Police Service", "role": "Collaborates in law enforcement and security operations, especially against wildlife crime", "responsibilities": "(INFERRED) Assisting KWS in anti-poaching, providing security in wildlife areas."})
process['stakeholders'].append({"stakeholder": "Ministry of Tourism, Wildlife and Heritage", "role": "Parent Ministry providing policy direction, funding, and oversight for wildlife sector", "responsibilities": "(INFERRED) Formulating wildlife policies, allocating resources, regulating the sector."})
process['stakeholders'].append({"stakeholder": "Kenya Tourism Board (KTB)", "role": "Markets Kenya as a tourism destination, including its wildlife attractions", "responsibilities": "(INFERRED) Promoting wildlife tourism, collaborating on marketing campaigns."})
process['stakeholders'].append({"stakeholder": "Research Institutions / Scientists", "role": "Conduct scientific research to inform KWS's conservation strategies and practices", "responsibilities": "(INFERRED) Generating data, providing expert advice on wildlife management."})
process['stakeholders'].append({"stakeholder": "Donors / Development Partners", "role": "Provide financial and technical assistance for KWS programs and projects", "responsibilities": "(INFERRED) Funding conservation initiatives, sharing expertise."})
process['stakeholders'].append({"stakeholder": "Ranchers / Landowners (in dispersal areas)", "role": "Manage lands critical for wildlife dispersal and migration", "responsibilities": "(INFERRED) Practicing wildlife-friendly land use, collaborating on conservation efforts."})

process['as_is_narrative'] = "(INFERRED) KWS operates through a multi-faceted approach to wildlife conservation. This involves deploying highly trained rangers to conduct patrols, anti-poaching operations, and surveillance within national parks, reserves, and sanctuaries to ensure the security of wildlife and visitors. KWS actively manages habitats through activities such as prescribed burning, water provision, and invasive species control to support biodiversity. Scientific research is a cornerstone of KWS's operations, informing evidence-based conservation strategies, ecological monitoring, and population management. The Service engages extensively with local communities to promote co-existence, address human-wildlife conflict incidents (e.g., through rapid response teams and mitigation measures), and ensure benefit-sharing from wildlife resources. KWS also operates wildlife orphanages and rescue centers for rehabilitation, enforces the Wildlife Conservation and Management Act through arrests and prosecutions of offenders, and collaborates with other security agencies (e.g., police, military) and international partners to combat transnational wildlife crime. Additionally, KWS manages and develops park infrastructure, including roads, airstrips, and visitor facilities, to support both conservation and responsible tourism."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.kws.go.ke/",
    "https://kikosi.co.ke/", # Provided context
    "https://wikipedia.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixty-eighth process enriched and combined_data.json updated.")
