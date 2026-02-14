
import json

try:
    with open('combined_data.json', 'r') as f:
        data = json.load(f)

    # Check MDA at index 0
    if len(data['processes']) > 0:
        mda_0 = data['processes'][0]
        print(f"MDA at index 0: {mda_0['mda_name']}")
        if mda_0.get('metadata') and mda_0['metadata'].get('confidence_level'):
            print(f"Confidence Level at index 0: {mda_0['metadata']['confidence_level']}")
        else:
            print("Confidence Level at index 0: Not enriched or metadata/confidence_level missing.")
    else:
        print(f"Index 0 is out of bounds. Total processes: {len(data['processes'])}")

    # Check MDA at index 116
    if len(data['processes']) > 116:
        mda_116 = data['processes'][116]
        print(f"MDA at index 116: {mda_116['mda_name']}")
        if mda_116.get('metadata') and mda_116['metadata'].get('confidence_level'):
            print(f"Confidence Level at index 116: {mda_116['metadata']['confidence_level']}")
        else:
            print("Confidence Level at index 116: Not enriched or metadata/confidence_level missing.")
    else:
        print(f"Index 116 is out of bounds. Total processes: {len(data['processes'])}")

except FileNotFoundError:
    print("Error: combined_data.json not found.")
except json.JSONDecodeError:
    print("Error: Could not decode combined_data.json. Check for valid JSON format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
