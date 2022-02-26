"""
This script aims at reconciliating the zooniverse data, the local image10k
dataset, and the xlsx metaddata used to document authorship and licenses.
"""
import os
import numpy as np
import pandas as pd
from api import get_data, get_path_image10k

# Load image10k and zooniverse data frames
df_image10k = get_data()
df_zooniverse = pd.read_csv('you-see-it-you-name-it-subjects.csv')

## Generate consolidated xlxs
path_image10k = get_path_image10k()
df_animal = pd.read_excel(os.path.join(path_image10k, 'animal.xlsx'))
df_human_face = pd.read_excel(os.path.join(path_image10k, 'human_face.xlsx'))
df_human_body_parts = pd.read_excel(os.path.join(path_image10k, 'human_body_parts.xlsx'))
df_object = pd.read_excel(os.path.join(path_image10k, 'object.xlsx'))
df_metadata = pd.concat([df_human_face, df_human_body_parts, df_animal, df_object], ignore_index=True)
df_metadata = df_metadata.drop(['ID', 'metadata', 'website', 'online_image_id', 'extension', 'include', 'license'], axis=1)
df_metadata = df_metadata.rename({'url': 'source_website'}, axis=1)
df_metadata.to_csv(os.path.join(path_image10k, 'image10k.tsv'), sep='\t')

# Find discrepancies
discrepancies = {}

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

print("\nDiscrepancies image10k -> zooniverse")
for file in df_image10k['name']:
    keyword = file.split('.')[0]
    mask = [keyword in item for item in df_zooniverse['metadata']]
    if not any(mask):
        print(f"{keyword} not found in zooniverse records")

print("\nDiscrepancies zooniverse -> image10k")
for item in df_zooniverse['metadata']:
    mask = [keyword.split('.')[0] in item for keyword in df_image10k['name']]
    if not any(mask):
        print(f"{item} not found in image10k")

## look for possible correspondance
search_term = 'peacock'
for items in df_zooniverse['metadata']:
    if search_term in items:
        print(items)
