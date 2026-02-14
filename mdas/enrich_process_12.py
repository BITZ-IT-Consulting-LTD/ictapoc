
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the thirteenth process (index 12)
process = data['processes'][12]

# Populate fields
process['executive_summary'] = "The State Department for Technical and Vocational Education and Training (TVET) in Kenya coordinates national skills training and fosters an effectively harmonized TVET system. Its goal is to produce a skilled human resource base with the necessary attitudes and values to contribute to the growth and prosperity of various economic sectors."
process['process_overview']['process_objective'] = "To develop and implement policies and strategies for technical and vocational skills training, oversee the provision and quality of TVET programs, manage TVET institutions, enhance access and relevance, and foster strong linkages with industry to meet labor market needs."
process['process_overview']['policy_legal_context'].append("Mandate primarily derived from The TVET Act 2013. Operates within a regulatory framework that includes the TVET Authority (TVETA) and the TVET Curriculum Development, Assessment and Certification Council (TVET CDACC).")
process['stakeholders'].append({"stakeholder": "TVET Trainees/Students", "role": "Recipients of technical and vocational skills training", "responsibilities": "(INFERRED) Engaging in learning, pursuing career development."})
process['stakeholders'].append({"stakeholder": "Industry/Employers", "role": "Consumers of skilled labor; partners in curriculum development and training", "responsibilities": "(INFERRED) Providing input on skills needs, offering attachments/internships, employing TVET graduates."})
process['stakeholders'].append({"stakeholder": "TVET Institutions (Technical Colleges, National Polytechnics)", "role": "Providers of TVET training programs", "responsibilities": "(INFERRED) Delivering quality training, adhering to TVET standards, managing resources."})
process['stakeholders'].append({"stakeholder": "TVET Authority (TVETA)", "role": "Regulatory and coordinating body for TVET training", "responsibilities": "(INFERRED) Accrediting programs, inspecting institutions, advising Cabinet Secretary."})
process['stakeholders'].append({"stakeholder": "TVET Curriculum Development, Assessment and Certification Council (TVET CDACC)", "role": "Body responsible for TVET curriculum and certification", "responsibilities": "(INFERRED) Designing curricula, conducting assessments, issuing competence certificates."})

process['as_is_narrative'] = "(INFERRED) The State Department for TVET develops national TVET policies, oversees the management and operations of various TVET institutions, regulates training standards through TVETA, develops curricula via TVET CDACC, promotes access and equity in training opportunities, integrates ICT in TVET, and builds strong industry linkages to ensure relevance of training."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://devolution.go.ke/",
    "https://tveta.go.ke/",
    "https://tvetcdacc.go.ke/"
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Thirteenth process enriched and combined_data.json updated.")
