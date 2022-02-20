# image10k

## Overview

`image10k` is a dataset of natural images sorted by categories developed by the Courtois project on neuronal modelling ([cneuromod](https://cneuromod.ca)). The images were collected by M. Francois Nadeau and Mrs. Samie-Jade Allard. The annotation of the images on the [zooniverse]() platform was led by Dr Valentina Borghesani. Further contributors include Dr Martin Hebart, Mrs Julie Boyle and Dr Pierre Bellec.

## API  
The main API to access the dataset can be found in `api/image10k.py`.

```Python
# Import the module
from image10k import Image10k

# Navigate the database
data = Image10k()
human = data.loc['human']['data']

# shows image names (synsets)
human.index

# number of images for a concept
human.n_pic

# path to each concept folder
bar = human.fpath
# synsets of every superior category
# a synset crosses while ascending the database
human.tags

# flatten one-hot encoding of category membership
human.vec
```

## Other content
 * `image10k` is a symbolic link to the `image10k` dataset. Update this link to your local copy. This will eventually be replaced by a datalad submodule.
 * `get_authors` scripts and data used to collect the meta-data of all pictures, including author names and licenses.
 * `zooniverse` scripts and data used in the upload on the zooniverse platform.
 * `api` python tools to access the data.
