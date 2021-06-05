import random
from imutils.video import FPS
import cv2
import numpy as np


cv2.startWindowThread()
cap = cv2.VideoCapture(0)
fps = FPS().start()
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
_, prev = cap.read()
prev = cv2.flip(prev, 1)
_, new = cap.read()
new = cv2.flip(new, 1)

while True:

    def randomfun():
        Update = random.randrange(180)

        if Update in range(1,89):
            print(((Update/89)*100)-100)
            print("left function called")
        elif Update in range(91,180):
            print(((Update / 89) * 100)-100)
            print("right function called")
        else:
            print("move straight forward")

    _, img = cap.read()
    diff = cv2.absdiff(prev, new)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    diff = cv2.blur(diff, (5, 5))

    _, thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)
    threh = cv2.dilate(thresh, None, 3)
    thresh = cv2.erode(thresh, np.ones((4, 4)), 1)
    contor, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.circle(prev, (20, 450), 5, (0, 0, 255), -1)
    cv2.circle(prev, (610, 450), 5, (0, 0, 255), -1)

    for contors in contor:
        if cv2.contourArea(contors) > 10000:
            faces = face_classifier.detectMultiScale(prev, 1.2, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(prev, (x, y), (x + w, y + h), (0, 255, 0), 2)
                continue
            (x, y, w, h) = cv2.boundingRect(contors)
            (x2, y2), rad = cv2.minEnclosingCircle(contors)
            x2 = int(x2)
            y2 = int(y2)

            k = abs(((450 - 450) * (x2 - 20)) - ((610 - 20) * (y2 - 450))) / (np.square(450 - 450) +np.square (610 - 20))
            x3 = x2 - k * (450 - 450)
            y3 = y2 + k * (610 - 20)
            x3 = int(x3)
            y3 = int(y3)
            cv2.putText(prev, '{}'.format((int(np.sqrt((x2-x3)**2 + (y2-y3)**2))*0.0264583333)),
                            (100, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

            cv2.rectangle(prev, (x, y), (x + w, y + h), (0, 255, 0), 2)
            randomfun()
            cv2.circle(prev, (x2, y2), 5, (0, 0, 255), -1)

            cv2.circle(prev, (x3,y3), 5, (0, 0, 255), -1)
                #cv2.line(prev, (x3,y3), (x2, y2), (255, 0, 0), 4)


    cv2.imshow("orig", prev)



    prev = new
    _, new = cap.read()
    new = cv2.flip(new, 1)
    k = cv2.waitKey(10) & 0xff == ord('q')

    fps.update()

cap.release()
cv2.destroyAllWindows()



