import os
import json

dir_path = '.'

for filename in os.listdir(dir_path):
    if not filename.isdigit():
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r') as f:
        data = json.load(f)

    img = data['image']
    anim = data['animation_url']

    # Strip any trailing 'image' or 'glb' suffixes (could be doubled)
    while img.endswith('image'):
        img = img[:-5]  # len('image') = 5
    while anim.endswith('glb'):
        anim = anim[:-3]  # len('glb') = 3

    # Now apply exactly once
    data['image'] = img + 'image'
    data['animation_url'] = anim + 'glb'

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

print("Done! All files fixed.")
