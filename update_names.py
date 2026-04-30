import os
import json

dir_path = '.'

for filename in os.listdir(dir_path):
    if filename.isdigit():
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
        grade = None
        for attr in data['attributes']:
            if attr['trait_type'] == 'Grade':
                grade = attr['value']
                break
        if grade:
            data['name'] = data['name'] + ' ' + grade + ' #' + filename
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)