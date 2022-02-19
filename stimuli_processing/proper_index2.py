#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 13:29:33 2020

@author: francois
"""
import os
from os.path import dirname as dname
from os.path import join
import pandas as pd

def proper_index2(folder_name):
    '''
    Names and indexes images according to category.
    Doesn't affect the image's web reference as would 'naming_indexing'
    would (useful to inventoriate and unify labels across categories).
    '''
    sources = pd.read_csv(join(dname(os.getcwd()), 'sources.csv'))
    references = sources['reference'].tolist()
    folderpath = join(os.getcwd(), folder_name)

    for root, dirs, files in os.walk(folderpath):
        counter = 1
        for file in files:
            dir_path = os.path.dirname(join(root, file))
            dir_name = os.path.basename(dir_path)
            if 'bodypart' in dir_name:
                dir_name = dir_name.replace('bodypart', 'body_part')
            for ref in references.__iter__():
                if file.find(ref) != -1:
                    suffix = file[file.find(ref):]
                else:
                    suffix = ''
            if counter <= 9:
                ok_name = dir_name  + '0' + str(counter) + suffix
            elif counter >= 10:
                ok_name = dir_name + str(counter) + suffix
            ok_path = join(root, ok_name)
            os.rename(join(root, file), os.path.splitext(ok_path)[0])
            counter += 1
            print(len(os.listdir(dir_path)))
