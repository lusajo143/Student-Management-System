#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 02:08:03 2020

@author: lusajo
"""


import numpy as np
import os
import cv2
from keras.models import model_from_json


def load_model():
    json = open('model.json','r')
    mjson = json.read()
    json.close()

    loaded_model = model_from_json(mjson)
    loaded_model.load_weights('model.h5')
    
    """
    Compile loaded model
    """
    loaded_model.compile(loss='binary_crossentropy',metrics=['accuracy'],optimizer='adam')
    
    return loaded_model

def predict(frame,con, model):
    frame = np.asarray(frame)
    frame = cv2.resize(frame, dsize=(54, 140), interpolation=cv2.INTER_CUBIC)
    """
    Normalize frame
    """
    frame = frame/255
    
    return model.predict(frame)
    

if __name__ == "__main__":
    load_model()
    predict()
