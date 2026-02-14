
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the twenty-first process (index 20)
process = data['processes'][20]

# Populate fields
process['executive_summary'] = "The National Environment Management Authority (NEMA) is Kenya's principal government agency responsible for environmental management and policy. Established under EMCA 1999, it ensures the sustainable management of the environment through general supervision, coordination of environmental matters, and implementation of all environmental policies to maintain standards and regulations across Kenya."
process['process_overview']['process_objective'] = "To exercise general supervision and coordination over all matters relating to the environment, implement environmental policies, enforce environmental laws and regulations, promote public environmental awareness, and ensure sustainable environmental management and conservation across Kenya."
process['process_overview']['policy_legal_context'].append("Established under the Environmental Management and Coordination Act (EMCA) of 1999, which provides the foundational legal framework for its mandate and functions. Operates under the Ministry of Environment and Forestry.")
process['stakeholders'].append({"stakeholder": "Kenyan Citizens", "role": "Beneficiaries of a clean and healthy environment; participants in environmental conservation", "responsibilities": "(INFERRED) Practicing sustainable habits, reporting environmental violations."})
process['stakeholders'].append({"stakeholder": "Industries", "role": "Subjects of environmental regulations, licensing, and compliance enforcement", "responsibilities": "(INFERRED) Adhering to environmental standards, conducting EIAs, obtaining necessary permits."})
process['stakeholders'].append({"stakeholder": "Government Ministries, Departments, and Agencies", "role": "Entities coordinating environmental management activities; subjects of NEMA's oversight", "responsibilities": "(INFERRED) Integrating environmental considerations into their programs, collaborating on policy implementation."})
process['stakeholders'].append({"stakeholder": "Environmental Conservation Groups", "role": "Partners in promoting environmental awareness and sustainable practices", "responsibilities": "(INFERRED) Advocating for environmental protection, engaging in community education."})
process['stakeholders'].append({"stakeholder": "International Environmental Bodies", "role": "Collaborators on international environmental conventions and agreements", "responsibilities": "(INFERRED) Harmonizing national policies with global standards, supporting environmental projects."})

process['as_is_narrative'] = "(INFERRED) NEMA's operations involve enforcing environmental laws, reviewing and approving Environmental Impact Assessments (EIAs), monitoring environmental quality, issuing licenses and permits for environmentally significant activities, promoting public awareness and education, advising the government on environmental policy, conducting research, and coordinating national and international environmental management efforts."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official website) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://nema.go.ke/",
    "https://en.wikipedia.org/wiki/National_Environment_Management_Authority_(Kenya)", # Provided context
    "https://investkenya.go.ke/", # Provided context
    "https://greenclimate.fund/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Twenty-first process enriched and combined_data.json updated.")
