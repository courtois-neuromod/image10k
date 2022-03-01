"""
This script aims at reconciliating the zooniverse data, the local image10k
dataset, and the xlsx metaddata used to document authorship and licenses.
"""
import os
import numpy as np
import pandas as pd
from api import get_data, get_path_image10k
import json

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

## Clean up file extensions and license codes
df_metadata.loc[df_metadata['author'].isna(), 'author'] = 'none'
df_metadata.loc[df_metadata['license_code'].isna(), 'license_code'] = 'none'

for row in df_metadata.index:
    try:
        df_metadata.loc[row, 'license_code'] = df_metadata.loc[row, 'license_code'].replace('None', 'none')
    except:
        df_metadata.loc[row, 'license_code'] = f"F{df_metadata.loc[row, 'license_code']:.0f}"
    try:
        df_metadata.loc[row, 'source_url'] = df_metadata.loc[row, 'source_url'].replace('None', 'none')
    except:
        df_metadata.loc[row, 'source_url'] = str(df_metadata.loc[row, 'source_url'])
    try:
        df_metadata.loc[row, 'author'] = df_metadata.loc[row, 'author'].replace('None', 'none')
    except:
        df_metadata.loc[row, 'author'] = str(df_metadata.loc[row, 'author'])
    df_metadata.loc[row, 'name'] = df_metadata.loc[row, 'name'].replace('jpeg', 'jpg')
    df_metadata.loc[row, 'name'] = df_metadata.loc[row, 'name'].replace('png', 'jpg')
    df_metadata.loc[row, 'name'] = df_metadata.loc[row, 'name'].replace('JPG', 'jpg')

## Merge tag information from the dataset
df_metadata.insert(len(df_metadata.columns), "tag", "None")
for row_m, file in enumerate(df_metadata['name']):
    for row_i, item in enumerate(df_image10k['name']):
        if file == item:
            df_metadata.loc[row_m, 'tag'] = df_image10k.loc[row_i, 'tag']

df_metadata.to_csv(os.path.join(path_image10k, 'image10k.tsv'), sep='\t')
