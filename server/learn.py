#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 10:48:52 2020

@author: lusajo
"""

import tensorflow
from tensorflow import keras
from keras.models import Sequential
import cv2
import numpy as np
import os

import model.py

imgList = []
def get_image(img,name):
    #cv2.imwrite(str(name)+".jpg", img)
    print(np.asarray(img))
    

