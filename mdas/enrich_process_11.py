
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the twelfth process (index 11)
process = data['processes'][11]

# Populate fields
process['executive_summary'] = "The State Department for Basic Education in Kenya is responsible for the coordination and management of Early Childhood Development, Primary Education, and Teacher Training Colleges. It oversees the overall governance of basic education, including policy formulation, curriculum development, and resource management to ensure access and quality education."
process['process_overview']['process_objective'] = "To formulate and implement policies and programs for primary education and teacher training, oversee basic education institutions, develop and review curriculum in collaboration with KICD, and promote the growth and quality of basic education across Kenya."
process['process_overview']['policy_legal_context'].append("Operates under the Basic Education Act. Mandated with the governance and management of basic education in Kenya. Relevant policies and strategies are implemented for Free Primary Education and Special Needs Education (SNE).")
process['stakeholders'].append({"stakeholder": "Students (Learners)", "role": "Primary beneficiaries of basic education services", "responsibilities": "(INFERRED) Engaging in learning, adhering to school rules."})
process['stakeholders'].append({"stakeholder": "Teachers", "role": "Educators in primary schools and teacher training colleges", "responsibilities": "(INFERRED) Delivering curriculum, guiding students, professional development."})
process['stakeholders'].append({"stakeholder": "Parents/Guardians", "role": "Key partners in children's education and well-being", "responsibilities": "(INFERRED) Supporting learning, ensuring school attendance, engaging with schools."})
process['stakeholders'].append({"stakeholder": "Teacher Training Colleges", "role": "Institutions responsible for training primary school teachers", "responsibilities": "(INFERRED) Providing quality teacher education, adhering to training standards."})
process['stakeholders'].append({"stakeholder": "Kenya Institute of Curriculum Development (KICD)", "role": "Collaborator in curriculum development, review, and monitoring", "responsibilities": "(INFERRED) Developing curricula, providing educational materials."})
process['stakeholders'].append({"stakeholder": "District Education Boards (DEBs)", "role": "Local governance bodies for education", "responsibilities": "(INFERRED) Overseeing education matters at the district level, school registration."})

process['as_is_narrative'] = "(INFERRED) The State Department's operations include formulating educational policies, supervising basic education institutions, developing and implementing curricula, registering schools, managing financial resources for basic education, overseeing teacher and student affairs, and coordinating strategic partnerships for educational initiatives."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandate, functions, legal basis from official sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://devolution.go.ke/",
    "https://sheriamex.com/", # Though not primary, provided useful context in search
    "https://ilo.org/" # Though not primary, provided useful context in search
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Twelfth process enriched and combined_data.json updated.")
