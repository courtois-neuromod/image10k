"""
Check discrepancies between three data sources:
 1. the spreadsheet containing meta-data for all images.
 2. the files inside image10k_dataset
 3. the list of files uploaded to zooniverse
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
df_metadata = pd.read_csv(os.path.join(path_image10k, 'image10k.tsv'), sep='\t')

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
