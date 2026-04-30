import os
import json

dir_path = '.'

fixed = 0
for filename in os.listdir(dir_path):
    if not filename.isdigit():
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r') as f:
        data = json.load(f)

    if 'Holo' not in data.get('name', ''):
        continue

    # Get the back from attributes
    back = None
    for attr in data['attributes']:
        if attr['trait_type'] == 'Back':
            back = attr['value']
            break

    back_str = 'piedmont' if back == 'Piedmont' else 'sweet'

    data['image'] = f"10{back_str}holoimage"
    data['animation_url'] = f"10{back_str}hologlb"

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Fixed {filename}: image={data['image']}, animation_url={data['animation_url']}")
    fixed += 1

print(f"\nDone! Fixed {fixed} files.")
