
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninety-eighth process (index 97)
process = data['processes'][97]

# Populate fields
process['executive_summary'] = "The Communications Authority of Kenya (CA) is the independent regulatory agency for the Information, Communications and Technology (ICT) industry in Kenya, established in 1999 by the Kenya Information and Communications Act, 1998. Its mandate encompasses licensing, spectrum management, market development, consumer protection, and cybersecurity. The CA aims to ensure a vibrant, accessible, secure, and well-regulated ICT sector that fosters innovation, economic growth, and social development, while upholding consumer rights and promoting fair competition."
process['process_overview']['process_objective'] = "To license all systems and services in the communications industry, including telecommunications, postal, courier, and broadcasting services; to manage the country's frequency spectrum and numbering resources efficiently; to facilitate the development of e-commerce and the overall information and communications sectors, including broadcasting, cybersecurity, multimedia, telecommunications, and postal/courier services; to type approve and accept communications equipment for use in the country; to protect consumer rights within the communications environment; to manage competition within the sector to ensure a level playing field for all players; to regulate retail and wholesale tariffs for communications services; to administer the Universal Service Fund (USF) to facilitate widespread access to communications services by all in Kenya; to promote capacity building and innovation in ICT services; and to facilitate the development and management of a national cybersecurity framework."
process['process_overview']['policy_legal_context'].append("Established in 1999 by the Kenya Information and Communications Act, 1998 (KICA), which provides the comprehensive legal and regulatory framework for the ICT industry in Kenya. The CA operates under the Ministry of Information, Communications and the Digital Economy (or the relevant government ministry responsible for ICT) and is guided by national ICT policies, constitutional provisions for freedom of expression and access to information, and international best practices and conventions for communications regulation.")
process['stakeholders'].append({"stakeholder": "Telecommunications Service Providers (Safaricom, Airtel, Telkom)", "role": "Licensed entities offering telecommunication services; regulated by CA", "responsibilities": "(INFERRED) Complying with license conditions, providing quality services, paying fees/taxes."})
process['stakeholders'].append({"stakeholder": "Broadcasters (TV, Radio stations)", "role": "Licensed entities offering broadcasting services; regulated by CA", "responsibilities": "(INFERRED) Complying with license conditions, adhering to content standards, paying fees/taxes."})
process['stakeholders'].append({"stakeholder": "Internet Service Providers (ISPs)", "role": "Licensed entities offering internet services; regulated by CA", "responsibilities": "(INFERRED) Complying with license conditions, providing reliable internet access, paying fees/taxes."})
process['stakeholders'].append({"stakeholder": "Postal and Courier Service Providers", "role": "Licensed entities offering postal and courier services; regulated by CA", "responsibilities": "(INFERRED) Complying with license conditions, providing efficient services, paying fees/taxes."})
process['stakeholders'].append({"stakeholder": "Consumers / Subscribers of Communications Services", "role": "End-users of telecommunications, broadcasting, and internet services; their rights are protected by CA", "responsibilities": "(INFERRED) Utilizing services responsibly, reporting grievances, understanding consumer rights."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (Ministry of Information, Communications and the Digital Economy)", "role": "Parent Ministry providing policy direction, funding, and oversight to CA", "responsibilities": "(INFERRED) Formulating ICT policies, allocating resources, strategic guidance for the digital economy."})
process['stakeholders'].append({"stakeholder": "Cybersecurity Agencies (e.g., National Computer and Cybercrimes Coordination Committee - NC4)", "role": "Collaborators in developing and managing national cybersecurity frameworks and combating cybercrime", "responsibilities": "(INFERRED) Collaborating on cybersecurity, sharing threat intelligence, enforcing cybercrime laws."})
process['stakeholders'].append({"stakeholder": "Content Creators", "role": "Develop content for broadcasting and online platforms; affected by content regulations", "responsibilities": "(INFERRED) Creating content, adhering to broadcasting standards, respecting intellectual property."})
process['stakeholders'].append({"stakeholder": "Equipment Vendors", "role": "Supply communications equipment; their products require CA type approval", "responsibilities": "(INFERRED) Supplying type-approved equipment, ensuring quality and compatibility."})
process['stakeholders'].append({"stakeholder": "International Telecommunication Union (ITU)", "role": "Specialized agency of the UN; sets international telecommunications standards; CA aligns with ITU recommendations", "responsibilities": "(INFERRED) Setting global telecommunications standards, facilitating international cooperation."})
process['stakeholders'].append({"stakeholder": "Mobile Network Operators (MNOs)", "role": "Specific type of telecommunications service provider; heavily regulated by CA", "responsibilities": "(INFERRED) Providing mobile services, managing network infrastructure, complying with CA regulations."})
process['stakeholders'].append({"stakeholder": "Media Council of Kenya", "role": "Regulates media content and journalists; collaborates with CA on broadcasting content standards", "responsibilities": "(INFERRED) Setting media ethics, promoting responsible journalism, collaborating on content regulation."})

process['as_is_narrative'] = "(INFERRED) The Communications Authority of Kenya (CA) exercises its mandate through a dynamic regulatory framework that adapts to the rapidly evolving ICT landscape. It initiates and processes applications for various licenses, covering telecommunications, broadcasting (both terrestrial and online), postal, and courier services, and ensures ongoing compliance with license terms through regular monitoring. A core function involves the intricate management of national frequency spectrum and numbering resources, ensuring their efficient allocation and utilization. CA plays a proactive role in market development by facilitating the growth of e-commerce, promoting infrastructure rollout, and fostering innovation across all ICT sub-sectors. It conducts rigorous type approval and acceptance testing for all communications equipment to be used in Kenya, ensuring safety, compatibility, and adherence to technical standards. Consumer protection is paramount, with CA developing guidelines, mediating disputes between consumers and service providers, and running awareness campaigns. The Authority actively monitors market competition to prevent monopolies and anti-competitive practices, intervening where necessary. It administers the Universal Service Fund (USF) to finance projects aimed at expanding access to communications services in underserved and unserved areas. Furthermore, CA is at the forefront of developing and implementing Kenya's national cybersecurity framework, collaborating closely with law enforcement and other agencies to combat cybercrime and ensure a secure online environment. Through continuous research, consultation, and policy advice to the government, CA strives to ensure that Kenya's ICT sector remains robust, competitive, inclusive, and contributes effectively to the digital economy."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.ca.go.ke/", # Official website
    "https://wikipedia.org/", # Provided context
    "https://cybilportal.org/", # Provided context
    "https://afro.co.ke/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninety-eighth process enriched and combined_data.json updated.")
