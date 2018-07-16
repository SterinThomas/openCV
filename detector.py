import cv2
import numpy as np
import sqlite3
import webbrowser
from datetime import datetime


faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);
rec=cv2.createLBPHFaceRecognizer();
rec.load("recognizer\\trainingData.yml")

def getProfile(id):
    conn=sqlite3.connect("Face.db")
    cmd="select * from People where ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
        a=row[0]
        #print profile
    conn.close()
    return profile
font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,2,1,0,4)
while True:
    conn=sqlite3.connect("Face.db")
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        print id
        profile=getProfile(id)
        a=str(datetime.now().time())

        if profile!=None:
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[1]),(x,y+h+30),font,255)
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[2]),(x,y+h+60),font,255)
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[3]),(x,y+h+90),font,255)
            cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[4]),(x,y+h+120),font,255)
            cv2.cv.PutText(cv2.cv.fromarray(img),a,(x,y+h+150),font,255)
##        if str(profile[4])=="Yes":
##            webbrowser.open_new("1.php?id="+str(a))
        conn.close()    
    cv2.imshow("Face",img)
    if( cv2.waitKey(1)==ord('q')):
        break;
cam.release()
cv2.destroyAllWindows()
