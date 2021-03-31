#!/home/lusajo/anaconda3/bin/python


import cv2
import socket
import os
import model
from keras.models import model_from_json
from threading import Thread
import json

import ast


"""
**********************************************************************************************
                                        For opencv
                                                
                                Capturing images and cropping
**********************************************************************************************
"""
class cv:

    def launch(self,con,name):

        #create a folder
        try:
            os.mkdir(name)
        except Exception as e:
            print('[::] ERROR')
            print(e)

        counter = 0
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        classifier = cv2.CascadeClassifier('haar.xml')

        video = cv2.VideoCapture(0)

        while (counter<200):
            #video = cv2.VideoCapture("rtsp://192.168.1.101:5554/camera", cv2.CAP_FFMPEG)
            #video = cv2.VideoCapture(0)
            video.set(cv2.CAP_PROP_BUFFERSIZE, 2)

            state, frame = video.read()
            if state:
                faces = classifier.detectMultiScale(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),scaleFactor=1.10, minNeighbors=10)

                for x, y, w, h in faces:
                    frame = cv2.rectangle(frame,(x,y), (x+w, y+h), (0,255,0), 3)
                    cv2.imwrite(name+'/'+str(counter)+'.jpg',frame[y:y+h,x:x+w])
                    counter+=1
                    #Send percent to the client app
                    self.send(con,counter/2)
                    #Thread(target=self.send(), args=(con,counter,)).start()

                cv2.imshow("image",frame)
                #con.send(str(counter).ecode('utf-8'))
                #Thread(send(),args=(con,counter,)).start()
                cv2.waitKey(1)
                if counter == 100 or counter == 101:
                    cv2.destroyAllWindows()
            else:
                print('not')

    def send(self,con,counter):
        print(counter)
        con.send((str(counter)+'\n').encode('utf-8'))

    def get_name(self,name):
        self.name = name

    def get_reg_nos(self,my_list,values):
        index = []
        largest = 0
        largest_index = 0
        
        #Create index for reffering back to values
        for x in range(0,len(my_list)):
            index.append(x)

        #Obtain largest index and value
        for x in range(0,len(index)):
            if values[0][x] > largest:
                largest = values[0][x]
                largest_index = x
        return largest, my_list[largest_index]

    # Checking if attendance taking need to be stopped
    def check(self,con):
        status = con.recv(1024).decode('utf-8')
        if status.split('###')[1] == 'stop':
            self.status = status.split('###')[1]

    #launching camera and getting attendance done
    def start_attendance(self,con,time,current_time):
        print(time)
        self.status = 'start'

        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        classifier = cv2.CascadeClassifier('haar.xml')

        dp = deep()
        
        video = cv2.VideoCapture(0)

        Thread(target=self.check,args=(con,)).start()

        # Dictionary for results
        attendance = []

        while self.status == 'start':
            #video = cv2.VideoCapture("rtsp://192.168.1.101:5554/camera", cv2.CAP_FFMPEG)
            #video = cv2.VideoCapture(0)
            video.set(cv2.CAP_PROP_BUFFERSIZE, 2)

            state, frame = video.read()
            if state:
                faces = classifier.detectMultiScale(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),scaleFactor=1.03, minNeighbors=10)

                for x, y, w, h in faces:
                    frame = cv2.rectangle(frame,(x,y), (x+w, y+h), (0,255,0), 3)
                    #print(frame[y:y+h,x+w])
                    frame2 = frame[y:y+h, x:x+w]
                    cv2.imwrite('name.jpg',frame2)
                    frame2 = cv2.imread('name.jpg')
                    results = dp.predict(time,frame2,con)
                    #Get usernames i.e Registration numbers
                    my_list = ['mayai','T/UDOM/2019/00424']
                    
                    with open('reg_nos.txt','r') as p:
                        my_list = p.read()
                    
                    my_list = ast.literal_eval(my_list)
                    
                    high_score, username = self.get_reg_nos(my_list,results)
                    print('This is',username)
                    print('Accuracy',str(high_score))

                    '''
                    ************************************
                    Creating json file to send to client
                    ************************************
                    '''
                    dict_ = {
                            'reg':username,
                            'accuracy':high_score
                            }
                    print(dict_)
                    # Checking if the present person is found in the list already
                    found = False
                    for x in attendance:
                        if x['reg'] == dict_['reg']:
                            found = True
                            break

                    # Add person to the list
                    if not found:
                        attendance.append(dict_)

                    #Send percent to the client app
                    #Thread(target=self.send(), args=(con,counter,)).start()

                cv2.imshow("image",frame)
                #con.send(str(counter).ecode('utf-8'))
                #Thread(send(),args=(con,counter,)).start()
                cv2.waitKey(1)
                if self.status == 'stop':
                    cv2.destroyAllWindows()
        con.send((str(attendance)+'\n').encode('utf-8'))
        print('Done sending')

