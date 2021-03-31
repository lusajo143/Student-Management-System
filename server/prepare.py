#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 04:21:02 2020

@author: lusajo
"""


import PIL.Image as pil
import os
import matplotlib.pyplot as plt
import random
import numpy as np

from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

"""
Obtaining registration numbers
with corresponding images
i.e reg_nos are folders and pictures are those found in reg_nos
"""

path_ = '/media/lusajo/E0D4A130D4A109BC1/projects/sms1/'


def obtain():
    reg_nos = []
    pictures = []
    
    counter = 0
    
    #Number of folders to train used in last layer of model
    No = 0
    for name in os.walk(path_):
        if counter == 0:
            n = name[1]
            if n != []:
                for folder in n:
                    if folder != '__pycache__' and folder != 'resized' and folder !='.ipynb_checkpoints' and folder != 'models':
                        reg_nos.append(folder)
                        
                        print(folder)
                        No+=1
                        
                        for pic in os.walk(path_+folder):
                            pictures.append(pic[2])
        counter+=1
    return reg_nos, pictures,No



"""
Creating labels and loading image names
i.e labels are registration number for individual images
    and are used througout the prepare.py
    images are individual image names
"""

def load_image_label():
    reg_nos, pictures, No = obtain()
    
    
    images = []
    labels = []

    for no, img in zip(reg_nos, pictures):
        for image in img:
            labels.append(no)
            images.append(no+"/"+image)
    
    
    return images, labels, reg_nos,No



"""
Resizing images and saving them to resized directory
"""

# Resize function
def RESIZING(name,resized_images):
    directory = 'resized'

    try:
        image = pil.open(path_+name)
        image.resize((96,96)).save(path_+directory+'/'+name)
        resized_images.append(path_+directory+'/'+name)
    except Exception as e:
        print(e,"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")


def resize():
    images, labels, reg_nos,No = load_image_label()
    
    print('*******************************')
    
    """
    Checking if resized folder is present or not
    if present then skip but if not make directory resized
    """
    
    present = []
    for x in os.walk(path_):
        if 'resized' in x[1]:
            present.append('present')
            
    if len(present) == 0:
        os.mkdir(path_+'resized')
        
    for reg in reg_nos:
        directory = 'resized'
        present2 = []
        print(path_+'resized')
        for folder_name in os.walk(path_+'resized'):
            if reg in folder_name[1]:
                present2.append('present')
        
        if len(present2) == 0:
            os.mkdir(path_+directory+'/'+reg)
    
    # Actual resizing start here
    resized_images = []
    for name in images:
        
        RESIZING(name,resized_images)
        
    
    return resized_images, labels, No



"""
resize and load images using matplotlib
"""

def data():
    resized_images, labels, No = resize()
    
    imgz = []

    for image, folder in zip(resized_images,labels):
        imgz.append(plt.imread(image))
        
    return imgz, labels, No
    

"""
********************************************
Now prepare data for deep learning modelling
********************************************
"""

"""
Change labels into index to allow to_categorical transformation
"""

def change2Index(labels):
    unique = list(set(labels))
    labels2 = []
    index = []
    for ind in range(0,len(unique)):
        index.append(ind)
        
    # Changing into index
    for lab in labels:
        for uniq, ind in zip(unique, index):
            if lab == uniq:
                labels2.append(ind)
    
    return labels2, unique

"""
Shuffle the data
"""
def Shuffle(features, targets):
    c = list(zip(features, targets))
    random.shuffle(c)
    features, targets = zip(*c)
    return features, targets


"""
Normalize features
"""
def Normalize(features):
    return features/255


"""
Get registration number from categorical data
"""

"""
Prepare to get label

def prepare_label():
    with open('reg_nos.txt','r') as p:
        labels = p.read()
    
    index, useless = change2Index(labels)
    

def get_label(labels, categorical):
    unique = list(set(labels))
    index = []
    for ind in range(0,len(list(categorical))):
        index.append(ind)
    
    for cat, ind in zip(list(categorical),index):
        if int(cat) == 1:
            print(unique[ind])
"""

"""
Actual preparation and posting prepared data to model.py
"""

def prepare_data():
    features, targets, No = data()
    
    # Shuffle
    features, targets = Shuffle(features, targets)

    print(len(targets))
    targets, reg_nos = change2Index(targets)
    
    #Save registration numbers used in a model
    with open('reg_nos.txt','w') as p:
        p.write(str(reg_nos))

    #Normalize
    features = Normalize(np.array(features))
    targets = to_categorical(targets)
    #print(features[0])    
    print(len(targets))
    print(len(features))
    
    x_train, x_test, y_train, y_test = train_test_split(np.array(features),
                                                        np.array(targets),
                                                        test_size=0.2,
                                                        random_state=40)
    
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)
    #get_label(l, np.array(targets[17]))
    
    return x_train, x_test, y_train, y_test, No
    
    

if __name__ == '__main__':
    prepare_data()
    #r, l = resize()
    #print("erereerrerere")
    #print(l)
    #print(r)
    #print(r)
    #print(e)
