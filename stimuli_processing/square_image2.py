 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 12:00:03 2020

@author: francois
"""

import os
from os.path import join
from os.path import basename as bname
from os.path import dirname as dname
#from os.path import relpath
from PIL import Image
from tqdm import tqdm
import imdirect
from taskfunctions import loadimages
from taskfunctions import splitall

FOLDERPATH = '/home/francois/Documents/CCNIB_OFFICIAL_224_vgg16/images'

def square_image(folderpath, length=500):
    '''
    Alt square_image.py using os.makedirs() insead of os.system
    Crops all images in a directory to square aspect ratio and resizes them
    to 'dimensions'. Doesn't overwrite the original image directory.
    '''
    imdirect.monkey_patch()
    pre = str(length)+'_'
    impaths = loadimages(folderpath)
    newpaths = []
    for impath in enumerate(impaths):
        newparts = []
        parts = splitall(impath[1])[1:-1]
        for part in parts:
            newparts.append(pre+part)
    newpaths.append((impath[1], join(*[pre+part for part in splitall(impath[1])]),
                     dname(join(*[pre+part for part in splitall(impath[1])]))))
    for newpath in tqdm(newpaths):
        if not os.path.exists(newpath[2]):
            os.mkdir(newpath[1])
        image = Image.open(newpath[1])
#    newdir = join(dname(folderpath), pre+bname(folderpath)
#    os.system("mkdir {}".format(newdir))
#    for allim in os.walk(os.getcwd()):
#        for picture in tqdm(allim[2]):
#            picpath = join(allim[0], picture)
#            if os.path.isdir(dname(picpath)):
#                subdir = join(newdir, pre+bname(dname(dname(dname(picpath)))))
#                subdir2 = join(subdir, pre+bname(dname(dname(picpath))))
#                subdir3 = join(subdir2, pre+bname(dname(picpath)))
#                print(newdir+'\n', subdir+'\n', subdir2+'\n', subdir3+'\n')
#                os.makedirs(subdir3, exist_ok=True)
#                os.system("mkdir {}".format(subdir), exist_ok=True)
#                os.system("mkdir {}".format(subdir2), exist_ok=True)
#                os.system("mkdir {}".format(subdir3), exist_ok=True)
        if image.mode != 'RGB':
            image.convert("RGB")
        if image.size[0] > image.size[1]:
            image = image.crop(((image.size[0]-image.size[1])/2,
                                0,
                                (image.size[0]+image.size[1])/2,
                                image.size[1]))
        elif image.size[0] < image.size[1]:
            image = image.crop((0,
                                (image.size[1]-image.size[0])/2,
                                image.size[0],
                                (image.size[1]+image.size[0])/2))
        im_resized = image.resize((length, length), Image.ANTIALIAS)
        im_resized.save(newpath[1], 'JPEG', quality=100)
#square_image(dimensions=(500, 500))
