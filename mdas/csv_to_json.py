import pandas as pd
import json
import numpy as np

# Define the base JSON structure
base_json_structure = {
  "ministry_code": "",
  "ministry_name": "",
  "processes": []
}

# Define a blank process structure based on the user's schema
blank_process = {
      "process_id": "",
      "mda_name": "",
      "sector": "",

      "cover_page": {
        "process_name": "",
        "document_version": "",
        "publication_date": "",
        "classification": ""
      },

      "document_control": [],
      "executive_summary": "",
      "process_overview": {
        "service_category": "",
        "process_objective": "",
        "scope": {
          "in_scope": [],
          "out_of_scope": []
        },
        "triggers": [],
        "end_states": {
          "successful": [],
          "unsuccessful": []
        },
        "policy_legal_context": []
      },

      "stakeholders": [],
      "inputs_outputs_dependencies": {
        "inputs": [],
        "outputs": [],
        "external_dependencies": []
      },

      "process_maturity": {
        "existing_workflow": "",
        "documentation_status": "",
        "level_of_automation": ""
      },

      "as_is_narrative": "",
      "as_is_steps": [],
      "decision_points": [],
      "exceptions": [],
      "pain_points_bottlenecks_risks": [],
      "to_be_process": {
        "narrative": ""
      },

      "digitization_opportunities": [],
      "kpis": [],
      "change_impact": {
        "people": "",
        "process": "",
        "technology": "",
        "policy": ""
      },

      "assumptions_gaps_open_issues": {
        "assumptions": [],
        "gaps": [],
        "open_issues": []
      },

      "data_elements": [],
      "glossary": [],
      "metadata": {
        "source_url": "",
        "confidence_level": ""
      }
    }


# Read the CSV file without a header
df = pd.read_csv('combined_tiers.csv', header=None)

# Initialize the final JSON object
final_json = base_json_structure.copy()

# Iterate through the DataFrame rows, starting from row 2 (index 2) for data
# The actual header with "MDA Code", "MDA Name" etc. is in row 0 (index 0)
# The row with "S/N" and "ENTITY’S NAME" is in row 1 (index 1)

for i in range(2, len(df)): # Start from index 2 to skip header and subheader rows
    row = df.iloc[i]
    current_process = json.loads(json.dumps(blank_process)) # Deep copy the blank process template

    # Pattern 1: Data in column 2 (ENTITY’S NAME type of rows) - if col 2 has value and col 3 is NaN
    if pd.notna(row[2]) and pd.isna(row[3]):
        current_process['mda_name'] = str(row[2]).strip()
        current_process['cover_page']['process_name'] = str(row[2]).strip()
    # Pattern 2: Data in columns 3-8 (MDA Code, MDA Name etc.) - if col 3 has a value
    elif pd.notna(row[3]):
        val_3 = row[3]
        if pd.notna(val_3):
            try:
                # Attempt to convert to float, then int, then string
                current_process['process_id'] = str(int(float(val_3)))
            except ValueError:
                # If conversion fails (e.g., it's a non-numeric string), leave blank
                current_process['process_id'] = ""
        else:
            current_process['process_id'] = ""

        current_process['mda_name'] = str(row[4]).strip() if pd.notna(row[4]) else ""
        current_process['sector'] = str(row[6]).strip() if pd.notna(row[6]) else ""
        current_process['cover_page']['process_name'] = str(row[4]).strip() if pd.notna(row[4]) else ""
        current_process['executive_summary'] = str(row[8]).strip() if pd.notna(row[8]) else ""
        current_process['process_overview']['process_objective'] = str(row[8]).strip() if pd.notna(row[8]) else ""

    if current_process['mda_name'] or current_process['process_id']: # Only add if it has some meaningful data
        final_json['processes'].append(current_process)

# Write the JSON object to a file
with open('combined_data.json', 'w') as f:
    json.dump(final_json, f, indent=2)

print("JSON file 'combined_data.json' created successfully.")