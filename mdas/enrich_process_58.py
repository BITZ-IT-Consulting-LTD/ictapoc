
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the fifty-ninth process (index 58)
process = data['processes'][58]

# Populate fields
process['executive_summary'] = "The Kenya National Examinations Council (KNEC) is a statutory body mandated by Section 10 of the KNEC Act No. 29 of 2012. Its core responsibility is to set and maintain examination standards, and to develop and conduct public academic, technical, and other national examinations at basic and tertiary levels within Kenya. KNEC also awards certificates or diplomas to successful candidates, thereby playing a critical role in evaluating educational achievement and facilitating progression in education and employment."
process['process_overview']['process_objective'] = "To develop and implement robust examination policies, procedures, and regulations; to effectively conduct national examinations across various educational levels; to register candidates efficiently for all KNEC examinations; to process and disseminate examination results accurately and in a timely manner; to award credible certificates and diplomas to successful candidates; to confirm the authenticity of credentials issued by the Council; to undertake research on educational assessment to inform best practices; to carry out the equation of foreign qualifications; and to advise the Government on matters pertaining to examinations and certification policies."
process['process_overview']['policy_legal_context'].append("Mandated by Section 10 of the KNEC Act No. 29 of 2012, which establishes its legal framework and functions. Operates under the oversight of the Ministry of Education and collaborates with other educational agencies to ensure the quality and relevance of national examinations and assessment systems.")
process['stakeholders'].append({"stakeholder": "Learners / Candidates", "role": "Primary subjects of examinations; beneficiaries of certification", "responsibilities": "(INFERRED) Registering for exams, adhering to examination rules, preparing for assessments."})
process['stakeholders'].append({"stakeholder": "Schools / Educational Institutions", "role": "Centers for examination administration and preparation", "responsibilities": "(INFERRED) Registering candidates, providing examination facilities, preparing learners."})
process['stakeholders'].append({"stakeholder": "Teachers / Examiners", "role": "Involved in preparing learners, invigilating examinations, and marking scripts", "responsibilities": "(INFERRED) Delivering curriculum, ensuring fair examination processes, accurate marking."})
process['stakeholders'].append({"stakeholder": "Ministry of Education", "role": "Parent Ministry providing policy direction and oversight", "responsibilities": "(INFERRED) Formulating education policies, ensuring examination system integrity."})
process['stakeholders'].append({"stakeholder": "Parents / Guardians", "role": "Support and monitor learners' educational progress", "responsibilities": "(INFERRED) Supporting examination preparation, ensuring timely registration."})
process['stakeholders'].append({"stakeholder": "Higher Education Institutions", "role": "Utilize KNEC certificates for admissions and academic progression", "responsibilities": "(INFERRED) Setting admission criteria, recognizing KNEC qualifications."})
process['stakeholders'].append({"stakeholder": "Employers", "role": "Utilize KNEC certificates to assess candidates' qualifications for employment", "responsibilities": "(INFERRED) Validating credentials, recruiting qualified personnel."})
process['stakeholders'].append({"stakeholder": "Foreign Examination Boards", "role": "Collaborators in standardizing and equating qualifications across borders", "responsibilities": "(INFERRED) Exchanging information, recognizing equivalent qualifications."})
process['stakeholders'].append({"stakeholder": "Curriculum Developers (e.g., KICD)", "role": "Develop curricula that examinations assess", "responsibilities": "(INFERRED) Aligning curriculum with assessment, providing subject content expertise."})
process['stakeholders'].append({"stakeholder": "Quality Assurance Bodies", "role": "Ensure the quality and integrity of the education and examination system", "responsibilities": "(INFERRED) Monitoring standards, providing feedback for improvement."})

process['as_is_narrative'] = "(INFERRED) KNEC's operations involve a meticulous process that begins with the development of examination papers and assessment tools across various subjects and educational levels, guided by curriculum requirements. This is followed by the registration of candidates, ensuring all eligible learners are enrolled. The Council then meticulously plans and administers examinations nationwide, ensuring strict security protocols to safeguard the integrity of the process. After examinations, KNEC manages the complex logistical exercise of collecting, marking, and processing millions of examination scripts. This leads to the accurate compilation and release of examination results, which are then used to award tamper-proof certificates and diplomas to successful candidates. Furthermore, KNEC engages in continuous research to improve assessment methodologies, provides a service for the equation and confirmation of academic qualifications, and offers expert advice to the government on educational assessment policies and standards, thereby playing a central role in shaping Kenya's education landscape."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.knec.ac.ke/",
    "https://educationnewshub.co.ke/", # Provided context
    "https://afro.co.ke/", # Provided context
    "https://kenyaplex.com/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fifty-ninth process enriched and combined_data.json updated.")
