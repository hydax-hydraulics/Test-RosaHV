from tkinter import *
import tkinter as tk
from PIL import ImageTk,Image
from imutils.video import FPS
import cv2
import numpy as np      
import threading
from datetime import datetime
from time import strftime
import time
import os,sys
import csv 

root = tk.Tk()
root.resizable(0,0)
root.geometry("790x400+10+10")
root.configure(background="white")


def switch():
    global is_on
    if is_on:
        start_button.config(image=stop)
        threading.Thread(target=videoLoop, args=(videoloop_stop,)).start()
        #threading.Thread(target=function).start()
        
        is_on=False
    else:
        start_button.config(image=start)
        videoloop_stop[0] = True
        is_on=True


def videoLoop(self):
    cap = cv2.VideoCapture(0)
    cap.set(3, 300)
    cap.set(4, 400)
    
    fps = FPS().start()
    
    _, prev = cap.read()
    prev = cv2.flip(prev, 1)
    _, new = cap.read()
    new = cv2.flip(new, 1)
    while True:
        _, frame = cap.read()
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
        #image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(prev)
        imgtk = ImageTk.PhotoImage(image = img)
        
        panel = tk.Label(image=imgtk)
        panel.image = img
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
    #print("Hello")

################################################################################################################################
    

def setup1():
    
    global x
    global y
    global list1
    window = Toplevel()
    window.resizable(0,0)
    window.geometry("790x400+10+10")
    window.configure(background="white")
    
    f1 = Frame(window, bg="white")
    f1.place(relwidth=1, relheight=1)
    label=Label(f1,text="R O S A - Hv",font=("calibrie"," 68"),fg="#ffc0cb",background="white")
    label.place(relx=-0.25,relwidth=1.5,relheight=0.2)
    
   
    
    def clock():
        
        clocktime = time.strftime('%H:%M:%S %p')
        curr_time.config(text=clocktime)
        curr_time.after(1000,clock)
        return clock
    
    label1 = Label(window,text = "Current Time",font = ("calibrie", 20), fg="#ffc0cb",background="white")
    label1.place(relx=0.11,rely=0.40,relwidth=0.25,relheight=0.15)

    curr_time =Label(window, font ='calibrie', text = 'Current Time', fg = 'black' ,bg ='white',highlightcolor= '#ffc0cb',highlightbackground= '#ffc0cb')
    curr_time.place(relx=0.5,rely=0.40,relwidth=0.25,relheight=0.15)
    clock()
    
    

    global a
    global b
    global c
    label1 = Label(window,text = "Start Time", width=20,font = ("calibrie", 20), fg="#ffc0cb",background="white")
    label1.place(relx=0.11,rely=0.60,relwidth=0.2,relheight=0.15)
    
    hrs= StringVar()
    a=Spinbox(window, from_ = 1, to =24,textvariable = hrs, width =2, font = 'arial 12',format="%02.0f")
    a.place(relx=0.5,rely=0.60,relwidth=0.09,relheight=0.1)
    hrs.set('00')
    mins= StringVar()
    b=Spinbox(window, from_ = 0, to =59,textvariable = mins, width =2, font = 'arial 12',format="%02.0f")
    b.place(relx=0.6,rely=0.60,relwidth=0.09,relheight=0.1)
    mins.set('00')
    sec = StringVar()
    c=Spinbox(window, from_ = 0, to =59, textvariable = sec, width = 2, font = 'arial 12',format="%02.0f")
    c.place(relx=0.7,rely=0.60,relwidth=0.09,relheight=0.1)
    sec.set('00')
    
   
    
    def condition():
        now = datetime.now()
        currenttime = now.strftime("%M%S")
        currenttime1 = int(currenttime)
        print("currenttime:",currenttime1)
        list1 = []
        str1 = ""
        #data1=a.get()       
        data2=b.get()
        data3=c.get()
        list1.append(data2)
        list1.append(data3)
        for ele in list1:
            str1 += ele
        print("starttime:",str1)
        starttime1 = int(str1)
    
        if (currenttime1 >= starttime1):
            getvalue()
        else:
            print("wait")
    
    
    global x
    global y
    mins= StringVar()
    x=Spinbox(window, from_ = 1, to =60,textvariable = mins, width =2, font = 'arial 12',format="%02.0f")
    x.place(relx=0.5,rely=0.80,relwidth=0.09,relheight=0.1)
    mins.set('00')
    
    sec = StringVar()
    y=Spinbox(window, from_ = 0, to =60, textvariable = sec, width = 2, font = 'arial 12',format="%02.0f")
    y.place(relx=0.6,rely=0.80,relwidth=0.09,relheight=0.1)
    sec.set('00')
    
    
    
    def runtime():
        global list1
        list1=[]
        list2=[]
        
        
        data = x.get()
        data1 = y.get()
        data2 = a.get()
        data3 = b.get()
        data4 = c.get()
        
        #print("Spin box values:",data +":"+data1+ "," +data2 + ":" + data3 + ":" + data3)
        list1.append(data)
        list1.append(data1)
        
        list2.append(data2)
        list2.append(data3)
        list2.append(data4)
        
        delim = ":"
        res1 = ""
        res = ""
        for ele1 in list1:
            res1 = res1 + ele1 + delim
        result1 = res1.rstrip(':')
        
        list1 = result1
        
        for ele in list2:
            res = res + ele + delim
        result = res.rstrip(':')
        print("list2:",result)
        list2 = result
        
        
        row_list=[list1]
        row_list1=[list2]
        ff=("/home/pi/Desktop/Hydax/ROSA-Hv/store.csv")
        with open(ff,"w",newline="") as file:
              writer = csv.writer(file)
              writer.writerow(row_list)
              writer.writerow(row_list1)
        
    
    label1 = Label(window,text = "Run Time",font = ("calibrie", 20), fg="#ffc0cb",background="white")
    label1.place(relx=0.11,rely=0.80,relwidth=0.2,relheight=0.15)
    
    
    button = Button(window, text='Load', width=10, command=lambda:[runtime(),condition()])
    button.place(relx=0.8,rely=0.60,relwidth=0.13,relheight=0.1)
    
    
