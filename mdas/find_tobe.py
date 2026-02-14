import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

try:
    with open(file_path, 'r') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])
    
    tobe_count = 0
    
    for item in items:
        tobe = item.get('to_be_process', {})
        # Check if narrative is non-empty or if there are steps inside
        if tobe.get('narrative') or tobe.get('steps'):
            tobe_count += 1

    print(f"Total objects with 'to_be_process' populated: {tobe_count}")

except Exception as e:
    print(f"Error: {e}")
