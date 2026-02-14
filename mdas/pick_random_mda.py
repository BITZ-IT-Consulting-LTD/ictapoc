import json
import random
import sys

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

try:
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Determine where the MDA/Process objects are
    if isinstance(data, list):
        # Top level is a list
        items = data
    elif isinstance(data, dict) and 'processes' in data:
        # Top level is a dict with a processes list
        items = data['processes']
    else:
        print("Unknown JSON structure. Keys:", data.keys() if isinstance(data, dict) else "List")
        sys.exit(1)

    if not items:
        print("No items found.")
        sys.exit(1)

    # Pick one random item
    random_item = random.choice(items)
    
    # Print it formatted
    print(json.dumps(random_item, indent=2))

except Exception as e:
    print(f"Error: {e}")
