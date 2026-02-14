
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventy-sixth process (index 75)
process = data['processes'][75]

# Populate fields
process['executive_summary'] = "The National Museums of Kenya (NMK) is a state corporation established by the Museums and Heritage Act 2006. Its primary mandate is to collect, preserve, study, document, and present Kenya's past and present cultural and natural heritage. NMK manages numerous regional museums, sites, and monuments of national and international importance, housing priceless collections of Kenya's living cultural and natural heritage. Through these efforts, NMK aims to enhance knowledge, appreciation, respect, and sustainable utilization of these resources for the benefit of Kenya and the world, contributing significantly to national development and tourism."
process['process_overview']['process_objective'] = "To collect, preserve, study, document, and present Kenya's past and present cultural and natural heritage; to manage numerous Regional Museums, Sites, and Monuments of national and international importance; to contribute to national development by responding to the growing needs of society through heritage conservation; to safeguard and conserve Kenya's cultural and natural heritage through continuous research and documentation; to promote public awareness and understanding of Kenya's heritage through educational programs, exhibitions, and community outreach; to develop and maintain engaging exhibits that showcase the nation's artifacts, artworks, and historical items; to oversee the operations and management of various museums and heritage sites across the country; to provide expert advice to the government and other stakeholders on matters related to heritage conservation and management; to facilitate cultural exchanges and collaborations with national and international museums and institutions; to enhance the skills and capabilities of museum staff and other stakeholders involved in heritage conservation; to encourage tourism to Kenya's cultural and natural heritage sites to foster economic development; and to contribute to the development of national policies related to heritage management, cultural preservation, and museum practices."
process['process_overview']['policy_legal_context'].append("Established by the Museums and Heritage Act 2006, which provides the legal framework for its mandate and functions. NMK operates under the Ministry of Tourism, Wildlife and Heritage (or the relevant government ministry responsible for culture, heritage, and national patrimony) and is central to implementing national heritage policies, safeguarding cultural property, and adhering to international conventions on cultural and natural heritage protection.")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens (General Public)", "role": "Primary audience for NMK's educational and exhibition programs; beneficiaries of heritage preservation", "responsibilities": "(INFERRED) Visiting museums, respecting heritage sites, participating in cultural preservation."})
process['stakeholders'].append({"stakeholder": "Researchers / Academics (Local and International)", "role": "Utilize NMK's collections and research for scientific study and knowledge creation", "responsibilities": "(INFERRED) Conducting research ethically, sharing findings, collaborating on heritage studies."})
process['stakeholders'].append({"stakeholder": "Educational Institutions (Schools, Universities)", "role": "Partners in heritage education and outreach programs", "responsibilities": "(INFERRED) Integrating heritage into curricula, organizing educational visits, collaborating on research."})
process['stakeholders'].append({"stakeholder": "Tourists / Visitors", "role": "Consumers of heritage tourism products; contribute revenue for conservation", "responsibilities": "(INFERRED) Visiting sites, respecting cultural norms, supporting heritage conservation through entry fees."})
process['stakeholders'].append({"stakeholder": "Local Communities (especially those near heritage sites)", "role": "Custodians of local heritage; often involved in site management and benefit-sharing", "responsibilities": "(INFERRED) Protecting local heritage, participating in community cultural activities, sharing traditional knowledge."})
process['stakeholders'].append({"stakeholder": "Ministry of Tourism, Wildlife and Heritage", "role": "Parent Ministry providing policy direction, funding, and oversight to NMK", "responsibilities": "(INFERRED) Formulating heritage policies, allocating resources, strategic guidance."})
process['stakeholders'].append({"stakeholder": "Kenya Tourism Board (KTB)", "role": "Markets Kenya as a tourism destination, including its cultural and natural heritage sites", "responsibilities": "(INFERRED) Promoting heritage tourism, collaborating on marketing campaigns."})
process['stakeholders'].append({"stakeholder": "Cultural & Arts Organizations", "role": "Partners in promoting Kenyan culture and arts; collaborate on exhibitions and events", "responsibilities": "(INFERRED) Showcasing cultural talent, collaborating on joint programs."})
process['stakeholders'].append({"stakeholder": "Conservation Organizations", "role": "Partners in preserving natural heritage sites and biodiversity", "responsibilities": "(INFERRED) Funding conservation projects, advocating for environmental protection."})
process['stakeholders'].append({"stakeholder": "International Museum / Heritage Bodies (e.g., ICOM, UNESCO)", "role": "Provide international standards, best practices, and collaborative opportunities in heritage management", "responsibilities": "(INFERRED) Setting global heritage norms, supporting capacity building, facilitating international cooperation."})
process['stakeholders'].append({"stakeholder": "Donors / Development Partners", "role": "Provide financial and technical assistance to support NMK's programs and projects", "responsibilities": "(INFERRED) Funding heritage conservation, supporting research and exhibition development."})

process['as_is_narrative'] = "(INFERRED) The National Museums of Kenya (NMK) actively fulfills its mandate through extensive fieldwork, including archaeological and paleontological excavations, aimed at discovering and understanding Kenya's deep history and biodiversity. It collects a vast array of artifacts, specimens, and historical documents, which form the core of its national collections, ensuring their meticulous preservation through modern conservation techniques. Scientific research is integral to NMK's operations, with experts across various disciplines (e.g., anthropology, zoology, botany, geology) studying these collections and conducting fieldwork to deepen knowledge about Kenya's natural and cultural heritage. NMK curates and develops engaging exhibitions for its national and regional museums, making heritage accessible and understandable to diverse audiences. It runs robust educational programs for schools, public lectures, and community outreach activities to promote public awareness and appreciation of heritage. The Authority is responsible for maintaining and safeguarding numerous national monuments and sites, ensuring their structural integrity and historical authenticity. NMK is also increasingly digitizing its collections, making them accessible to a global audience. It collaborates with other cultural institutions, both nationally and internationally, for exhibitions, research, and cultural exchange. Furthermore, NMK provides crucial expert advice to the government on policy matters related to heritage protection, legislation, and cultural resource management, ensuring that heritage considerations are integrated into national planning."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official websites and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.museums.or.ke/", # Official website
    "https://www.nmk.go.ke/", # Official website
    "https://ecitizen.go.ke/", # Provided context
    "https://saraka.info/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventy-sixth process enriched and combined_data.json updated.")