################################################################################################################################    

videoloop_stop = [False]

is_on = True

start = ImageTk.PhotoImage(file="START.png")
stop = ImageTk.PhotoImage(file="STOP.png")


f1 = Frame(root, bg="white")
f1.place(relwidth=1, relheight=1)
label=Label(f1,text="R O S A - Hv",font=("calibrie"," 68"),fg="#ffc0cb",background="white")
label.place(relx=-0.25,relwidth=1.5,relheight=0.2)




button2 = tk.Button(
    root, text = "Setup", bg="#fff", font=("", 50), command = setup1)
#path2 = "SetUp.png"
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

def clock1():
    clocktime = time.strftime('%H:%M:%S')
    curr_time.config(text=clocktime)
    curr_time.after(1000,clock1)
    return clock1
    

label1 = Label(root,text = "Current Time",font = ("calibrie", 14), fg="#ffc0cb",background="white")
label1.place(relx=0.6,rely=0.19,relwidth=0.2,relheight=0.05)   
curr_time =Label(root, font ='calibrie', text = 'Current Time', fg = 'black' ,bg ='white',highlightcolor= '#ffc0cb',highlightbackground= '#ffc0cb')
curr_time.place(relx=0.8,rely=0.19,relwidth=0.2,relheight=0.05)
clock1()


def getvalue():
    
    global canvas
    global canvas1
    global num
    global num1
    global num2
    filepath=("/home/pi/Desktop/Hydax/ROSA-Hv/store.csv")
    
    
    with open(filepath,"r",newline="") as file:
        reader = csv.reader(file)
        for col in reader:
            for row in reader:
                canvas = Label(root,text = col,font = ("calibrie"), fg="black",bg="white")
                canvas.place(relx=0.8,rely=0.25,relwidth=0.2,relheight=0.05)
                canvas1 = Label(root,text = row,font = ("calibrie"), fg="black",bg="white")
                canvas1.place(relx=0.8,rely=0.30,relwidth=0.2,relheight=0.05)
    

def function():
    
    global state
    global mins
    global secs
    global minutes
    global seconds
    
    
    num = canvas["text"]
    num1 = num.split(':')
    num2 = num1
    for i in range(0,len(num2)):
        num1[i] = int(num2[i])
    num2 = (num2)
    
    state = False
    minutes = num2[0]
    
    seconds = num2[1]
    
    mins = num2[0]
    secs = num2[1]
    
    
    

def countdown():
    global state
    global mins
    global secs
    if state == True:
        if (mins == 0) and (secs == 0):
            state = False
        else:
            canvas.config(text = "%02d:%02d" % (mins , secs))
            if secs == 0:
                mins -= 1
                secs = 60
            else:
                secs -= 1
    root.after(1000,countdown)

def function1():
    global state
    if state == False:
        state = True
        mins = minutes
        secs = seconds
        countdown()



label1 = Label(root,text = "Run Time",font = ("calibrie", 14), fg="#ffc0cb",bg="white")
label1.place(relx=0.6,rely=0.25,relwidth=0.2,relheight=0.05)

label2 = Label(root,text = "Start Time",font = ("calibrie", 14), fg="#ffc0cb",bg="white")
label2.place(relx=0.6,rely=0.30,relwidth=0.2,relheight=0.05)  

#button5= Button(root, text = "Get", bg="#fff", font=("", 0),command= lambda:[function(),function1()]) 
#button5.place(relx=0.11,rely=0.85,relwidth=0.2,relheight=0.15)

start_button= Button(root, image = start, bg="#fff", font=("", 50),command= lambda:[switch(),function(),function1()]) 

start_button.place(relx=0.11,rely=0.25,relwidth=0.2,relheight=0.15)



root.mainloop()