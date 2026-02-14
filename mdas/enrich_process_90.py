
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninety-first process (index 90)
process = data['processes'][90]

# Populate fields
process['executive_summary'] = "The Anti-Female Genital Mutilation Board is a semi-autonomous government agency in Kenya, established in December 2013 under the Prohibition of Female Genital Mutilation Act, 2011. Its core mandate is to design, supervise, and coordinate public awareness programs against the practice of Female Genital Mutilation (FGM), advise the Government on FGM matters, and lead national efforts to eradicate FGM. The Board plays a crucial role in upholding the dignity and empowerment of girls and women by ensuring the effective implementation of anti-FGM legislation and promoting alternative rites of passage."
process['process_overview']['process_objective'] = "To design, supervise, and coordinate comprehensive public awareness programs against FGM; to advise the Government on all matters relating to FGM and the effective implementation of the Prohibition of FGM Act; to design and formulate policy on the planning, financing, and coordination of all activities related to FGM eradication; to provide technical and other support to institutions, agencies, and other bodies involved in FGM eradication programs; to design specific programs aimed at the eradication of FGM; to facilitate resource mobilization for programs and activities dedicated to eradicating FGM; to raise awareness and actively campaign against FGM across various communities; and to coordinate and lead efforts on behalf of the Kenyan government to ultimately end FGM."
process['process_overview']['policy_legal_context'].append("Established in December 2013 under the Prohibition of Female Genital Mutilation Act, 2011 (Act No. 32 of 2011), which criminalizes FGM and provides the legal framework for the Board's operations. The Board operates under the Ministry of Public Service, Gender, Senior Citizens Affairs and Special Programs (or the relevant government ministry responsible for gender and social protection) and is central to implementing national legislation and policies aimed at eradicating FGM, protecting the rights of girls and women, and promoting gender equality in Kenya.")
process['stakeholders'].append({"stakeholder": "Girls and Women (potential victims/survivors of FGM)", "role": "Primary beneficiaries of the Board's protection, awareness, and eradication programs", "responsibilities": "(INFERRED) Seeking protection, reporting FGM practices, participating in empowerment programs."})
process['stakeholders'].append({"stakeholder": "Local Communities (practicing and non-practicing FGM)", "role": "Key targets for awareness campaigns and community dialogue; their engagement is crucial for FGM eradication", "responsibilities": "(INFERRED) Participating in dialogues, adopting alternative rites of passage, protecting girls from FGM."})
process['stakeholders'].append({"stakeholder": "Traditional / Religious Leaders", "role": "Influential figures in communities; engage with the Board to promote change and support anti-FGM initiatives", "responsibilities": "(INFERRED) Advocating against FGM, supporting alternative rites, educating community members."})
process['stakeholders'].append({"stakeholder": "Community-Based Organizations (CBOs)", "role": "Grassroots organizations implementing anti-FGM programs; receive technical and financial support from the Board", "responsibilities": "(INFERRED) Implementing programs, mobilizing communities, providing local insights."})
process['stakeholders'].append({"stakeholder": "Non-Governmental Organizations (NGOs) working on FGM eradication", "role": "Partners in advocacy, awareness, research, and program implementation; collaborate with the Board", "responsibilities": "(INFERRED) Advocating for rights, implementing programs, sharing best practices."})
process['stakeholders'].append({"stakeholder": "Government Agencies (e.g., Ministry of Health, Ministry of Education, Interior Security, Judiciary, Children's Services)", "role": "Collaborators in implementing anti-FGM policies, providing services, and prosecuting offenders", "responsibilities": "(INFERRED) Providing healthcare, educating about FGM, enforcing laws, protecting children."})
process['stakeholders'].append({"stakeholder": "Law Enforcement Agencies (Police, Prosecutors)", "role": "Responsible for investigating and prosecuting FGM perpetrators", "responsibilities": "(INFERRED) Investigating FGM cases, arresting perpetrators, ensuring legal action."})
process['stakeholders'].append({"stakeholder": "National Gender and Equality Commission", "role": "Advocates for gender equality and the protection of women's rights; collaborates on FGM eradication", "responsibilities": "(INFERRED) Promoting gender equality, monitoring FGM eradication efforts, advising on policy."})
process['stakeholders'].append({"stakeholder": "International Organizations (e.g., UNICEF, UNFPA, UN Women)", "role": "Provide technical and financial support for FGM eradication efforts in Kenya", "responsibilities": "(INFERRED) Funding programs, sharing international best practices, capacity building support."})
process['stakeholders'].append({"stakeholder": "Media", "role": "Key partner in disseminating information and raising public awareness about FGM", "responsibilities": "(INFERRED) Reporting on FGM issues, promoting awareness campaigns, educating the public."})
process['stakeholders'].append({"stakeholder": "Donors / Development Partners", "role": "Provide financial assistance for the Board's programs and FGM eradication initiatives", "responsibilities": "(INFERRED) Funding projects, supporting capacity building, ensuring program sustainability."})

process['as_is_narrative'] = "(INFERRED) The Anti-Female Genital Mutilation Board actively works to eradicate FGM in Kenya through a multi-pronged approach. It develops and implements nationwide public awareness campaigns, utilizing various media channels (radio, TV, print, social media) and community outreach events to educate communities about the severe health, psychological, and human rights consequences of FGM, as well as its illegality under Kenyan law. The Board provides crucial technical and financial support to grassroots Community-Based Organizations (CBOs) and Non-Governmental Organizations (NGOs) that are directly engaged in FGM eradication efforts at the local level, helping them design and implement targeted interventions. It conducts and commissions research and data collection to identify FGM hotspots, understand underlying drivers, and monitor the progress of eradication efforts, thereby informing evidence-based policies and programs. The Board collaborates closely with various government agencies, including the Ministry of Health, Ministry of Education, Interior Security, and the Judiciary, as well as law enforcement agencies (Police, Directorate of Public Prosecutions) to ensure that FGM perpetrators are investigated and prosecuted, and potential victims are protected. Advocacy is a key function, with the Board actively engaging in promoting stronger policies, legislative frameworks, and resource allocation for FGM eradication. It also mobilizes resources from both national and international partners to fund its programs and supports alternative rites of passage (ARP) as a culturally sensitive alternative to FGM. Furthermore, the Board actively engages with traditional and religious leaders to foster dialogue and secure their commitment to ending FGM within their communities, driving social and cultural change."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.antifgmboard.go.ke/", # Official website
    "https://parliament.go.ke/", # Provided context
    "https://unicef.org/", # Provided context
    "https://treasury.go.ke/", # Provided context
    "https://afro.co.ke/", # Provided context
    "https://fgmcri.org/", # Provided context
    "https://www.gov.uk/", # Provided context
    "https://equalitynow.org/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninety-first process enriched and combined_data.json updated.")
