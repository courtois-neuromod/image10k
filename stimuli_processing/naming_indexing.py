# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 16:39:22 2019

@author: Francois
"""

import os
from os import getcwd
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
from os.path import splitext
import pandas as pd
from tqdm import tqdm # Displays iteration progress bar

def naming_indexing(fname):
    '''
    Names and indexes images according to category.
    Saves image's infos to .xlsx format in current working directory.
    Use when all images are ready to be catalogued.
    If not, use 'proper_index2.py' instead to avoid erasing original names.

    Parameters
    ----------
    fname: type=str
        Name of the image folder

    Returns:
    --------
    pandas DataFrame:
        columns: name, website, online image ID, extension
    '''
    SOURCES = '/home/francois/Desktop/neuromod_image_bank/neuromod_image_bank_docs/sources.csv'
    refs = pd.read_csv(SOURCES)['reference'].tolist()
    urls = pd.read_csv(SOURCES)['URL'].tolist()
    imageinfos_to_df = []
    for subd in os.listdir(join(getcwd(), fname)):
        for subdd in tqdm(os.listdir(join(getcwd(), fname, subd))):
            if subd in subdd:
                newsubdd = subdd[subdd.find(subd)+len(str(subd))+1:]
            if 'bodypart' in subd:#corrections to uniformize labels
                newsubdd = subd.replace('bodypart', 'body_part')
            else: newsubdd = subdd
            os.rename(join(getcwd(), fname, subd, subdd),
                      join(getcwd(), fname, subd, newsubdd))
    for allpics in os.walk(join(getcwd(), fname)):
        counter = 1
        for picture in tqdm(allpics[2]):
            if os.path.isfile(join(allpics[0], picture)):
                if counter <= 9:
                    okname = bname(dname(join(allpics[0], picture)))+ \
                             '0'+str(counter)+splitext(join(allpics[0],
                                                            picture))[1]
                elif counter >= 10:
                    okname = bname(dname(join(allpics[0], picture)))+ \
                    str(counter)+splitext(join(allpics[0], picture))[1]
                for ref in refs.__iter__():
                    if picture.find(ref) != -1:
                        longpath, ext = splitext(join(allpics[0], picture))
                        image_id = longpath[longpath.find(ref)+len(ref):]
                        imageinfos_to_df.append((picture, okname, ref,
                                                 urls[refs.index(ref)],
                                                 image_id, ext))
                os.rename(join(allpics[0], picture),
                          join(allpics[0], okname))
                counter += 1
    imageinfos_to_df = pd.DataFrame(imageinfos_to_df, columns=['picture','name', 'website', 'url',
                                'online_image_id', 'extension'])
#    imageinfos_to_df.columns = 
    imageinfos_to_df.to_excel(join(getcwd(), fname+'DF.xlsx'))
