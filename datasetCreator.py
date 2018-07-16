import cv2
import sqlite3
import numpy as np

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);

def insertOrUpdate(Id,Name,Age,Gender,Criminal):
    conn=sqlite3.connect("Face.db")
    cmd="select * from People where ID="+str(Id)
    cursor=conn.execute(cmd)
    #cursor.execute("select * from People where ID="+str(Id))
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if isRecordExist==1:
        cmd="update People set Name="+str(Name)+" where ID="+str(Id)
    else:
        cmd="insert into People(ID,Name,Age,Gender,CriminalRecords)values("+str(Id)+","+str(Name)+","+str(Age)+","+str(Gender)+","+str(Criminal)+")"
    cursor=conn.execute(cmd)
    conn.commit()
    conn.close()
id1=raw_input('Enter user id')
name=raw_input('Enter your name')
Age=raw_input('Enter the age:')
gender=raw_input('Enter the gender')
criminal=raw_input('Criminal Background?')
insertOrUpdate(id1,name,Age,gender,criminal)
SampleNum=0
while True:
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        SampleNum=SampleNum+1
        cv2.imwrite("dataSet/User."+str(id1)+"."+str(SampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.waitKey(100)
    cv2.imshow("Face",img)
    cv2.waitKey(100)
##    if SampleNum>20:
##        break
cam.release()
cv2.destroyAllWindows()
