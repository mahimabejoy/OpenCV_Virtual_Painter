import cv2
import numpy as np
import HandTrackingModule as htm
import time

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

drawColor =(0,0,0)
brushsize=20
erasersize=50

pTime=0

imgcanvas=np.zeros((720,1280,3),np.uint8)


detector=htm.handDetector(detectionCon=0.8)

while True:
    success,img=cap.read()
    img=cv2.flip(img,1)

    cv2.rectangle(img,(20,10),(300,100),(0,0,255),cv2.FILLED)
    cv2.rectangle(img,(310,10),(640,100),(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(650,10),(950,100),(255,0,0),cv2.FILLED)
    cv2.rectangle(img,(960,10),(1280,100),(0,0,0))
    cv2.putText(img,'Eraser',(1050,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
    


#1.find hand landmarks

    img=detector.findHands(img)
    imlist=detector.findPosition(img,draw=False)
   
    if len(imlist)!=0:
        # print(imlist)

        x1,y1=imlist[8][1:]
        x2,y2=imlist[12][1:]
        # print("index finger :", x1,y1)
        # print("middle finger :",x2,y2 )
#2.find which finger is up



        fingers=detector.fingersUp()
        # print(fingers)


#3.selction mode - two finger is up

        if fingers[1] and fingers[2]:
            print("selection mode")

            xp,yp=0,0

            if y1<100:
                if 20<x1<300:
                    drawColor=(0,0,255)

                elif 310<x1<640:
                    drawColor=(0,255,0)
                elif 650<x1<950:
                    drawColor=(255,0,0)
                elif 960<x1<1280:
                    drawColor=(0,0,0)



                

            cv2.circle(img,(x2,y2),20,drawColor,cv2.FILLED)



#4.drawing mode - one is up( index finger )

        if fingers[1] and fingers[2]==False:
            print("drawing mode")

            if xp==0 and yp==0:
                xp,yp=x1,y1

            xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,erasersize)
                cv2.line(imgcanvas,(xp,yp),(x1,y1),drawColor,erasersize)


            else:



                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushsize)
                cv2.line(imgcanvas,(xp,yp),(x1,y1),drawColor,brushsize)






            cv2.circle(img,(x1,y1),20,drawColor,cv2.FILLED)


    imggray= cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
    _,imginv=cv2.threshold(imggray,50,255,cv2.THRESH_BINARY_INV)
    imginv=cv2.cvtColor(imginv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imginv)
    img=cv2.bitwise_or(img,imgcanvas)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,str(int(fps)),(50,200),cv2.FONT_HERSHEY_COMPLEX,5,(0,255,255),5)


    img=cv2.addWeighted(img,1,imgcanvas,0.5,0)

    # cv2.imshow("canvas",imgcanvas)
    cv2.imshow('image',img)
    cv2.waitKey(1)


