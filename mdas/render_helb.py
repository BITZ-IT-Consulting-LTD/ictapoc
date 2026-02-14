import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    
    match = None
    for item in items:
        if "Higher Education Loans Board" in item.get('mda_name', ''):
            match = item
            break
            
    if match:
        print(json.dumps(match, indent=2))
    else:
        print("HELB object not found.")

except Exception as e:
    print(f"Error: {e}")
