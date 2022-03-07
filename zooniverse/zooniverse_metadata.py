import os
import pandas as pd
import json
from tqdm import tqdm
from api.image10k import get_data, get_path_image10k
from report.generate_report import _get_index_zooniverse

def _get_metadata(df, name, dict_license):
    include = False
    author = 'none'
    license = 'none'
    for row in df.itertuples():
        license_ok = getattr(row, "license_code") not in ["F0", "none"]
        if license_ok and (name == getattr(row, 'name').split('.')[0]):
            include = getattr(row, 'include')
            author = f"Author: {getattr(row, 'author')}. Image source: {getattr(row, 'source_url')}"
            license = dict_license[getattr(row, 'license_code')]
    return author, license, include


# Set up path and load dataset
path_image10k = get_path_image10k()
path_report = os.path.join(os.path.split(path_image10k)[0], "image10k_report")
path_template = os.path.join(os.path.split(path_image10k)[0], "report")
df = pd.read_csv(os.path.join(path_image10k, "image10k.tsv"), sep="\t")
with open(os.path.join(path_image10k, "image10k.json"), 'r') as f: info = json.load(f)
dict_license = info['license_code']['Levels']

df_zooniverse = pd.read_csv(os.path.join(os.path.split(path_image10k)[0], 'zooniverse', 'you-see-it-you-name-it-subjects.csv'))
index_zooniverse = _get_index_zooniverse(df_zooniverse)

df_zooniverse.insert(len(df_zooniverse.columns), "author", "none")
df_zooniverse.insert(len(df_zooniverse.columns), "license", "none")
df_zooniverse.insert(len(df_zooniverse.columns), "include", "False")
for row, name in tqdm(enumerate(index_zooniverse[0:100])):
    author, license, include = _get_metadata(df, name, dict_license)
    df_zooniverse.loc[row, 'author'] = author
    df_zooniverse.loc[row, 'license'] = license
    df_zooniverse.loc[row, 'include'] = include

# Save results
file_output = os.path.join(os.path.split(path_image10k)[0], 'zooniverse', 'you-see-it-you-name-it-subjects_with_metadata.csv')
df_zooniverse.to_csv(file_output, sep='\t')
