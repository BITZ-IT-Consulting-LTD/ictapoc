
import json

with open('combined_data.json', 'r') as f:
    data = json.load(f)
    print(len(data['processes']))
