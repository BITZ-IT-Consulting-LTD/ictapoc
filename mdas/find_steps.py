import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

try:
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Handle list vs dict structure
    items = data if isinstance(data, list) else data.get('processes', [])

    found_count = 0
    example = None

    for item in items:
        steps = item.get('as_is_steps', [])
        if steps and len(steps) > 0:
            found_count += 1
            if example is None:
                example = item

    print(f"Total objects with 'as_is_steps' populated: {found_count}")
    
    if example:
        print("\n--- Example Found ---")
        print(f"MDA Name: {example.get('mda_name')}")
        print(f"Process Name: {example.get('cover_page', {}).get('process_name')}")
        print("Steps:")
        print(json.dumps(example['as_is_steps'], indent=2))

except Exception as e:
    print(f"Error: {e}")
