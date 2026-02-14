
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the sixty-ninth process (index 68)
process = data['processes'][68]

# Populate fields
process['executive_summary'] = "The Micro and Small Enterprises Authority (MSEA) is a state corporation established in 2013 under the Micro and Small Enterprises Act, 2012 (No. 55 of 2012). Its primary mandate is to promote, develop, and regulate Micro and Small Enterprises (MSEs) across Kenya. MSEA aims to foster the growth of MSEs, enhance their competitiveness, facilitate access to critical resources like finance and markets, and integrate them into the formal economy, thereby contributing significantly to job creation, wealth generation, and overall economic development in the country."
process['process_overview']['process_objective'] = "To formulate, coordinate, and implement policies and programs that foster the growth and development of MSEs; to facilitate access to credit, financing options, and start-up grants for micro and small businesses; to provide capacity building and entrepreneurial training to enhance skills among MSE owners; to offer business development services and advisory support; to establish and enforce regulations that govern the operation of MSEs; to conduct research and gather data to inform policy decisions; to create market linkages and access for MSE products and services; to promote innovation, product development, and technology transfer within the MSE sector; to ensure the inclusion and empowerment of youth, women, and persons with disabilities in MSE activities; and to mobilize resources and facilitate the formalization and registration of MSEs."
process['process_overview']['policy_legal_context'].append("Established in 2013 under the Micro and Small Enterprises Act, 2012 (No. 55 of 2012), which provides the legal framework for its mandate, functions, and the development of the MSE sector. MSEA operates under the relevant government ministry (e.g., Ministry of Industrialization, Trade and Enterprise Development) and aligns its activities with national development strategies such as Vision 2030, focusing on enterprise development, economic empowerment, and poverty reduction.")
process['stakeholders'].append({"stakeholder": "Micro and Small Entrepreneurs / Businesses", "role": "Primary beneficiaries and target group for MSEA's support and regulatory frameworks", "responsibilities": "(INFERRED) Establishing and running businesses, complying with regulations, seeking support for growth."})
process['stakeholders'].append({"stakeholder": "Youth, Women, and Persons with Disabilities (as specific target groups)", "role": "Specific demographic groups whose inclusion and empowerment in the MSE sector is prioritized", "responsibilities": "(INFERRED) Participating in MSE programs, utilizing available support, contributing to inclusive growth."})
process['stakeholders'].append({"stakeholder": "Financial Institutions (Banks, Microfinance Institutions)", "role": "Partners in providing access to finance, credit, and other financial services to MSEs", "responsibilities": "(INFERRED) Offering tailored financial products, collaborating on financial literacy initiatives."})
process['stakeholders'].append({"stakeholder": "Government Ministries and Departments (e.g., Trade, Finance, Planning)", "role": "Collaborators in policy formulation, resource allocation, and program implementation for MSEs", "responsibilities": "(INFERRED) Aligning policies, providing sector-specific support, coordinating initiatives."})
process['stakeholders'].append({"stakeholder": "County Governments", "role": "Partners in local MSE development and implementation of MSE programs at the county level", "responsibilities": "(INFERRED) Supporting local MSEs, providing business environments, facilitating access to resources."})
process['stakeholders'].append({"stakeholder": "Business Development Service Providers", "role": "Offer advisory, training, and mentorship services to MSEs", "responsibilities": "(INFERRED) Delivering quality services, collaborating with MSEA on capacity building."})
process['stakeholders'].append({"stakeholder": "Training Institutions (TVETs, Universities)", "role": "Provide entrepreneurial and technical skills training relevant to MSEs", "responsibilities": "(INFERRED) Developing relevant curricula, offering practical training, equipping entrepreneurs."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Conduct studies and provide data to inform MSEA's policy and program development", "responsibilities": "(INFERRED) Generating market intelligence, identifying MSE trends, advising on best practices."})
process['stakeholders'].append({"stakeholder": "Market Linkage Platforms / Buyers", "role": "Provide avenues for MSE products and services to reach consumers and larger markets", "responsibilities": "(INFERRED) Procuring from MSEs, participating in trade fairs, providing market access."})
process['stakeholders'].append({"stakeholder": "International Development Partners", "role": "Provide financial and technical assistance to support the MSE sector in Kenya", "responsibilities": "(INFERRED) Funding programs, sharing international best practices, capacity building support."})
process['stakeholders'].append({"stakeholder": "Associations of MSEs", "role": "Represent the interests of various MSE sub-sectors; advocate for supportive policies", "responsibilities": "(INFERRED) Lobbying for MSEs, providing feedback to MSEA, facilitating member networking."})

process['as_is_narrative'] = "(INFERRED) MSEA implements its mandate through a comprehensive framework that includes developing strategies for the formalization and growth of MSEs, which often involves public awareness campaigns and simplifying registration processes. It offers and coordinates various training programs focused on business management, financial literacy, and specific technical skills tailored to the needs of different MSE sectors. Through strategic partnerships with financial institutions, MSEA facilitates access to affordable credit, loan guarantees, and startup grants, addressing a major constraint for MSEs. The Authority also provides business advisory and mentorship services to help entrepreneurs develop viable business plans and navigate challenges. MSEA actively conducts market research to identify opportunities, value chains, and challenges facing MSEs, informing targeted interventions. It develops and enforces regulations to ensure a fair and conducive business environment for MSEs. Furthermore, MSEA promotes market access for MSE products and services through organizing trade fairs, exhibitions, and facilitating linkages with larger enterprises and export markets. It also champions innovation and the adoption of relevant technologies within the MSE sector and maintains a robust national database of registered MSEs to enable effective monitoring, evaluation, and policy formulation."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.msea.go.ke/",
    "https://saraka.info/", # Provided context
    "https://ecitizen.go.ke/", # Provided context
    "https://treasury.go.ke/", # Provided context
    "https://un.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Sixty-ninth process enriched and combined_data.json updated.")
