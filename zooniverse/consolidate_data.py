"""
This script aims at reconciliating the zooniverse data, the local image10k
dataset, and the xlsx metaddata used to document authorship and licenses.
"""
import os
import numpy as np
import pandas as pd
from api import get_data, get_path_image10k

# Load image10k and zooniverse data frames
path_image10k = get_path_image10k()
df_image10k = get_data()
df_zooniverse = pd.read_csv(os.path.join(os.path.split(path_image10k)[0], 'zooniverse', 'you-see-it-you-name-it-subjects.csv'))

## Generate consolidated xlxs
df_animal = pd.read_excel(os.path.join(path_image10k, 'animal.xlsx'))
df_human_face = pd.read_excel(os.path.join(path_image10k, 'human_face.xlsx'))
df_human_body_parts = pd.read_excel(os.path.join(path_image10k, 'human_body_parts.xlsx'))
df_object = pd.read_excel(os.path.join(path_image10k, 'object.xlsx'))
df_metadata = pd.concat([df_human_face, df_human_body_parts, df_animal, df_object], ignore_index=True)
df_metadata = df_metadata.drop(['ID', 'metadata', 'website', 'online_image_id', 'extension', 'include', 'license'], axis=1)
df_metadata = df_metadata.rename({'url': 'source_website'}, axis=1)
for row in df_metadata.index:
    df_metadata.loc[row, 'name'] = df_metadata.loc[row, 'name'].replace('jpeg', 'jpg')
    df_metadata.loc[row, 'name'] = df_metadata.loc[row, 'name'].replace('png', 'jpg')
    df_metadata.loc[row, 'name'] = df_metadata.loc[row, 'name'].replace('JPG', 'jpg')

df_metadata.to_csv(os.path.join(path_image10k, 'image10k.tsv'), sep='\t')

# Find discrepancies
discrepancies = {}

print("\nDiscrepancies zooniverse -> metadata")
discrepancies['zoo2meta'] = []
for item in df_zooniverse['metadata']:
    item_json = json.loads(item)
    if "Filename" in item_json.keys():
        file = item_json["Filename"]
    elif "#name" in item_json.keys():
        file = item_json["#name"]
    elif "image_name_1" in item_json.keys():
        file = item_json["image_name_1"]
    else:
        print(item_json)
        raise ValueError
    file = file.replace("-compressed", "")
    mask = [file.split('.')[0] == item.split('.')[0] for item in df_metadata['name']]
    if not any(mask):
        discrepancies['zoo2meta'].append(file)
print(sorted(discrepancies['zoo2meta']))
print(f"{len(discrepancies['zoo2meta'])} discrepancies found")

print("\nDiscrepancies image10k -> metadata")
discrepancies['image2meta'] = []
for file in df_image10k['name']:
    mask = [file == item for item in df_metadata['name']]
    if not any(mask):
        discrepancies['image2meta'].append(file)
        print(f"{file} from image10k not found in metadata")

print(f"{len(discrepancies['image2meta'])} discrepancies found")

print("\nDiscrepancies metadata -> image10k")
discrepancies['meta2image'] = []
for file in df_metadata['name']:
    mask = [file == item for item in df_image10k['name']]
    if not any(mask):
        discrepancies['meta2image'].append(file)
        print(f"{file} from metadata not found in image10k")

print(f"{len(discrepancies['meta2image'])} discrepancies found")

print("\nDiscrepancies image10k -> zooniverse")
for file in df_image10k['name']:
    keyword = file.split('.')[0]
    mask = [keyword in item for item in df_zooniverse['metadata']]
    if not any(mask):
        print(f"{keyword} not found in zooniverse records")

print("\nDiscrepancies zooniverse -> image10k")

discrepancies['zoo2image'] = []
for item in df_zooniverse['metadata']:
    item_json = json.loads(item)
    if "Filename" in item_json.keys():
        file = item_json["Filename"]
    elif "#name" in item_json.keys():
        file = item_json["#name"]
    elif "image_name_1" in item_json.keys():
        file = item_json["image_name_1"]
    else:
        print(item_json)
        raise ValueError
    file = file.replace("-compressed", "")
    mask = [file.split('.')[0] == item.split('.')[0] for item in df_image10k['name']]
    if not any(mask):
        discrepancies['zoo2image'].append(item)
        print(f"{item} from zooniverse not found in image10k")

print(f"{len(discrepancies['zoo2image'])} discrepancies found")

## look for possible correspondance
search_term = 'peacock'
for items in df_zooniverse['metadata']:
    if search_term in items:
        print(items)
