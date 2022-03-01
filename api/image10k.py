"""
API to access the image10k dataset
@author: Francois Nadeau, Pierre Bellec
"""
import os
from os.path import basename as bname
from os.path import dirname as dname
from os.path import splitext

import numpy as np
import pandas as pd
from typing import Sequence


def _load_image():
    """Lists the full path of all '.jpeg' files in image10k."""
    root_data = get_path_image10k()
    list_img = []
    for allimages in os.walk(root_data):
        for image in allimages[2]:
            root_data = os.path.join(allimages[0], image)
            if os.path.isfile(root_data) and root_data.endswith(".jpg"):
                list_img.append(root_data)
    return list_img


def _get_path(list_img):
    list_path = []
    for img in list_img:
        head, tail = os.path.split(img)
        list_path.append(head)
    return list_path


def _get_tag(list_img, root_data):
    list_path = _get_path(list_img)
    list_tag = [path.replace(root_data+os.path.sep, "") for path in list_path]
    list_tag = [tag.replace(os.path.sep, ", ") for tag in list_tag]
    return list_tag


def get_path_image10k():
    """Returns the path to the image10k dataset"""
    library_path, basename = os.path.split(__file__)
    root_repo, library_name = os.path.split(library_path)
    root_data = os.path.join(root_repo, "image10k_dataset")
    return root_data


def get_data():
    """Returns a data frame with the image name and labels."""
    list_img = _load_image()
    root_data = get_path_image10k()
    list_tag = _get_tag(list_img, root_data)
    df = pd.DataFrame(columns=["name", "file", "tag"])
    for num, img in enumerate(list_img):
        df.loc[num, "file"] = img
        head, df.loc[num, "name"] = os.path.split(img)
        df.loc[num, "tag"] = list_tag[num]
    return df
