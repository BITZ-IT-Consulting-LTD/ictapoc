
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the forty-sixth process (index 45)
process = data['processes'][45]

# Populate fields
process['executive_summary'] = "The Kenya Airports Authority (KAA) is an autonomous government-owned enterprise established in 1991 under the KAA Act, Chapter 395 of the Laws of Kenya. Its primary mandate is to provide facilitative infrastructure for aviation services, administering, controlling, and managing aerodromes, and undertaking the development and maintenance of airports and airstrips throughout Kenya."
process['process_overview']['process_objective'] = "To administer, control, and manage aerodromes throughout Kenya; provide and maintain essential facilities for the efficient operation of aircraft; offer rescue and firefighting equipment and services; undertake the construction, operation, and maintenance of aerodromes; and ensure the safety, sustainability, and efficiency of civil aviation operations in compliance with relevant acts."
process['process_overview']['policy_legal_context'].append("Established in 1991 under the Kenya Airports Authority Act, Chapter 395 of the Laws of Kenya. Operates in compliance with the Civil Aviation Act and other international aviation standards and regulations.")
process['stakeholders'].append({"stakeholder": "Airlines", "role": "Primary users of airport facilities for passenger and cargo transport", "responsibilities": "(INFERRED) Adhering to airport regulations, contributing to airport revenue through fees."})
process['stakeholders'].append({"stakeholder": "Passengers", "role": "Users of airport services and facilities for travel", "responsibilities": "(INFERRED) Complying with security procedures, respecting airport rules."})
process['stakeholders'].append({"stakeholder": "Cargo Operators", "role": "Users of airport facilities for air cargo logistics", "responsibilities": "(INFERRED) Adhering to cargo handling regulations, utilizing cargo facilities efficiently."})
process['stakeholders'].append({"stakeholder": "Aviation Service Providers (e.g., ground handlers, fuel suppliers)", "role": "Entities providing various essential services at airports", "responsibilities": "(INFERRED) Providing quality services, complying with operational standards."})
process['stakeholders'].append({"stakeholder": "Kenya Civil Aviation Authority (KCAA)", "role": "Regulatory body for civil aviation in Kenya", "responsibilities": "(INFERRED) Overseeing aviation safety and security, licensing, setting standards."})
process['stakeholders'].append({"stakeholder": "Government (Ministry of Transport)", "role": "Oversight ministry providing policy direction", "responsibilities": "(INFERRED) Policy formulation, strategic guidance, resource allocation for KAA."})
process['stakeholders'].append({"stakeholder": "Airport Businesses (e.g., concessions, shops)", "role": "Commercial entities operating within airport premises", "responsibilities": "(INFERRED) Providing services to passengers, contributing to airport revenue."})
process['stakeholders'].append({"stakeholder": "Security Agencies", "role": "Partners in ensuring airport security and safety", "responsibilities": "(INFERRED) Enforcing security protocols, responding to incidents."})
process['stakeholders'].append({"stakeholder": "International Aviation Organizations (e.g., ICAO)", "role": "Organizations setting global aviation standards and recommendations", "responsibilities": "(INFERRED) Providing guidance, ensuring compliance with international best practices."})

process['as_is_narrative'] = "(INFERRED) KAA manages and operates nine civilian airports and airstrips across Kenya, including major international hubs like Jomo Kenyatta International Airport. Its operations encompass planning, designing, and constructing airport infrastructure, maintaining runways, terminals, and air navigation facilities, providing essential safety services such as rescue and firefighting, ensuring compliance with national and international aviation safety and security standards, and approving the establishment and operation of private airstrips. KAA also develops commercial activities within its airports to generate revenue and enhance the passenger experience."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://devex.com/", # Provided context
    "https://wikipedia.org/", # Provided context
    "https://centreforaviation.com/", # Provided context
    "https://issuu.com/", # Provided context
    "https://prezi.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Forty-sixth process enriched and combined_data.json updated.")
