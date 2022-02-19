# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 19:06:24 2019

@author: Francois
"""
import os
from os.path import basename as bname
from os.path import join
from os.path import splitext
import pandas as pd
from random import sample
from typing import Sequence
from nltk.corpus import wordnet as wn
imdir = '../images'

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return tuple(allparts)
    
def flatten(nestedlst):
    """
    Description
    -----------
    Returns unidimensional list from nested list using list comprehension.

    Parameters
    ----------
        nestedlst: list containing other lists etc.

    Variables
    ---------
        bottomElem: type = str
        sublist: type = list

    Return
    ------
        flatlst: unidimensional list
    """
    flatlst = [bottomElem for sublist in nestedlst
               for bottomElem in (flatten(sublist)
               if (isinstance(sublist, Sequence)
               and not isinstance(sublist, str))
               else [sublist])]
    return flatlst

def loadimages(impath='../images'):
    '''
    Description
    -----------
    Lists the full relative path of all '.jpeg' files in a directory.

    Parameters
    ----------
    imdir: type = str
        Name of the directory containing the images.

    Return
    ------
    imlist: type = list
        1D list containing all '.jpeg' files' full relative paths
    '''
    imlist = []
    for allimages in os.walk(impath):
        for image in allimages[2]:
            impath = join(allimages[0], image)
            if os.path.isfile(impath) and impath.endswith('.jpg'):
                imlist.append(impath)
    return imlist

def sampling(lst, nsize, nsamples, exclusives=[]):
    '''
    Description
    -----------
    Draws desired amount of samples of desired size without
    replacement from population.
    Output can be either list or dict.

    Parameters
    ----------
    lst: type=list
        Input list from where population elements are sampled.

    nsize: type=int
        Size of each sample.

    nsamples: type=int
        Number of samples to be drawn from 'lst'

    exclusives: type=list or type=dict
    '''
    samples = list(range(nsamples))#len=16
    inds = sample(range(0, len(lst)), nsize*nsamples)#len = 640
    exclusives = flatten(exclusives)
    for item in range(len(exclusives)):
        if item in flatten(inds) and item in exclusives:
            inds.remove(item)
    samples = [inds[ind:ind+nsize] for ind in range(0, len(inds), nsize)]
    try:
        for exclusive in exclusives:
            error_msg = 'non-exlusive samples'
            shared_items = []
            for item in flatten(samples):
                if item in flatten(exclusive):
                    shared_items.append(item)
        len(shared_items) != 0
        print(error_msg)
    except:
        return samples

def get_answers(rundict):
    '''
    Returns the answers based on keys pressed by subject
    in a list and adds this list as 'Answers' in 'self.rundict'.
    '''
    answerlist = []
    encnames = [rundict['encstims'][stim][0]
                for stim in range(len(rundict['encstims']))]
    encpos = [rundict['encstims'][stim][1]
              for stim in range(len(rundict['encstims']))]
    recnames = [rundict['recstims'][stim][0]
                for stim in range(len(rundict['recstims']))]
    recpos = [rundict['recstims'][stim][1]
              for stim in range(len(rundict['recstims']))]
    for ans in range(len(encnames)):
        if recnames[ans] in encnames:
            if recpos[ans] == encpos[ans]:
                answerlist.append('HIT')
            else:
                answerlist.append('WS')
        elif recnames[ans] not in encnames and recpos[ans] != 'None':
            answerlist.append('FA')
        else:
            answerlist.append('CR')
    rundict.update({'answers':answerlist})

def con2syn(word):
    try:
        ind = list(char.isnumeric() for char in str(word)).index(True)
        return word.split(sep=word[ind], maxsplit=1)[0]
    except: 
        return word
def clean_image_names(name):
    if not name.isalpha():
        n_ind = [char.isnumeric() for char in iter(name)]
        name = name.split(name[n_ind.index(True)])[0]
        return name


def q_rename(fpath, prefix=str()):
    count = 1
    lst = []
    for image in os.listdir(fpath):
#        prefix = '_'.join(reversed(list(splitall(fpath.split(imdir)[0])[-3:])))
        if count <=9:
            suffix = ''.join(['0'+str(count), splitext(image)[1]])
        else:
            suffix = ''.join([str(count), splitext(image)[1]])
        os.rename(join(fpath, image), join(fpath, prefix+suffix))
        count += 1
    return lst
#        os.rename(join(fpath, image), join(fpath, prefix+suffix))

# q_rename('/home/francois/Desktop/cnib_22july2020/images/animate_being/human/face/male/elder')
