
# coding: utf-8
# In[1]:


import os
import numpy as np
import cv2
import persons
import time
from datetime import datetime
import mysql.connector
# from config import db_config
import argparse

def find_zones(x,y,w,h):
    if x < 0.5*w:
        if y < 0.5*h:
            return 'A'
        else:
            return 'C'
    else:
        if y < 0.5*h:
            return 'B'
        else:
            return 'D'

#Initializing the counts
people_in = 0
people_out = 0

parser = argparse.ArgumentParser(description='people counting')
parser.add_argument('path', type=str,help='path of video file')
args = parser.parse_args()

#Reading the video
cap = cv2.VideoCapture(str(args.path))

#print cap.isOpened()
w = cap.get(3)
h = cap.get(4)
frameArea = h*w
areaTH = frameArea/100
#print 'Area Threshold', areaTH, "Frame Area", frameArea

mid_h = int(0.5*w)
mid_v = int(0.5*h)

#Defining the lines for entry and exit
line_up = int(.9*w)
line_down   = int(.9*w)

up_limit =   int(1*w)
down_limit = int(.1*w)

#print "Red line y:",str(line_down)
#print "Blue line y:", str(line_up)
line_down_color = (255,0,0)
line_up_color = (0,0,255)
pt1 =  [line_up, 0];
pt2 =  [line_up, h];
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [line_down, 0];
pt4 =  [line_down, h];
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [up_limit,0];
pt6 =  [up_limit,h];
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [down_limit,0];
pt8 =  [down_limit,h];
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

pt9 =  [mid_h,0];
pt10 =  [mid_h,h];
pts_L5 = np.array([pt9,pt10], np.int32)
pts_L5 = pts_L5.reshape((-1,1,2))
pt11 =  [0,mid_v];
pt12 =  [w,mid_v];
pts_L6 = np.array([pt11,pt12], np.int32)
pts_L6 = pts_L6.reshape((-1,1,2))


#Backgroud Subtraction
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

#Defining kernels for erosion and dilation
kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

#Variables
font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 50
pid = 1

#MySQL Database Connection Parameters
arvind_cnx_str = {'host': 'f1.cemnrzna330w.ap-south-1.rds.amazonaws.com',
    'username': 'runcy',
    'password': 'enternow123',
    'db': 'f1'}
con = mysql.connector.connect(host=arvind_cnx_str['host'], user=arvind_cnx_str['username'],
                                        password=arvind_cnx_str['password'], database=arvind_cnx_str['db'])
cursor = con.cursor(True)


while(cap.isOpened()):
    p_in = 0
    p_out = 0
    # capture the frames
    ret, frame = cap.read()
    #print frame.shape

    for i in persons:
        i.age_one() #age every person one frame
    #########################
    #   PRE-PROPROCESSING   #
    #########################
    
    #Calling the background substraction function
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    #Binarization of the image using a manually decided threshold
    try:
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        ret,imBin2 = cv2.threshold(fgmask2,230,255,cv2.THRESH_BINARY)
        #Opening (erode->dilate) 
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) 
        mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        print 'UP:',cnt_up
        print 'DOWN:',cnt_down
        break
    
    #   CONTOUR IDENTIFICATION
    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    _, contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv2.contourArea(cnt)
        if (area > areaTH): #& (area < 4*areaTH):
            #################
            #   TRACKING    #
            #################
            
            #Calculating the moments of the contours
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)

            #print cx,cy
            new = True

            if cx in range(down_limit,up_limit):
                sql = "INSERT INTO Coordinates (TimeStamp,CX,CY) VALUES('{}',{},{});".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),cx,cy)
                cursor.execute(sql)

                for i in persons:
                    if abs(cx-i.getX()) <= 150 and abs(cy-i.getY()) <= 150:
                        # The object is close to one already detected before
                        new = False
                        zone = find_zones(cx,cy,frame.shape[1],frame.shape[0])
                        i.updateCoords(cx,cy,zone) #Updating co-ordinates and reseting age
                        if i.going_UP(line_down,line_up) == True:
                            people_in += 1;
                            p_in += 1;
                            #print "ID:",i.getId(),'crossed going up at',time.strftime("%c")
                        elif i.going_DOWN(line_down,line_up) == True:
                            people_out += 1;
                            p_out += 1;
                            #print "ID:",i.getId(),'crossed going down at',time.strftime("%c")
                        break
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getX() < down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getX() > up_limit:
                            i.setDone()
                    
                    if i.timedOut():
                        #Creating a list of persons
                        index = persons.index(i)
                        persons.pop(index)
                        del i     #Releasing the memory
                    
                if new == True:
                    p = Persons.MyPerson(pid,cx,cy, max_p_age)
                    persons.append(p)
                    pid += 1     

            #################
            #   Drawing the rectangular box     #
            #################
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
            #cv2.drawContours(frame, cnt, -1, (0,255,0), 3)
            
    #END for cnt in contours0
    if p_in + p_out != 0:
        sql = "INSERT INTO PeopleCounter (TimeStamp,Pers_In,Pers_Out) VALUES('{}',{},{});".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),p_in,p_out)
        cursor.execute(sql)

    for i in persons:
        if len(i.getTracks()) >= 2:
            if i.zones[-1] != i.zones[-2]:
                sql = "INSERT INTO Zones (TimeStamp,Old_Zone,New_Zone) VALUES('{}','{}','{}');".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),i.zones[-2],i.zones[-1])
                cursor.execute(sql)
                
        elif len(i.getTracks()) == 1:
            sql = "INSERT INTO Zones (TimeStamp,Old_Zone,New_Zone) VALUES('{}',NULL,'{}');".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),i.zones[-1])
            cursor.execute(sql)

    #################
    #   Putting the lines and texts#
    #################
    str_up = 'People In: '+ str(people_in)
    str_down = 'People Out: '+ str(people_out)
    frame = cv2.polylines(frame,[pts_L1],False,line_up_color,thickness=2)
    cv2.polylines(frame,[pts_L5],False,(0,0,0),thickness=1)
    cv2.polylines(frame,[pts_L6],False,(0,0,0),thickness=1)
    #frame = cv2.polylines(frame,[pts_L2],False,line_down_color,thickness=2)
    #frame = cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
    #frame = cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
    #cv2.putText(frame, str_up ,(int(.9*w),90),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_up ,(1000,80),font,0.5,(0,255,0),1,cv2.LINE_AA)
    #cv2.putText(frame, str_down ,(int(.1*w),90),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_down ,(1000,100),font,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(frame, 'zone A',(70,70),font,1,(0,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, 'zone B',(mid_h+70,70),font,1,(0,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, 'zone C',(70,mid_v+70),font,1,(0,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, 'zone D',(mid_h+70,mid_v+70),font,1,(0,255,255),2,cv2.LINE_AA)

    cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Frame',1000,1000)
    #producer.send('count',str(people_out)+','+str(people_in))
    cv2.imshow('Frame',frame) 
   # cv2.namedWindow('Back_sub',cv2.WINDOW_NORMAL)
   # cv2.resizeWindow('Back_sub',500,500)
    #cv2.imshow('Back_sub',fgmask)
   # cv2.namedWindow('Mask',cv2.WINDOW_NORMAL)
   # cv2.resizeWindow('Mask',500,500)
    #cv2.imshow('Mask',mask)    
    con.commit()
    #Closing the window 
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
#END while(cap.isOpened())
    
#################
#   Closing the windows    #
#################
con.close()
cap.release()
cv2.destroyAllWindows()
#controlling the flow
#signal(SIGPIPE,SIG_DFL)
