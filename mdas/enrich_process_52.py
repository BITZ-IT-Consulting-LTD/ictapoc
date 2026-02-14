
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifty-third process (index 52)
process = data['processes'][52]

# Populate fields
process['executive_summary'] = "The Kenya Institute of Curriculum Development (KICD) is a state corporation established by the KICD Act No. 4 of 2013. Its primary mandate is to develop quality curricula and curriculum support materials for basic and tertiary education, advise the government and the public on curriculum matters, and promote the application of research findings and educational innovations to enhance the quality of education in Kenya."
process['process_overview']['process_objective'] = "To develop, review, and approve programs, curricula, and curriculum support materials for all levels of education; to advise the Government on all matters pertaining to curriculum development; to evaluate, vet, and approve local and foreign curricula; to implement curriculum policies; to initiate and conduct research to inform curriculum development; and to promote the appropriate utilization of technology to foster innovations in education."
process['process_overview']['policy_legal_context'].append("Established under the Kenya Institute of Curriculum Development Act No. 4 of 2013, which provides its legal framework. Recent legislative changes (Kenya Institute of Curriculum Development (Amendment) Bill, 2024) aim to refine its mandate to focus primarily on basic and teacher education, resolving overlaps with other sector regulators.")
process['stakeholders'].append({"stakeholder": "Learners / Students", "role": "Primary recipients of the developed curricula and educational materials", "responsibilities": "(INFERRED) Engaging with learning materials, providing feedback on curriculum effectiveness."})
process['stakeholders'].append({"stakeholder": "Teachers", "role": "Implementers of the curriculum and users of curriculum support materials", "responsibilities": "(INFERRED) Delivering the curriculum, participating in professional development, providing feedback."})
process['stakeholders'].append({"stakeholder": "Teacher Trainers", "role": "Educators who train teachers on curriculum delivery and methodologies", "responsibilities": "(INFERRED) Training teachers effectively, staying updated on curriculum changes."})
process['stakeholders'].append({"stakeholder": "Educational Institutions", "role": "Venues for curriculum delivery and implementation", "responsibilities": "(INFERRED) Adhering to curriculum guidelines, providing resources for learning."})
process['stakeholders'].append({"stakeholder": "Ministry of Education", "role": "Parent Ministry providing oversight, policy direction, and funding", "responsibilities": "(INFERRED) Formulating national education policies, ensuring curriculum relevance."})
process['stakeholders'].append({"stakeholder": "Parents / Guardians", "role": "Key partners in the education of learners", "responsibilities": "(INFERRED) Supporting learners' education, engaging with curriculum content."})
process['stakeholders'].append({"stakeholder": "Publishers (Curriculum Support Materials)", "role": "Developers and producers of textbooks and other learning resources", "responsibilities": "(INFERRED) Developing high-quality materials, ensuring alignment with curriculum."})
process['stakeholders'].append({"stakeholder": "Quality Assurance Officers", "role": "Ensure the quality of curriculum implementation and educational standards", "responsibilities": "(INFERRED) Monitoring curriculum delivery, assessing educational outcomes."})
process['stakeholders'].append({"stakeholder": "Other Education Personnel", "role": "Various staff involved in supporting the education system", "responsibilities": "(INFERRED) Contributing to an effective learning environment."})
process['stakeholders'].append({"stakeholder": "Research Institutions", "role": "Collaborators in educational research and innovation", "responsibilities": "(INFERRED) Conducting research, providing data for curriculum improvements."})
process['stakeholders'].append({"stakeholder": "Mass Media / Digital Platforms", "role": "Channels for disseminating educational programs and curriculum support materials", "responsibilities": "(INFERRED) Broadcasting educational content, facilitating digital learning."})

process['as_is_narrative'] = "(INFERRED) KICD's operations involve a cyclical process of curriculum development, review, and approval, covering various educational levels from early childhood to tertiary education. This includes rigorous research and evaluation to inform policy and content. KICD also evaluates and vets a wide range of curriculum support materials (e.g., textbooks, digital resources) for use in Kenyan schools. A key function is the professional development of teachers and other education personnel through training programs on curriculum delivery and pedagogical approaches. Furthermore, KICD leverages mass media and digital platforms to disseminate educational programs and materials, actively promoting the integration of technology in learning and advising the government on curriculum-related policies to ensure education remains relevant, equitable, and of high quality."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://kicd.ac.ke/",
    "https://theorg.com/", # Provided context
    "https://educationnews.co.ke/", # Provided context
    "https://institutiontoday.com/", # Provided context
    "https://scribd.com/", # Provided context
    "https://askfilo.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifty-third process enriched and combined_data.json updated.")
