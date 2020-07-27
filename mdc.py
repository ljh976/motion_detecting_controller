import numpy as np
import cv2
import time
import pyautogui
import win32com.client

#control keyboard
wsh = win32com.client.Dispatch("WScript.Shell")
#don't need it anymore
#wsh.AppActivate("")

#remove lag
pyautogui.PAUSE = 0

#set video cam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

focus = 0  # min: 0, max: 255, increment:5
cap.set(28, focus) 
                                          
#bring cascade 
face_cascade = cv2.CascadeClassifier('xmls/Hand.xml') 

#font info
# font 
font = cv2.FONT_HERSHEY_SIMPLEX 
   
# fontScale 
fontScale = 0.75
   
# Blue color in BGR 
color = (150, 255, 0) 
  
# Line thickness of 2 px 
thickness = 2

#for photo index
count = 0

#variables for left or right
temp_x = 0
temp_y = 0
left_counter = 0
right_counter = 0
delay = 0 #prevent multiple input at once

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Convert the image to gray scale 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
      
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))   
    # Performing OTSU threshold 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
    # Appplying dilation on the threshold image 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
    # Finding contours 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,  
                                                     cv2.CHAIN_APPROX_NONE) 
    
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    #face set
    face = face_cascade.detectMultiScale(frame, minSize=(100, 100), maxSize=(600, 600))

    #area of face picture
    picture_area_dict = {
        'x' : 210,
        'y' : 100,
        'w' : 400,
        'h' : 400,
    }
   

    #set up control box
    #up box
    #cv2.rectangle(frame, (200, 10), (450, 115),(255,255,255),2)
    #left box (mirror)
    #cv2.rectangle(frame, (80, 100), (180, 350),(255,255,255),2)
    #right box (mirror)
    #cv2.rectangle(frame, (470, 100), (570, 350),(255,255,255),2)
    #down box
    #cv2.rectangle(frame, (200, 325), (450, 425),(255,255,255),2)
    #control circle
    cv2.circle(frame, (320, 230), 230, (255, 100, 100), 2) 
    
    cv2.putText(frame, str(count), (50, 20), font, fontScale, (150, 0, 200), thickness, cv2.LINE_AA)
    
    #detection part 
    #face part
    if np.any(face):
        #print("Found a face")
        for (x, y, w, h) in face:
            arr = [x, y, x+w, y+h]
            #print(arr)
           # arr = []
 
            mercy = 20
            
            #text org (x, y) 
            org = (x, y-20)
            #draw circle on face
            cv2.rectangle(frame,(x+50,y+50),(x+60,y+60),(255,0,0),2)
            #cv2.putText(frame, '', org, font,  
                   #fontScale, color, thickness, cv2.LINE_AA)
            
            mercy = 50

            if delay == 0:
                #catch up
                if (x+mercy > 200 and x+mercy < 450 and y+mercy > 10 and y+mercy < 115):
                    print("up")
                    pyautogui.keyDown('up')
                    pyautogui.keyUp('up')

                #catch right (mirror)
                elif (x + mercy > 80 and x + mercy  < 180 and y + mercy  > 100 and y + mercy  < 350):
                    print("right")
                    pyautogui.keyDown('right')
                    pyautogui.keyUp('right')
                    
                #catch left (mirror)
                elif (x + mercy  > 470 and x + mercy  < 570 and y + mercy  > 100 and y + mercy  < 350):
                    print("left")
                    pyautogui.keyDown('left')
                    pyautogui.keyUp('left')

                #catch down
                elif (x + mercy  > 200 and x + mercy  < 450 and y + mercy  > 325 and y + mercy  < 425):
                    print("down")
                    pyautogui.keyDown('down')
                    pyautogui.keyUp('down')    
                
                else:
                    print("waiting")
                delay = 0
                
            #preventing multiple input in very short time
            delay += 1
            if delay > 3:
                delay = 0
          
            
            temp_x = x
            temp_y = y

             



    # Display the resulting frame
    cv2.namedWindow("frame", 0);
    cv2.resizeWindow("frame", 800, 680);
    cv2.imshow('frame',frame) #imshow('window name', color)
    if cv2.waitKey(1) & 0xFF == ord('q'):   
        break
   
    
# When everything done, release the capture

cap.release()
cv2.destroyAllWindows()
