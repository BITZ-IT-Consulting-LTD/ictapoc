
import json
import datetime

# Load the JSON data
with open('combined_data.json', 'r') as f:
    data = json.load(f)

# Get the ninetieth process (index 89)
process = data['processes'][89]

# Populate fields
process['executive_summary'] = "The Anti-Doping Agency of Kenya (ADAK) is an agency mandated to protect the integrity of drug-free sports and the fundamental right of athletes to participate in doping-free activities in Kenya. Established to give effect to the World Anti-Doping Code and the UNESCO Convention Against Doping in Sport, ADAK undertakes comprehensive anti-doping activities. These include enforcing regulations, conducting testing, research, education and awareness campaigns, investigating doping offenses, and managing results of Anti-Doping Rule Violations, thereby ensuring fair play and upholding the ethical values of sports."
process['process_overview']['process_objective'] = "To advise the Government on all anti-doping matters; to undertake anti-doping activities in Kenya in consultation and partnership with regional and international anti-doping organizations, including the World Anti-Doping Agency (WADA); to enforce regulations made by ADAK and WADA; to conduct doping control, which involves in- and out-of-competition testing of athletes and safeguarding sample integrity; to undertake research related to anti-doping; to create awareness and implement programs to combat doping through education, sensitization, and awareness campaigns; to liaise with other government agencies to eradicate performance-enhancing substance use among sports persons; to promote the integrity of drug-free sports; to investigate and gather intelligence on anti-doping related offenses, including results management of Anti-Doping Rule Violations (ADRVs); to oversee the prosecution of anti-doping cases; to develop and execute anti-doping rules and regulations; to grant Therapeutic Use Exemptions (TUEs); and to develop a national strategy to address doping in sport."
process['process_overview']['policy_legal_context'].append("ADAK's mandate is primarily derived from the Anti-Doping Act, 2016, which domesticates the World Anti-Doping Code and the UNESCO Convention Against Doping in Sport. This legislative framework provides ADAK with the legal authority to implement anti-doping rules and regulations in Kenya. ADAK operates under the Ministry of Sports, Culture and the Arts (or the relevant government ministry responsible for sports development) and is guided by national sports policies aimed at promoting clean sports and protecting the health and rights of athletes.")
process['stakeholders'].append({"stakeholder": "Athletes (Amateur and Professional)", "role": "Primary subjects of anti-doping regulations; beneficiaries of clean sport environment", "responsibilities": "(INFERRED) Adhering to anti-doping rules, participating in testing, seeking TUEs if needed, participating in education programs."})
process['stakeholders'].append({"stakeholder": "Sports Federations / Associations (National and International)", "role": "Implement anti-doping rules within their respective sports; collaborate with ADAK", "responsibilities": "(INFERRED) Ensuring their athletes comply, assisting in testing coordination, promoting clean sport."})
process['stakeholders'].append({"stakeholder": "Coaches / Team Officials", "role": "Influence athletes' adherence to anti-doping rules; responsible for athlete welfare", "responsibilities": "(INFERRED) Educating athletes on anti-doping, avoiding prohibited methods/substances."})
process['stakeholders'].append({"stakeholder": "Sports Medicine Practitioners", "role": "Provide medical care to athletes; must adhere to anti-doping regulations regarding prescribed substances", "responsibilities": "(INFERRED) Prescribing medications ethically, understanding TUE process, protecting athlete health."})
process['stakeholders'].append({"stakeholder": "Government of Kenya (Ministry of Sports, Culture and the Arts, Ministry of Health)", "role": "Provides policy direction, funding, and legislative support to ADAK; supports public health aspects", "responsibilities": "(INFERRED) Formulating sports policy, allocating resources, collaborating on public health campaigns."})
process['stakeholders'].append({"stakeholder": "World Anti-Doping Agency (WADA)", "role": "Global regulatory body; provides the World Anti-Doping Code and International Standards that ADAK implements", "responsibilities": "(INFERRED) Setting global anti-doping standards, monitoring compliance, providing guidance."})
process['stakeholders'].append({"stakeholder": "International Sports Federations", "role": "Govern international competitions; collaborate with ADAK on testing and results management for Kenyan athletes competing internationally", "responsibilities": "(INFERRED) Implementing anti-doping rules for their sport, collaborating with National Anti-Doping Organizations (NADOs)."})
process['stakeholders'].append({"stakeholder": "National Olympic Committee of Kenya (NOCK)", "role": "Oversees Olympic sports in Kenya; collaborates with ADAK on athlete preparation and clean sport initiatives", "responsibilities": "(INFERRED) Promoting clean sport, supporting athletes, ensuring anti-doping compliance for major games."})
process['stakeholders'].append({"stakeholder": "Sports Fans / Public", "role": "Beneficiaries of clean and fair sports competitions; contribute to public pressure for drug-free sport", "responsibilities": "(INFERRED) Supporting clean athletes, advocating for fair play, reporting suspicious activities."})
process['stakeholders'].append({"stakeholder": "Law Enforcement Agencies", "role": "Collaborate with ADAK on investigations into trafficking and supply of prohibited substances", "responsibilities": "(INFERRED) Investigating criminal aspects of doping, supporting ADAK's intelligence gathering."})

process['as_is_narrative'] = "(INFERRED) The Anti-Doping Agency of Kenya (ADAK) operates a robust program to combat doping in Kenyan sports, aligning with international best practices. Its core activities include the planning and execution of comprehensive doping control programs, involving both unannounced out-of-competition testing and in-competition testing at sports events, where trained Doping Control Officers collect biological samples (urine and/or blood) from athletes, ensuring strict adherence to sample integrity protocols. ADAK maintains a strong intelligence and investigations unit that gathers information on potential anti-doping rule violations (ADRVs), often in collaboration with law enforcement agencies and international partners. Upon confirmation of an ADRV, ADAK is responsible for managing the results, conducting hearings, and overseeing the prosecution of cases, applying appropriate sanctions as per the Anti-Doping Act and the World Anti-Doping Code. A significant focus is placed on prevention through extensive education and awareness programs delivered to athletes, coaches, and support personnel across various sports and age groups, covering topics like the dangers of doping, the list of prohibited substances and methods, and the Therapeutic Use Exemption (TUE) process. ADAK also reviews and grants TUEs for athletes who require prohibited substances for legitimate medical conditions. Collaborating closely with the World Anti-Doping Agency (WADA) and various national and international sports federations, ADAK ensures that Kenya's anti-doping efforts are globally harmonized, thereby protecting the health of athletes and the integrity of sports."

# Update metadata
process['metadata']['enrichment_method'] = "web_search_and_inference"
process['metadata']['confidence_level'] = "high (mandates, functions, legal basis from official website and other reliable sources) / medium (inferred responsibilities, narrative)"
process['metadata']['source_urls'] = [
    "https://www.adak.or.ke/", # Official website
    "https://sportsheritage.go.ke/", # Provided context
    "https://yahoo.com/", # Provided context
    "https://citizen.digital/" # Provided context
]
process['metadata']['last_enriched_date'] = datetime.datetime.now().strftime("%Y-%m-%d")


# Save the updated JSON data
with open('combined_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Ninetieth process enriched and combined_data.json updated.")
