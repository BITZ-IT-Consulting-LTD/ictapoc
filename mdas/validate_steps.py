import json

file_path = '/Users/mac/ictapoc/mdas/combined_data.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get('processes', [])

    total = len(items)
    with_steps = 0
    missing = []

    for item in items:
        steps = item.get('as_is_steps', [])
        if steps and len(steps) > 0:
            with_steps += 1
        else:
            missing.append(item.get('mda_name', 'Unknown'))

    print(f"Validation Report:")
    print(f"Total MDAs: {total}")
    print(f"MDAs with As-Is Steps: {with_steps}")
    print(f"MDAs Missing Steps: {len(missing)}")
    
    if len(missing) == 0:
        print("\n✅ VALIDATION PASSED: 100% Coverage Achieved.")
    else:
        print("\n❌ VALIDATION FAILED: Missing Steps for:")
        for name in missing[:10]:
            print(f"- {name}")

except Exception as e:
    print(f"Error: {e}")
