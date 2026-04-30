import os
import json

dir_path = '.'

for filename in os.listdir(dir_path):
    if not filename.isdigit():
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r') as f:
        data = json.load(f)

    data['image'] = data['image'] + 'image'
    data['animation_url'] = data['animation_url'] + 'glb'

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

print("Done! Updated all files.")
