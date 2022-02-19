#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 18:42:26 2020
@author: francois
"""

import os
from os.path import basename as bname
from os.path import dirname as dname
import numpy as np
import pandas as pd
from tqdm import tqdm
from taskfunctions import flatten
from taskfunctions import intersect
from taskfunctions import loadimages
from taskfunctions import splitall

class cnib():
    '''Generates im10k (pandas Dataframe)\n
       rows = im_names\n
       cols= ['im_name', 'n_pic', 'dir', 'tags', 'vec']\n
       Parameter(s)\n
       ------------\n
       'imdir': top image folder ('images' in cnib)\n
       Variables\n
       ---------\n
       'impaths': list of all image paths (see 'taskfunctions.py')\n
       'im_names': list of all im_names, quantity of images in folder,\
                             folders paths\n
           i.e. 'body_part_dog_tail', 'body_beaver', 'face_bveaver',
                'shoe', 'male_teen' etc.
       'all_tags': ordered list of all possible unique tags\n
       'im10k': conversion of im_names to DF.
                   im10k['tags'].items()
       'matrix': numpy array of category membership for all images
                 For each image, category membership is represented by 1 or 0
                 (1=Category name in path parts; else 0)
       'imdf': conversion from array to DataFrame to create vectors (as rows)\
               for each image\n
       Returns\n
       -------
       'cnib'\n
       *new columns added during execution:\n
           'tags': lists all folders' names (categories) in imdir\n
            'vec': tuple where each boolean value represents\
            category membership\n
            *categories are ordered as 'all_tags'\n
        DATA ACCESS\n
            cnib.loc['concept_name']['datas']['npic', 'dir', 'tags', 'vec']
    '''
    def im_data():
        imdir = '../images'
        impaths = loadimages(imdir)
        im_names = []
        for impath in impaths:
            if 'object' in impath:
                name = bname(dname(impath))
            else:
                name = bname(dname(impath))+' '+\
                                            bname(dname(dname(impath)))
            if '_' in name:
                name = name.replace('_', ' ')
            im_names.append((name, len(os.listdir(dname(impath))),
                             dname(impath)))
        im_names = sorted(list(dict.fromkeys(list(im_names))))
        im10k = pd.DataFrame(im_names, columns=['im_name', 'n_pic', 'dir'])
        im10k.index = im10k.im_name
        im10k['tags'] = [splitall(folderpath[1].split(imdir,
                                                      maxsplit=1)[1])[1:]
                         for folderpath in im10k['dir'].items()]

        alltags = sorted(list(dict.fromkeys(flatten(im10k['tags']))))
        matrix = np.array([[bool(tags[1].__contains__(tag))
                            for tag in alltags]
                           for tags in im10k['tags'].items()])
        imdf = pd.DataFrame(matrix, index=im10k['im_name'],
                            columns=alltags)
        im10k['vec'] = list(row[1] for row in imdf.iterrows())
        im10k = im10k.drop(columns='im_name')
        return im10k
    def categories(im10k, *tags):
        '''Categorizes the DF according to neuromod categories using "tags"'''
        return pd.DataFrame(flatten([[im10k.loc[row[0]]
                             for row in im10k.iterrows()
                             if tag in im10k.loc[row[0]].tags]
                             for tag in tags]))
    def categories2(im10k, **kwords):
        '''Categorizes the DF according to neuromod categories using "tags"'''
        return pd.DataFrame([im10k.loc[row[0]]
                             for row in im10k.iterrows()
                             if kword[0] in im10k.loc[row[0]].tags])
    im10k = get_data()
    alltags = sorted(list(dict.fromkeys(flatten(list(im10k.tags)))))
    cnib = pd.DataFrame(zip(alltags, list(categories(im10k, ind)
                                          for ind in tqdm(alltags))),
                        index=alltags, columns=['categories', 'data'])
    cnib = cnib.drop(columns=['categories'])
    return cnib

#cnib = im10k_data(imdir)
#example
#aquatic_mammal = cnib.loc['aquatic_mammal']['data']