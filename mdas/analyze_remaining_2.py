import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    remaining = []
    for item in items:
        # Check if NOT updated (no steps)
        if not item.get('as_is_steps') or len(item.get('as_is_steps')) == 0:
            remaining.append(item.get('mda_name', 'Unknown'))

    print(f"Remaining MDAs: {len(remaining)}")
    print("--- Sample of Remaining MDAs ---")
    # Print sorted sample (every 4th item to get a spread)
    for i, name in enumerate(sorted(remaining)):
        if i % 4 == 0:
            print(name)

except Exception as e:
    print(f"Error: {e}")
