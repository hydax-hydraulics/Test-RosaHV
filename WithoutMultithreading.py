from PIL import Image 
from PIL import ImageTk
import PIL.Image
from tkinter import *
import tkinter as tk
import threading
#from datetime import datetime
#from time import strftime
import time
from imutils.video import FPS
import cv2
#import os,sys
#import csv            
import numpy as np 

def switch():
    global is_on
    if is_on:
        start_button.config(image=stop)
        threading.Thread(target=videoLoop, args=(videoloop_stop,)).start()
        #threading.Thread(target=timer).start()
        is_on=False
    else:
        start_button.config(image=start)
        videoloop_stop[0] = True
        is_on=True

def videoLoop(self):
    global image
    cap = cv2.VideoCapture(0)
    cap.set(3, 300)
    cap.set(4, 400)
   

    fps = FPS().start()
    _, prev = cap.read()
    prev = cv2.flip(prev, 1)
    _, new = cap.read()
    new = cv2.flip(new, 1)
    while True:
        _, frame= cap.read()
        diff = cv2.absdiff(prev, new)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        diff = cv2.blur(diff, (5, 5))
        _, thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, 3)
        thresh = cv2.erode(thresh, np.ones((4, 4)), 1)
        contor, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contors in contor:
            if cv2.contourArea(contors) > 10000:
                (x, y, w, h) = cv2.boundingRect(contors)
                cv2.rectangle(prev, (x, y), (x + w, y + h), (0, 255, 0), 2)

        image = PIL.Image.fromarray(prev)
        image = ImageTk.PhotoImage(image)
        panel = tk.Label(image=image)
        panel.image = image
        panel.place(x=350, y=140)

        prev = new
        _, new = cap.read()
        new = cv2.flip(new, 1)
        if cv2.waitKey(1) == 27:
            break
        fps.update()



        if videoloop_stop[0]:
            # if switcher tells to stop then we switch it again and stop videoloop
            videoloop_stop[0] = False
            panel.destroy()
            break
    cap.release()
    cv2.destroyAllWindows()

videoloop_stop = [False]


root = tk.Tk()
root.resizable(0,0)
root.geometry("790x400+10+10")
root.configure(background="white")

global is_on
is_on = True
start = ImageTk.PhotoImage(file="START.png")
stop = ImageTk.PhotoImage(file="STOP.png")


f1 = Frame(root, bg="white")
f1.place(relwidth=1, relheight=1)
label=Label(f1,text="R O S A - Hv",font=("calibrie"," 68"),fg="#ffc0cb",background="white")
label.place(relx=-0.25,relwidth=1.5,relheight=0.2)


start_button= Button(
    root, image = start, bg="#fff", font=("", 50),
    command= switch) 

start_button.place(relx=0.11,rely=0.25,relwidth=0.2,relheight=0.15)

button2 = tk.Button(
    root, text = "Setup", bg="#fff", font=("", 50), command = setup1)
path2 = "SetUp.png"
img2 = ImageTk.PhotoImage(file="SetUp.png")
my2 = Label(root, image=img2)
my2.image = img2
button2.config(image=img2)
button2.place(relx=0.11,rely=0.40,relwidth=0.2,relheight=0.15)

button3 = tk.Button(
    root, text = "tools", bg="#fff", font=("", 50))
#path3 = "TOOLS.png"
img3 = ImageTk.PhotoImage(file="TOOLS.png")
my3 = Label(root, image=img3)
my3.image = img3
button3.config(image=img3)
button3.place(relx=0.11,rely=0.55,relwidth=0.2,relheight=0.15)

button4 = tk.Button(
    root, text = "help", bg="#fff", font=("", 50))
#path4 = "HELP.png"
img4 = ImageTk.PhotoImage(file="HELP.png")
my4 = Label(root, image=img4)
my4.image = img4
button4.config(image=img4)
button4.place(relx=0.11,rely=0.70,relwidth=0.2,relheight=0.15)


root.mainloop()