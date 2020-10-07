import numpy as np
import cv2

def empty(a):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 19, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 83, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 102, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 177, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 138, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 249, 255, empty)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(frame,frame,mask=mask)
    greencnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(greencnts)>0:
        green_area = max(greencnts, key=cv2.contourArea)
        (xg,yg,wg,hg) = cv2.boundingRect(green_area)
        cv2.rectangle(frame, (xg,yg), (xg+wg, yg+hg), (0,255,0), 2)

    # Display the resulting frame
    cv2.imshow('frame',imgResult)
    cv2.imshow('mask',frame)
    #cv2.imshow('frame',box)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()