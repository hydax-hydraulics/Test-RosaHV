# import libraries of python OpenCV 
# where its functionality
from imutils.video import FPS
import cv2 
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
fps = FPS().start()

while True:
    def speak(text):
        tts=gTTS(text=text, lang="en")
        filename = "voice.mp3"
        #tts.save(filename)
        playsound.playsound(filename)
    
    _, img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 4)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.imshow("img",img)
        speak("Excuse Me")
        fps.update()
    k=cv2.waitKey(10) & 0xff == ord('q')
   
cap.release()
cv2.destroyAllWindows()



    
    
    