"""
**********************************************************************************************************
                                                For Deep learnig

                                       Train a model from model.py getting loss and 
                                        accuracy to evaluate a model in javafx client
**********************************************************************************************************
"""
class deep:

    def train(self):
        self.loss, self.accuracy = model.train()

        print('server Loss: '+str(self.loss))
        print('Server Accuracy: '+str(self.accuracy))

        return self.loss, self.accuracy

    def save(self,time):
        model.save_model(time)
 
    def predict(self,time,frame,con):
        frame = cv2.resize(frame, dsize=(96, 96), interpolation=cv2.INTER_CUBIC)
        print('***************************************************',str(frame.shape))
        """
        Normalize frame
        """
        frame = frame/255
        
        json = open('models/'+str(time)+'/model.json','r')
        mjson = json.read()
        json.close()
        
        loaded_model = model_from_json(mjson)
        loaded_model.load_weights('models/'+str(time)+'/model.h5')
        
        """
        Compile loaded model
        """
        loaded_model.compile(loss='binary_crossentropy',metrics=['accuracy'],optimizer='adam')
        
        return loaded_model.predict(frame.reshape(1,96,96,3))

"""
*********************************************************************************************************
                                                For socket connections

                                            Handles all server client connections
*********************************************************************************************************
"""

class sockets:

    def __init__(self):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.s.bind(('',143))
            self.s.listen()
            print('bind complete')
        except:
            print('Failed to bind socket')


    def wait(self):
        while True:
            print('new conn')
            con, addr = self.s.accept()
            #start listening for incomming messages
            self.listen(con)

    def listen(self,con):
        while True:
            print('listening')
            info = con.recv(1024).decode('utf-8')
            print(info)

            info = info.split('###')
            print(info)

            """
            Check routine for either register or otherwise
            """
            #trying if empty data received should skip
            if info == ['']:
                break
            else:
                """
                **************************
                For name then registration
                **************************
                """
                
                if len(info) == 3 and info[1] == 'name':

                    #Get username
                    name = ''
                    if info[1] == 'name':
                        name = info[2]

                    info = con.recv(1024).decode('utf-8')
                    print(info)

                    info = info.split('###')
                    print(info)
                    print(len(info))
                    #for launching camera
                    try:
                        if info[1] == 'start_camera':
                            self.start_cv(con,name)
                        else:
                            print('Not start camera')
                        break

                    except:
                        break
            
                
                #*******************************
                #Saving model to model directory
                #*******************************
                
                elif len(info) == 3 and info[1] == 'save':
                    time = info[2]
                    print(time)

                    deepL = deep()
                    deepL.save(time)

                    con.send(b'Done saving successfully')
                    break
                    
                #*********************
                #For taking attendance
                #*********************

                elif len(info) == 4 and info[1] == 'attendance':
                    time = info[3]
                    current_time = info[2]
                    print(time)
                    print('##########################################')
                    
                    opencv = cv()
                    opencv.start_attendance(con,time,current_time)

                    break
                
                #******************
                #For training model
                #******************
                
                else:
                    if info[1] == 'start_train':
                        deepL = deep()
                        loss, accuracy = deepL.train()
                        dict_metrics = {
                                'loss':str(loss),
                                'accuracy':str(accuracy)
                                }
                        con.send((str(loss)+'###'+str(accuracy)+'\n').encode('utf-8'))
                        print(dict_metrics)
                        break
                    


    def start_cv(self,con,name):
        camera = cv()
        camera.launch(con,name)

if __name__ == "__main__":
    sock = sockets()
    sock.wait()
    #s = cv()
    #s.launch()
