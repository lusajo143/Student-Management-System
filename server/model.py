#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 03:24:24 2020

@author: lusajo
"""

"""
*************************
Model Training and saving
*************************
"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from keras.models import model_from_json
import tensorflow as tf
import logging
tf.get_logger().setLevel(logging.ERROR)

import os

import prepare

path_ = '/media/lusajo/E0D4A130D4A109BC1/projects/sms1/'


"""
model architecture
"""
"""def architecture():
    model = Sequential()
    
    model.add(Conv2D(64, (3,3), activation='relu', input_shape=(96,96,3)))
    model.add(MaxPool2D(pool_size=(3,3)))
    
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPool2D(pool_size=(3,3)))
    
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPool2D(pool_size=(3,3)))
    
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPool2D(pool_size=(3,3)))
    
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPool2D(pool_size=(3,3)))
    
    model.add(Flatten())
    
    model.add(Dense(1000,activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(1000,activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(700,activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(500,activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(300,activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(100,activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(50,activation='relu'))
    
    model.add(Dense(3,activation='softmax'))
    
    return model"""
    

"""
Delete a model in every single training
"""

def delete_model():
    try:
        os.remove('model.json')
        os.remove('model.h5')
    except Exception:
        print('Already deleted')
    
def architecture(No):
    
    delete_model()
    
    model = Sequential()

    model.add(Conv2D(64,(3,3),activation='relu', input_shape=(96,96,3)))
    
    model.add(MaxPool2D(pool_size=(3,3)))
    
    model.add(Conv2D(64,(3,3),activation='relu'))
    
    model.add(MaxPool2D(pool_size=(3,3)))
    
    model.add(Conv2D(64,(3,3),activation='relu'))
    
    model.add(MaxPool2D(pool_size=(3,3)))
    
    model.add(Flatten())
    
    model.add(Dense(3000,activation='relu'))
    
    model.add(Dropout(0.5))
    
    model.add(Dense(2500,activation='relu'))
    
    model.add(Dropout(0.5))
    
    model.add(Dense(1500,activation='relu'))
    
    model.add(Dropout(0.5))
    
    model.add(Dense(1000,activation='relu'))
    
    model.add(Dense(500,activation='relu'))
    
    model.add(Dense(No,activation='softmax'))
    
    return model
"""
Compile model
"""
def Compile(No):
    
    model = architecture(No)
    
    model.compile(optimizer='adam', loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model
    

"""
Training the model
"""
def train():
    
    x_train, x_test, y_train, y_test, No = prepare.prepare_data()

    model = Compile(No)
    
    model.fit(x_train,
              y_train,
              epochs=10,
              validation_split=0.2,
              batch_size=100)
    
    results = model.evaluate(x_test,y_test)
    
    model_json = model.to_json()
    with open('model.json','w') as fl:
        fl.write(model_json)

    model.save_weights('model.h5')
    
    loss, accuracy = results[0], results[1]
    
    return loss, accuracy

"""
Save a model for future use
"""

def save_model(name=123456789):
    path = path_+'models/'+str(name)
    try:
        os.mkdir(path)
    except Exception as e:
        print(e)
    
    # Load model
    json = open('model.json','r')
    mjson = json.read()
    json.close()
    
    modela = model_from_json(mjson)
    modela.load_weights('model.h5')
    
    # Save
    model_json = modela.to_json()
    with open(path+'/model.json','w') as fl:
        fl.write(model_json)
        
    # Copy reg_nos.txt
    with open('reg_nos.txt','r') as p:
        reg_txt = p.read()
    with open(path_+'models/'+str(name)+'/reg_nos.txt','w') as p:
        p.write(reg_txt)

    modela.save_weights(path+'/model.h5')
    


if __name__ == '__main__':
    train()
    save_model()

