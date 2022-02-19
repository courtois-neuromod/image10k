#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:10:38 2020

@author: francois
"""

from functools import reduce
import json
from nltk.corpus import wordnet as wn
import numpy as np
import os
from os.path import basename as bname
from os.path import dirname as dname
from os.path import expanduser as xpu
from os.path import join
import pandas as pd
from random import sample
import shutil
from tqdm import tqdm
from typing import Sequence
from taskfunctions import flatten
from taskfunctions import loadimages
from taskfunctions import splitall

IMDIR = '../images'

def get_im10k(IMDIR):
    '''Generates im10k (pandas Dataframe)
       rows = im_names
       cols= ['im_name', 'n_pic', 'dir', 'tags', 'vec']
       
       Parameter(s)
       ------------
       'IMDIR': top image folder ('images' in cnib)
       
       Variables
       ---------
       'impaths': list of all image paths (see 'taskfunctions.py')
       'im_names': list of all im_names, quantity of images in folder,
                             folders paths
           i.e. 'body_part_dog_tail', 'body_beaver', 'face_bveaver',
                'shoe', 'male_teen' etc.
       'all_tags': ordered list of all possible unique tags in 
       'im10k': conversion of im_names to DF.
                   im10k['tags'].items()
       'matrix': numpy array of category membership for all images
                  For each image, category membership is represented by 1 or 0 
                  (1=Category name in path parts; else 0)
       'imdf': conversion from array to DataFrame to create vectors (as rows)
               for each image
               
       Returns
       -------
       'cnib'
           *new columns added during execution:
               'tags': list of all folders' names (as categories) from IMDIR
                            to image dir
               'vec': tuple where each boolean value represents category membership
               *categories are ordered as 'all_tags'
        DATA ACCESS:
            cnib.loc['concept_name']['datas']['npic', 'dir', 'tags', 'vec']
       '''                                  
    def get_data():
        impaths = loadimages(IMDIR)
        im_names = []
        for impath in impaths:
            if 'object' in impath:
                name = bname(dname(impath))
            else:
                name = bname(dname(impath))+' '+\
                                            bname(dname(dname(impath)))
            im_names.append((name, len(os.listdir(dname(impath))),
                             dname(impath)))
        im_names = sorted(list(dict.fromkeys(list(im_names))))
                
        im10k = pd.DataFrame(im_names, columns=['im_name', 'n_pic', 'dir'])
        im10k.index = im10k.im_name
        im10k['tags'] = [splitall(folderpath[1].split(IMDIR,
                                                      maxsplit=1)[1])[1:-1]
                        for folderpath in im10k['dir'].items()]
        all_tags = sorted(list(dict.fromkeys(flatten([tags[1] 
                                      for tags in \
                                      im10k['tags'].items()]))))
        matrix = np.array([[bool(tags[1].__contains__(tag))
                          for tag in all_tags]
                          for tags in im10k['tags'].items()])
        imdf = pd.DataFrame(matrix,
                            index=[name for name in im10k['im_name']],
                            columns=all_tags)
        im10k['vec'] = [row[1] for row in imdf.iterrows()]
        im10k = im10k.drop(columns='im_name')
        return im10k
    im10k = get_data()
    def categories(kword):
        '''Categorizes the DF according to neuromod categories using "tags"'''
        return pd.DataFrame([im10k.loc[row[0]]
                            for row in im10k.iterrows()
                            if kword in im10k.loc[row[0]].tags])
    cnib = pd.DataFrame(zip(all_tags,
                            [categories(im10k, tag) for tag in all_tags]),
                        columns=['concepts', 'datas'],
                        index=all_tags)
    cnib = cnib.drop(columns='concepts')
    return cnib

cnib = get_im10k(IMDIR)

cnib = cnib.drop(columns='concepts')
cnib2 = pd.DataFrame.from_csv('../docs/cnib_full.csv')
#dataframe navigation example
# alpha = list(cnib.loc['female']['datas']['vec']['adult_female'])
cnib.to_csv('../docs/cnib_full.csv')

def check_syns():
    prefix = '/home/francois/Desktop/neuromod_image_bank/images/'
#    wn_syns = list(wn.all_synsets())
#    im10k_list = pd.read_excel('../docs/all_synsets.xlsx')['synsets'].tolist()
#    im10k_syns = [wn.synset(syn) for syn in im10k_list]
#    valid = sorted([name for name in names if name not in labels])
#    invalid = sorted([label for label in labels if label not in names])
    impaths = loadimages(IMDIR)
    im_names = sorted(list(dict.fromkeys((set(tuple([('_'.join((bname(dname(dname(impath))),
                                                 bname(dname(impath)))),
                                       len(os.listdir(dname(impath))),
                                       tuple(splitall(impath.strip(prefix))[2:-1]))
                                      for impath in impaths]))))))

    im10k = pd.DataFrame(im_names,
                               columns=['im_name', 'n_pics', 'tags'])
    taglist = []
    for ind in range(len(im10k['tags'])):
        taglist.append(im10k['n_pics'][ind]*im10k['tags'][ind])
    taglist = flatten(taglist)
    im_name_names = sorted([(taglist.count(im_name[2]),
                  im_name[0]) for im_name in im_names])
    table = list(dict.fromkeys(taglist))
    wordcloud = WordCloud().generate_from_frequencies(taglist)

# Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    taglist = [tag[1]*im10k['n_pics'][tag][0] for tag in enumerate(im10k['tags'])]
    wordlist = []
    matrix = [[label in im10k['tags'] for label in taglist]
              for tags in im10k['tags']]
    matrix = np.array([[int([tag for tag 
                             in im10k['tags']].__contains__(label))
                             for label in taglist]
                             for tag in im10k['tags']])
    return im10k

def embeddings(IMDIR):
    embeds = []
    alllabels =  list(dict.fromkeys([(bname(join(allimages[0], category)),
                                      len(os.listdir(join(allimages[0],
                                                          category))),
                                      join(allimages[0], category))
                                  for allimages in os.walk(IMDIR)
                                  for category in allimages[1]]))
    impaths = loadimages(IMDIR)
    # tuple(item name, quantity, directory path)
    im_names = list(dict.fromkeys(list((bname(dname(impath)),
                                            len(os.listdir(dname(impath))),
                                            dname(impath)) 
                                           for impath in impaths)))
    cnames = [im_name[0] for im_name in im_names]
    categories = list(dict.fromkeys([label for label in alllabels 
                                     if label not in im_names]))
    
    for categ in categories:
        embeds.append(os.listdir(categ[2]),)
    cnames_sizes = [im_name[1] for im_name in im_names]
    pathparts = [(im_name, splitall(im_name[2].split(IMDIR, maxsplit=1)[1])[1:-1])
                 for im_name in im_names]

    for allim in os.walk(FOLDERPATH):
        for folder in allim[1]:
            fpath = join(allim[0], folder)  
    col_names = [(colnames, coldata)[0] for (colnames, coldata) in imdf.iteritems()]
    row_names = [(index, row)[0] for (index, row) in imdf.iterrows()]
    for row in row_names:
        for col in col_names:

def get_im10k(IMDIR):
    '''Generates Dataframe (rows=image im_names, cols=categories).
       Image im_names = Name of image folder
                       Individual inanimate objects and specific
                       animal pictures
                       i.e. 'body_part_dog_tail', 'body_beaver', 
                            'face_bveaver', 'shoe' etc.
       Categories = Name of each folder in path to image folder
                   Category names as their WordNet synset would be typed
                   (without POS and number).
       For each image im_name, membership in a category is reoresented by 1 or
       0 (1=Category name in path parts; else 0).
       Next step: Split into smaller matrices for practical use.'''
    #All directory names in the bank (categories and items)
    alllabels =  list(dict.fromkeys([(bname(join(allimages[0], category)),
                                      len(os.listdir(join(allimages[0],
                                                          category))),
                                      join(allimages[0], category))
                                  for allimages in os.walk(IMDIR)
                                  for category in allimages[1]]))
    impaths = loadimages(IMDIR)
    # tuple(item name, quantity, directory path)
    im_names = list(dict.fromkeys(list((bname(dname(impath)),
                                            len(os.listdir(dname(impath))),
                                            dname(impath)) 
                                           for impath in impaths)))
    cnames = [im_name[0] for im_name in im_names]
    categories = list(dict.fromkeys([label for label in alllabels 
                                     if label not in im_names]))
    cnames_sizes = [im_name[1] for im_name in im_names]
    pathparts = [(im_name, splitall(im_name[2].split(IMDIR, maxsplit=1)[1])[1:-1])
                 for im_name in im_names]
    
    matrix = np.array([[int(parts[1].__contains__(label[0]))
                        for label in categories]
                       for parts in pathparts])
    imdf = pd.DataFrame(matrix, index=cnames,
                        columns=categories)
    imdf['n_pics'] = cnames_sizes
#    
#    col_names = [(colnames, coldata)[0] for (colnames, coldata) in imdf.iteritems()]
#    row_names = [(index, row)[0] for (index, row) in imdf.iterrows()]
#    for row in row_names:
#        for col in col_names:
#            if imdf[col][row] == 1:
#                imdf[col][row] = 1*imdf['n_pics'][row]
#    cat_parts = [splitall(cat.split(IMDIR, maxsplit=1)[1])[1:]
#                 for cat in categories]
#    
#    categs = [[(imdf[part].index(), imdf[part].sum()) for part in cat_parts]
#              for cat_part in cat_parts]
#    imdf['categs'] = categs
    return imdf

            if imdf[col][row] == 1:
                imdf[col][row] = 1*imdf['n_pics'][row]
    cat_parts = [splitall(cat.split(IMDIR, maxsplit=1)[1])[1:]
                 for cat in categories]
    
    categs = [[(imdf[part].index(), imdf[part].sum()) for part in cat_parts]
              for cat_part in cat_parts]
    imdf['categs'] = categs
    return imdf

def get_trees(syn_list):
    all_trees = []
    for syn in syn_list:
        hyp = lambda s:s.hypernyms()
        syn_tree = syn.tree(hyp)
        all_trees.append((syn, syn_tree))
#    trees_dict = dict(all_trees)
#    tlists = list(trees_dict.values())
#    tlists = [flatten(this[1]) for this in tlists]
#    tlists = [[those for those in these] for these in tlists]
    return all_trees

def str2syn(string_list):
    syn_list = []
    all_synsets = pd.read_excel('/home/francois/Desktop/CCNIB_OFFICIAL/docs/all_synsets.xlsx')['synsets'].tolist()
    all_synsets = list(dict.fromkeys(all_synsets))
    for string in string_list:
        for syn in enumerate(all_synsets):
            if string == syn[1].split('.')[0]:
                syn_list.append(wn.synset(syn[1]))
    return syn_list

IMDIR = '/home/francois/Desktop/neuromod_image_bank/images'
def validation(IMDIR):
    all_labels =  list(dict.fromkeys([(bname(join(allimages[0], category)),
                                      join(allimages[0], category))
                                     for allimages in os.walk(IMDIR)
                                     for category in allimages[1]]))
    impaths = loadimages(IMDIR)
    # tuple(item name, quantity, directory path)
    # im_name names are the image labels per se and don't match WN synsets
    im_names = list(dict.fromkeys(list((bname(dname(impath)),
                                            len(os.listdir(dname(impath))),
                                            dname(impath)) 
                                            for impath in impaths)))
    cnames = [im_name[0] for im_name in im_names]
    # Categories are the labels for all im_names >= 1 level higher than 
    # the image labels. These do match WN synsets.

    categories = list(dict.fromkeys([label for label in all_labels if label[0] not in cnames]))
    cat_syns = str2syn([cat[0] for cat in categories])
    cat_syns_trees = get_trees(cat_syns)
    cat_parts = [splitall(cat[1].split(IMDIR, maxsplit=1)[1])[1:]
                 for cat in categories]
    cat_parts_syns = [str2syn(part) for part in cat_parts]
    all_vecs = []
    for parts_syn in enumerate(cat_parts_syns):
        vec = []
        for tag in parts_syn[1]:
            validation = bool(str(cat_syns_trees[parts_syn[0]][1]).__contains__(tag.name()))
            vec.append((tag.name(),validation))  
        all_vecs.append(vec)
    big_tuple = tuple(zip(cat_syns, cat_syns_trees, cat_parts_syns, all_vecs))
    big_df = pd.DataFrame(list(big_tuple), columns=['synset', 'tree', 'tags',
                                              'in trees'])
#    validation_df = pd.DataFrame(all_vecs,
#                             index=cat_syns)
    return big_df

big_df = validation(IMDIR)

def checkup(valids):
#    valids = validation()
    outsiders = []
    for vec in enumerate(valids):
        for tag in vec[1]:
            if tag.__contains__(False):
                outsiders.append(tag)
    return outsiders
#    validation_df = pd.DataFrame((cat_parts_syns,cat_syns_trees,valids),
#                                 index=cat_syns)
check = checkup(valids)    

def get_inv():
    '''Converts category membership value (bool) to number (int) of images 
       for each im_name. Returns the sum of each column as the total of
       pictures representing each im_name.'''
    inv = get_im10k()
    new_matrix = []
    rowslist = list(inv.iterrows())
    quantities = [row[0][1] for row in rowslist]
    vectors = [row[1] for row in rowslist]
    for vec in enumerate(vectors):
        newvector = []
        for value in vec[1]:
            newvalue = value*quantities[vec[0]]
            newvector.append(newvalue)
        new_matrix.append(newvector)
    new_matrix = pd.DataFrame(np.array(new_matrix), columns=inv.columns)
    totals = new_matrix.sum(axis=0)
    return totals

new_matrix = get_inv()

new_matrix.to_excel(join(dname(IMDIR), 'new_matrix.xlsx'))
count = np.array(flatten([new_matrix[col].sum() for col in new_matrix.columns]))
count = list(count)
im_name_count = dict(zip(alllabels, count))
im_names = pd.DataFrame.from_dict(im_name_count, orient='index')
inventory = pd.DataFrame(np.array(count), columns=alllabels)
def get_counts():
    newvec = get_inv()
    newvecs = pd.DataFrame(newvec)
    col_totals = []
    for col in newvecs.columns:
        col_totals.append(newvecs[col].sum())
    final_count = pd.DataFrame(col_totals)
    return final_count

final_count = get_counts()

def get_to_increase(IMDIR):
    picdirs = []
    for allim in os.walk(IMDIR):
        for pic in allim[2]:
            picdir = dname(join(IMDIR, pic))
            if len(os.listdir(picdir)) <= 20:
                picdirs.append(picdir)
    picdirs = list(dict.fromkeys(picdirs))
    return picdirs

picdirs = get_to_increase(IMDIR)

def notjpg():
    '''Assert extension uniformity for all images'''
    notjpg = []
    for allim in os.walk(IMDIR):
        for pic in allim[2]:
            if not pic.endswith('.jpg'):
                notjpg.append(pic)
    return notjpg

def imdict():
    fnames = []
    flists = []
    for allim in os.walk(IMDIR):
        for folder in allim[1]:
            fnames.append(folder)
            fpath = join(allim[0], folder)
            flists.append(os.listdir(fpath))
    imdict = dict(zip(fnames, flists))
    return imdict
imagedict = imdict()


def getitdone(imdir=IMDIR):
    '''Categorization/Inventoring by neuroscience approved semantic categories'''
    updirs = []
    for allpics in os.walk(IMDIR):
        for picture in allpics[2]:
            if os.path.isfile(join(allpics[0], picture)):
                updirs.append(dname(join(allpics[0], picture)))
    upnames = [bname(updir) for updir in updirs]
    updirs = list(dict.fromkeys(updirs))
#    for updir in enumerate(updirs):
    categories = {'abod' : [], 'aface' : [], 'abpart' : [], 'hface' : [],
                  'hbpart' : [], 'obj' : []}
    animalbody = []
    animalface = []
    animalbodypart = []
    humanbodypart = []
    humanface = []
    inanimateobject = []
    for folder in enumerate(updirs):
        if 'animal' and 'body' in folder[1] and \
        'body_part' and 'object' not in folder[1]:
            categories['abod'].append((folder[1], bname(folder[1]),
                                       splitall(folder[1].split(IMDIR)[1][1:])))
            animalbody.append(folder[1])
        if 'animal' and 'face' in folder[1] and \
        'body_part' and 'body' and 'object' and 'human' not in folder[1]:
            categories['aface'].append((folder[1], bname(folder[1]),
                                        splitall(folder[1].split(IMDIR)[1][1:])))
            animalface.append(folder[1])
        if 'animal' and 'body_part' in folder[1] and \
        'face' and 'object' and 'human' not in folder[1]:
            categories['abpart'].append((folder[1], bname(folder[1]),
                                         splitall(folder[1].split(IMDIR)[1][1:])))
            animalbodypart.append(folder[1])
        if 'human' and 'face' in folder[1] and \
        'body_part' and 'animal' not in folder[1]:
            categories['hface'].append((folder[1], bname(folder[1]),
                                        splitall(folder[1].split(IMDIR)[1][1:])))
            humanface.append(folder[1])
        if 'human' and 'body_part' in folder[1] and 'animal' not in folder[1]:
            categories['hbpart'].append((folder[1], bname(folder[1]),
                                         splitall(folder[1].split(IMDIR)[1][1:])))
            humanbodypart.append(folder[1])
        if 'object' in folder[1] and 'animal' not in folder[1]:
            categories['obj'].append((folder[1], bname(folder[1]),
                                      splitall(folder[1].split(IMDIR)[1][1:])))
            inanimateobject.append(folder[1])
    return categories

categories = getitdone()

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    big = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], big)
        parent[folders[-1]] = subdir
    return big
big = get_directory_structure(IMDIR)

big2 = json.dumps(big, indent=1)
loaded_big = json.loads(big2)
with open('big.json', 'w') as fp:
    json.dump(loaded_big, fp)
loaded_big['rating'] #Output 3.5
type(r) #Output str
type(loaded_r) #Output dict

categs = getitdone(IMDIR)
categs = json.dumps(categs)
loaded_categs = json.loads(categs)
with open('categs2.json', 'w') as fp:
    json.dump(loaded_categs, fp)

def image10k():
    unique3 =  list(dict.fromkeys([bname(join(allimages[0], category))
                                   for allimages in os.walk(IMDIR)
                                   for category in allimages[1]]))
    impaths = [join(allimages[0], image)
               for allimages in os.walk(IMDIR)
               for image in allimages[2]]
    humans = []
    animals = []
    objects = []
    for allimages in os.walk(IMDIR):
        for image in allimages[2]:
            impath = join(allimages[0], image)
            parts = splitall(impath)[6:]
            if parts.__contains__('human') == True:
                humans.append(impath)
            if parts.__contains__('animal') == True:
                animals.append(impath)
            if parts.__contains__('object') == True:
                objects.append(impath)
    hdirs = list(dict.fromkeys([dname(impath) for impath in humans]))
    adirs = list(dict.fromkeys([dname(impath) for impath in animals]))
    
    odirs = list(dict.fromkeys([dname(impath) for impath in objects]))
            
    humans = [join(allimages[0], image)
              for allimages in os.walk(IMDIR)
              for image in allimages[2]
              if 'human' in join(allimages[0], image)]
###############################################################################
#en_allsyns = list(wn.all_synsets())
#en_names = [syn for syn in en_allsyns if syn.pos() == 'n']
#animalsyns = pd.read_excel(join(dname(IMDIR),'docs', 'animal_synsets.xlsx'))['animal_synsets'].to_list()
#a_syns = [syn.name() for syn in en_names if syn.name() in animalsyns]
#diff = [name for name in animalsyns if name not in a_syns]