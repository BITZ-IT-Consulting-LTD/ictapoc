import json

with open('combined_data.json', 'r') as f:
    data = json.load(f)

print("Enrichment Status for first 55 processes:")
for i, process in enumerate(data['processes'][:55]):
    mda_name = process.get('mda_name', 'N/A')
    confidence_level = process.get('metadata', {}).get('confidence_level', 'NOT ENRICHED')
    print(f"Index {i}: {mda_name} - Status: {confidence_level}")