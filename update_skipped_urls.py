import os
import json

dir_path = '.'

# The exact same skip list from before
skip_files = set([str(i) for i in range(1, 21)] + [
    '21', '50', '101', '115', '97', '206', '252', '290',
    '327', '360', '395', '420', '445', '470', '490', '500',
    '509', '517', '524'
])

for filename in skip_files:
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename} - file not found")
        continue

    with open(filepath, 'r') as f:
        data = json.load(f)

    grade = None
    back = None
    for attr in data['attributes']:
        if attr['trait_type'] == 'Grade':
            grade = attr['value']
        if attr['trait_type'] == 'Back':
            back = attr['value']

    if grade is None or back is None:
        print(f"Skipping {filename} - missing grade or back")
        continue

    if back == 'Piedmont':
        back_str = 'piedmont'
    elif back == 'Sweet Caporal':
        back_str = 'sweet'
    else:
        back_str = back.lower().replace(' ', '')

    url_value = f"{grade}{back_str}"
    data['image'] = url_value
    data['animation_url'] = url_value

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Updated {filename}: {url_value}")

print("Done!")
