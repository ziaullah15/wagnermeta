import os
import json
import random

dir_path = '.'

# Files to skip: first 20 (1-20) + specific list
skip_files = set([str(i) for i in range(1, 21)] + [
    '21', '50', '101', '115', '97', '206', '252', '290',
    '327', '360', '395', '420', '445', '470', '490', '500',
    '509', '517', '524'
])

# Collect all numeric files to process
files_to_process = []
for filename in os.listdir(dir_path):
    if filename.isdigit() and filename not in skip_files:
        files_to_process.append(filename)

files_to_process.sort(key=lambda x: int(x))
print(f"Files to process: {len(files_to_process)}")

# Read all files and extract their data
file_data = {}
for filename in files_to_process:
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r') as f:
        file_data[filename] = json.load(f)

# Extract the "metadata block" from each file:
# Everything EXCEPT the Edition attribute (which stays with the file number)
# The metadata block = name, attributes (minus Edition), Tokenid
# We'll shuffle these blocks across files

def extract_metadata_block(data):
    """Extract the shuffleable metadata from a file."""
    block = {
        'name': data['name'],
        'attributes': [attr for attr in data['attributes'] if attr['trait_type'] != 'Edition'],
        'Tokenid': data['Tokenid']
    }
    return block

def get_grade_and_back(attributes):
    """Get grade value and back value from attributes list."""
    grade = None
    back = None
    for attr in attributes:
        if attr['trait_type'] == 'Grade':
            grade = attr['value']
        if attr['trait_type'] == 'Back':
            back = attr['value']
    return grade, back

def get_edition_value(data):
    """Get the Edition attribute value from a file's data."""
    for attr in data['attributes']:
        if attr['trait_type'] == 'Edition':
            return attr['value']
    return None

# Extract metadata blocks
metadata_blocks = [extract_metadata_block(file_data[f]) for f in files_to_process]

# Shuffle the metadata blocks
random.shuffle(metadata_blocks)

# Assign shuffled blocks back to files
for i, filename in enumerate(files_to_process):
    original_data = file_data[filename]
    block = metadata_blocks[i]
    
    # Get the original Edition value (stays with this file)
    edition_value = get_edition_value(original_data)
    
    # Get grade and back from the new (shuffled) attributes
    grade, back = get_grade_and_back(block['attributes'])
    
    # Build image/animation_url: grade + back abbreviation
    if back == 'Piedmont':
        back_str = 'piedmont'
    elif back == 'Sweet Caporal':
        back_str = 'sweet'
    else:
        back_str = back.lower().replace(' ', '') if back else 'unknown'
    
    url_value = f"{grade}{back_str}"
    
    # Rebuild the attributes list: Edition first (preserved), then rest from shuffled block
    new_attributes = []
    # Add Trading Card trait from block
    for attr in block['attributes']:
        if attr['trait_type'] == 'Trading Card':
            new_attributes.append(attr)
            break
    # Add Edition (preserved from original file)
    new_attributes.append({'trait_type': 'Edition', 'value': edition_value})
    # Add remaining attributes from block (skip Trading Card already added)
    for attr in block['attributes']:
        if attr['trait_type'] != 'Trading Card':
            new_attributes.append(attr)
    
    # Build new data
    new_data = {
        'name': block['name'],
        'description': original_data['description'],
        'image': url_value,
        'animation_url': url_value,
        'attributes': new_attributes,
        'Tokenid': block['Tokenid']
    }
    
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'w') as f:
        json.dump(new_data, f, indent=2)

print("Done! Metadata randomized.")
print(f"Processed {len(files_to_process)} files.")
print("Skipped files:", sorted(skip_files, key=lambda x: int(x)))
