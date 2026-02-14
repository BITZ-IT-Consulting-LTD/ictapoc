
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fortieth process (index 39)
process = data['processes'][39]

# Populate fields
process['executive_summary'] = "The Athi Water Works Development Agency (AWWDA) is a Kenyan state corporation under the Ministry of Water, Sanitation & Irrigation. Established under the Water Act 2016, it is responsible for the development, maintenance, and management of water and sewerage infrastructure in Nairobi, Kiambu, and Murang'a Counties, playing a crucial role in providing bulk water and sanitation services."
process['process_overview']['process_objective'] = "To develop, maintain, and manage national public waterworks and sanitation infrastructure; provide bulk water services; offer technical services and build capacity for County Governments and Water Service Providers (WSPs); and support the Cabinet Secretary in their functions under the Water Act 2016, ensuring reliable and sustainable water and sanitation services within its area of jurisdiction."
process['process_overview']['policy_legal_context'].append("Established under the Water Act 2016, which provides the foundational legal framework for its mandate and functions. Operates as one of nine Water Works Development Agencies under the Ministry of Water, Sanitation & Irrigation.")
process['stakeholders'].append({"stakeholder": "Ministry of Water, Sanitation & Irrigation", "role": "Parent Ministry providing policy direction and oversight", "responsibilities": "(INFERRED) Formulating national water policies, strategic guidance, resource allocation."})
process['stakeholders'].append({"stakeholder": "County Governments (Nairobi, Kiambu, Murang'a)", "role": "Governing bodies in AWWDA's area of operation; recipients of technical support", "responsibilities": "(INFERRED) Collaborating on water and sanitation projects, managing county water resources."})
process['stakeholders'].append({"stakeholder": "Water Service Providers (WSPs)", "role": "Entities appointed and overseen by AWWDA for water and sewerage service delivery", "responsibilities": "(INFERRED) Providing water/sewerage services, monitoring water quality, ensuring efficient maintenance."})
process['stakeholders'].append({"stakeholder": "Local Communities/Citizens", "role": "Beneficiaries of improved water and sanitation services", "responsibilities": "(INFERRED) Conserving water, reporting service issues, paying for water services."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Organizations providing financial and technical assistance for water and sanitation projects", "responsibilities": "(INFERRED) Funding infrastructure development, technical expertise, capacity building."})

process['as_is_narrative'] = "(INFERRED) AWWDA operates by planning, designing, and constructing water and sewerage infrastructure projects across Nairobi, Kiambu, and Murang'a Counties. It manages existing waterworks, provides bulk water to Water Service Providers (WSPs), and monitors their performance to ensure efficient and quality service delivery. Additionally, it offers technical assistance and capacity building to county governments and WSPs and acts as a custodian of water and sewerage assets within its jurisdiction."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://awwda.go.ke/",
    "https://geospatialworld.net/", # Provided context
    "https://parliament.go.ke/", # Provided context
    "https://developmentaid.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fortieth process enriched and combined_data.json updated.")
