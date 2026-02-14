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
    # Print sorted sample
    for name in sorted(remaining)[:50]:
        print(name)

except Exception as e:
    print(f"Error: {e}")
