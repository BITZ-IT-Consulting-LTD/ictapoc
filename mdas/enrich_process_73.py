
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the seventy-fourth process (index 73)
process = data['processes'][73]

# Populate fields
process['executive_summary'] = "The National Housing Corporation (NHC) plays a principal role in the implementation of the Kenyan Government's Housing Policies and Programmes. Established as a state corporation, its primary mandate is to promote, develop, and provide affordable housing solutions for all income groups across Kenya. NHC aims to stimulate the building industry, encourage and assist housing research, and facilitate increased access to decent and affordable housing, thereby contributing significantly to national development and improving living standards."
process['process_overview']['process_objective'] = "To promote low-cost housing development across Kenya; to stimulate the building industry by encouraging local production and use of building materials and technologies; to encourage and assist housing research and development; to serve as the government's main agency for channeling public funds for low-cost housing to Local Authorities and County Governments; to provide technical assistance to Local Authorities and County Governments for the design and implementation of their housing schemes; to assist citizens and Local Authorities in constructing affordable housing through various schemes including Tenant Purchase, Outright Sale, Rural and Peri-Urban Housing Loans, and Rental Housing; to undertake direct construction of housing in areas where Local Authorities are unable or unwilling to do so; to promote appropriate and innovative building technologies, such as the manufacturing of EPS panels; and to provide housing loans to eligible individuals and organizations."
process['process_overview']['policy_legal_context'].append("Established by an Act of Parliament (National Housing Act, Cap 117), NHC plays a principal role in implementing the Kenyan Government's Housing Policies and Programmes. It operates under the Ministry of Lands, Public Works, Housing and Urban Development (or the relevant government ministry responsible for housing) and is guided by national housing acts and policies, including those aimed at achieving affordable housing as part of the Big Four Agenda.")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens (especially low-income earners)", "role": "Primary beneficiaries of affordable housing initiatives and housing loan schemes", "responsibilities": "(INFERRED) Seeking affordable housing, repaying loans, maintaining properties."})
process['stakeholders'].append({"stakeholder": "Local Authorities / County Governments", "role": "Partners in housing development and implementation of housing schemes at the local level", "responsibilities": "(INFERRED) Collaborating on housing projects, providing land, implementing urban planning."})
process['stakeholders'].append({"stakeholder": "Private Developers", "role": "Partners in joint venture housing projects and beneficiaries of an stimulated building industry", "responsibilities": "(INFERRED) Engaging in housing construction, adhering to building standards, marketing housing units."})
process['stakeholders'].append({"stakeholder": "Financial Institutions (Banks, Saccos)", "role": "Provide financing for housing projects and mortgage facilities to homebuyers", "responsibilities": "(INFERRED) Offering housing loans, collaborating on affordable housing finance models."})
process['stakeholders'].append({"stakeholder": "Building Material Manufacturers / Suppliers", "role": "Provide materials for NHC projects and the broader building industry", "responsibilities": "(INFERRED) Supplying quality building materials, innovating in affordable materials."})
process['stakeholders'].append({"stakeholder": "Construction Companies", "role": "Undertake construction works for NHC projects and other housing developments", "responsibilities": "(INFERRED) Delivering quality construction, adhering to timelines and budgets."})
process['stakeholders'].append({"stakeholder": "Housing Cooperatives", "role": "Groups of individuals pooling resources to acquire land and construct houses", "responsibilities": "(INFERRED) Mobilizing resources, participating in housing schemes, self-regulating."})
process['stakeholders'].append({"stakeholder": "Ministry of Lands, Public Works, Housing and Urban Development", "role": "Parent Ministry providing policy direction, funding, and oversight to NHC", "responsibilities": "(INFERRED) Formulating national housing policies, allocating resources, strategic guidance."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Conduct research into housing needs, affordable building technologies, and urban planning", "responsibilities": "(INFERRED) Providing data and insights, advising on innovative housing solutions."})
process['stakeholders'].append({"stakeholder": "Development Partners", "role": "Provide financial and technical assistance to support housing programs and capacity building", "responsibilities": "(INFERRED) Funding housing initiatives, sharing expertise in affordable housing."})

process['as_is_narrative'] = "(INFERRED) The National Housing Corporation (NHC) implements its mandate through a diverse range of activities. It conceptualizes, designs, and develops various housing schemes, often targeting specific income groups, from low-cost to middle-income housing. NHC directly undertakes the construction of housing units in strategic urban and peri-urban areas, or forms joint ventures with private developers to leverage resources and expertise. A significant function involves providing technical assistance, including architectural and engineering services, to local authorities and individuals engaged in housing development. NHC facilitates access to housing finance by offering various loan products (e.g., rural and peri-urban housing loans) and working with financial institutions to make mortgages more accessible. It actively researches, develops, and promotes the use of innovative and affordable building technologies, such as Expanded Polystyrene (EPS) panels, to reduce construction costs and accelerate housing delivery. NHC also manages a portfolio of rental housing estates, providing affordable accommodation. Furthermore, NHC engages in policy advocacy, advising the government on housing policy matters and collaborating with stakeholders to create a conducive environment for housing delivery, aligning with national goals of providing affordable housing for all Kenyans."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.nhckenya.go.ke/", # Official website
    "https://abdas.org/", # Provided context
    "https://devex.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Seventy-fourth process enriched and combined_data.json updated.")
