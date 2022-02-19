#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 09:08:02 2019

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

def square_image(dimensions=(500, 500)):
    '''
    Crops all images in a directory to square aspect ratio and resizes them
    to 'dimensions'. Doesn't overwrite the original image directory.
    '''
    imdirect.monkey_patch()
    pre = str(dimensions[0])+'_'
    newdir = join(dname(os.getcwd()), pre+bname(os.getcwd()))
    os.system("mkdir {}".format(newdir))
    for allim in os.walk(os.getcwd()):
        for picture in tqdm(allim[2]):
            picpath = join(allim[0], picture)
            if os.path.isdir(dname(picpath)):
                subdir = join(newdir, pre+bname(dname(dname(dname(picpath)))))
                subdir2 = join(subdir, pre+bname(dname(dname(picpath))))
                subdir3 = join(subdir2, pre+bname(dname(picpath)))
                print(newdir+'\n', subdir+'\n', subdir2+'\n', subdir3+'\n')
                os.system("mkdir {}".format(subdir))
                os.system("mkdir {}".format(subdir2))
                os.system("mkdir {}".format(subdir3))
            image = Image.open(picpath)
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
            im_resized = image.resize(dimensions, Image.ANTIALIAS)
            im_resized.save(join(subdir3, pre+picture), 'JPEG', quality=90)
square_image(dimensions=(500, 500))
