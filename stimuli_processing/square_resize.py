# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 16:19:43 2019

@author: Francois
"""

import os
from os import getcwd
from os import listdir as ls
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
from PIL import Image
from tqdm import tqdm
import imdirect

def square_resize(folderpath, dimensions=224):
    '''
    Resizes square aspect-ratio images to desired dimensions.
    Doesn't overwrite the images; instead, a prefix corresponding
    to 'dimensions' parameter is added before each image's and folder's
    name (i.e: folder 'aquatic_mammal' --> '500_aquatic_mammal').

	Parameters
	----------
	fname: type = str
		Name of category images directory (ex: 'outdoor_sport')

	dimensions: type = int
		Square side length in pixels

	Returns
    -------
    None'''
    imdirect.monkey_patch() #Fixes unexpected image rotation while saving
    prefix = str(dimensions)+'_'
    nfpath = join(dname(folderpath), prefix+bname(folderpath))
    os.system("mkdir {}".format(nfpath))
    for categs in ls(join(getcwd(), fname)):
        newcatpath = join(nfpath, prefix+categs)
        os.system("mkdir {}".format(newcatpath))
        for synname in ls(join(getcwd(), fname, categs)):
            os.system("mkdir {}".format(join(newcatpath, prefix+synname)))
            for allim in os.walk(join(getcwd(), fname, categs, synname)):
                for subd in allim[1]:
                    os.system("mkdir {}".format(join(newcatpath,
                                                     prefix+synname,
                                                     prefix+subd)))
                for im_name in tqdm(allim[2]):
                    impath = join(allim[0], im_name)
                    image = Image.open(impath)
                    newpath = impath.replace(fname, prefix+fname, 1)
                    newpath = newpath.replace(categs, prefix+categs, 1)
                    newpath = newpath.replace(synname, prefix+synname, 1)
                    newpath = newpath.replace(bname(dname(newpath)),
                                              prefix+bname(dname(newpath)),
                                              1)
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
                    im_resized = image.resize((dimensions, dimensions),
                                              Image.ANTIALIAS)
                    im_resized.save(join(dname(newpath), prefix+im_name),
                                    'JPEG',
                                    quality=90)
