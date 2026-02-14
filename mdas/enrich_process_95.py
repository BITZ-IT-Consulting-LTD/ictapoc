
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninety-sixth process (index 95)
process = data['processes'][95]

# Populate fields
process['executive_summary'] = "Bomas of Kenya is a cultural center established in 1971 by the Kenyan government, operating under the Bomas of Kenya Act, 2004. Its primary mandate is to promote and preserve Kenya's rich and diverse cultural heritage, foster national unity through cultural exchange, and act as the only national body with a specific mandate in cultural tourism. Bomas of Kenya serves as a vibrant platform for showcasing the country's traditions, hosting various national events, cultural performances, and exhibitions, thereby contributing significantly to cultural education, tourism, and national identity."
process['process_overview']['process_objective'] = "To promote and preserve Kenya's diverse cultural heritage; to host national celebrations, conferences, and forums that foster national unity and identity; to organize traditional music, dance, and theatrical performances showcasing over 50 dances from different ethnic communities; to provide a platform for cultural exhibitions that highlight various Kenyan communities and their traditions, including displays of cultural artifacts and traditional homesteads (bomas); to facilitate cultural education programs and workshops for schools and communities to enhance awareness of Kenya's heritage; to act as a tourist attraction, drawing both local and international visitors to experience Kenyan culture; to collaborate with local and international organizations to promote cultural exchange and development initiatives; to train and empower artists and cultural practitioners; to conduct research on cultural practices and traditions; and to provide state-of-the-art facilities for various events, including corporate functions, weddings, and conferences."
process['process_overview']['policy_legal_context'].append("Established in 1971 as a subsidiary of the Tourist Finance Corporation (TFC), Bomas of Kenya now operates under the Bomas of Kenya Act, 2004 (Cap. 347, Laws of Kenya), which provides the legal framework for its mandate and functions. It operates under the Ministry of Tourism, Wildlife and Heritage (or the relevant government ministry responsible for culture and national heritage) and is crucial for implementing national cultural policies, promoting cultural tourism, and preserving national identity and unity through its diverse programs and activities.")
process['stakeholders'].append({"stakeholder": "Kenyan Public (especially youth and children)", "role": "Primary audience for cultural education and performances; beneficiaries of heritage preservation and national unity efforts", "responsibilities": "(INFERRED) Attending cultural events, participating in cultural education, respecting national heritage."})
process['stakeholders'].append({"stakeholder": "Local and International Tourists / Visitors", "role": "Consumers of cultural tourism products; contribute revenue for Bomas's operations and cultural preservation", "responsibilities": "(INFERRED) Visiting Bomas, experiencing cultural performances, supporting cultural tourism."})
process['stakeholders'].append({"stakeholder": "Artists / Cultural Practitioners (dancers, musicians, artisans)", "role": "Performers and creators who showcase Kenya's cultural heritage; beneficiaries of Bomas's platforms and training", "responsibilities": "(INFERRED) Performing, creating cultural artifacts, participating in training programs."})
process['stakeholders'].append({"stakeholder": "Ethnic Communities of Kenya", "role": "Sources of diverse cultural heritage; their traditions are represented and preserved by Bomas", "responsibilities": "(INFERRED) Sharing cultural traditions, contributing to cultural diversity, collaborating on cultural events."})
process['stakeholders'].append({"stakeholder": "Ministry of Tourism, Wildlife and Heritage", "role": "Parent Ministry providing policy direction, funding, and oversight to Bomas", "responsibilities": "(INFERRED) Formulating cultural policies, allocating resources, strategic guidance for cultural tourism."})
process['stakeholders'].append({"stakeholder": "Kenya Tourism Board (KTB)", "role": "Markets Kenya as a tourism destination, including cultural attractions like Bomas of Kenya", "responsibilities": "(INFERRED) Promoting cultural tourism, collaborating on marketing campaigns, driving visitor numbers."})
process['stakeholders'].append({"stakeholder": "Educational Institutions (schools, colleges)", "role": "Partners in cultural education and outreach programs; utilize Bomas for educational visits", "responsibilities": "(INFERRED) Organizing educational trips, integrating cultural education into curricula."})
process['stakeholders'].append({"stakeholder": "Cultural Organizations / Institutions", "role": "Collaborators in promoting Kenyan culture and arts; partner on exhibitions and events", "responsibilities": "(INFERRED) Showcasing cultural talent, collaborating on joint programs, fostering cultural exchange."})
process['stakeholders'].append({"stakeholder": "Event Organizers", "role": "Utilize Bomas's facilities for hosting various events, conferences, and festivals", "responsibilities": "(INFERRED) Organizing events, adhering to Bomas's regulations, promoting cultural events."})
process['stakeholders'].append({"stakeholder": "Researchers / Academics", "role": "Conduct studies on cultural practices and traditions; may utilize Bomas's resources and expertise", "responsibilities": "(INFERRED) Conducting cultural research, providing expert insights, collaborating on documentation."})
process['stakeholders'].append({"stakeholder": "Tour Operators / Travel Agencies", "role": "Package and promote Bomas of Kenya as part of their tourism offerings", "responsibilities": "(INFERRED) Including Bomas in tour itineraries, promoting cultural experiences, bringing tourists."})

process['as_is_narrative'] = "(INFERRED) Bomas of Kenya actively implements its mandate by daily organizing and staging a vibrant array of traditional music, dance, and theatrical performances that represent the rich and diverse cultural heritage of various Kenyan ethnic groups, providing a captivating experience for audiences. It curates and maintains both permanent and temporary cultural exhibitions, featuring authentic artifacts, traditional homesteads (bomas) from different communities, and displays of historical and cultural practices, all designed to educate and immerse visitors in Kenya's cultural tapestry. The institution conducts comprehensive cultural education programs and outreach activities tailored for schools, colleges, and the general public, aiming to raise awareness and foster appreciation for Kenya's cultural diversity and national identity. Bomas of Kenya serves as a prestigious venue for hosting national events, conferences, forums, and cultural festivals, thereby fostering national unity and providing a platform for dialogue and celebration. It actively markets itself as a unique cultural tourism destination, attracting a significant number of both local and international visitors, thereby generating essential revenue through entrance fees, event hosting, and sales of cultural merchandise. The organization also engages in ongoing research to document and revitalize disappearing cultural practices and traditions, ensuring their continuity. Collaborations are key, with Bomas working closely with various stakeholders, including local communities, artists, tourism players, and government agencies, to promote and sustain cultural tourism, ensuring that Kenya's rich cultural heritage is preserved, celebrated, and accessible to all."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.bomasofkenya.co.ke/", # Official website
    "https://lakenakurukenya.com/", # Provided context
    "https://citysightseeing.co.ke/", # Provided context
    "https://bomasofkenya.go.ke/", # Provided context
    "https://wikipedia.org/", # Provided context
    "https://kenyawildlifetours.com/", # Provided context
    "https://saraka.info/", # Provided context
    "https://africanspicesafaris.com/", # Provided context
    "https://safari-center.com/", # Provided context
    "https://memphistours.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninety-sixth process enriched and combined_data.json updated.")
