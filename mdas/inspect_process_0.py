
import json

with open('combined_data.json', 'r') as f:
    data = json.load(f)
    print(json.dumps(data['processes'][0], indent=2))
