import cv2
import time
import numpy as np
import pyautogui

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')

video_capture = cv2.VideoCapture(0)  #object to access the camera

c=0

xcoord=0
ycoord=0

pyautogui.moveTo(pyautogui.size()[0]//2,pyautogui.size()[1]//2,duration=0.25)  #Move the cursor to center of the screen


wx,wy=pyautogui.position()   #get the mouse position


while True:
	ret, frame = video_capture.read()            #start reading the live stream using the camera

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		c=c+1
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		arr=list(eyes)
		print(type(arr))
		if(len(arr)>0):
			print("x=",(x+w))
			print("y=",(y+h))
			#conditions to move the cursor pointer
			if(x-xcoord>0 and y-ycoord>0 and wx>0 and wy<768 ):               
				wx=wx-35
				wy=wy+25
				pyautogui.moveTo(wx,wy,duration=0.01)
			if(x-xcoord<0 and y-ycoord>1 and wx<1368 and wy<768):
				wx=wx+35
				wy=wy+25
				pyautogui.moveTo(wx,wy,duration=0.01)
			if(x-xcoord>0 and y-ycoord<0 and wx>0 and wy>0):
				wx=wx-35
				wy=wy-25				
				pyautogui.moveTo(wx,wy,duration=0.01)
			if(x-xcoord<0 and y-ycoord<0 and wx<1368 and wy>0):
				wx=wx+35
				wy=wy-25
				pyautogui.moveTo(wx,wy,duration=0.01)
			xcoord=x
			ycoord=y
			print(pyautogui.position()[0],pyautogui.position()[1])
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	cv2.namedWindow("new",cv2.WINDOW_NORMAL)
	cv2.moveWindow("new",0,0)
	frame=cv2.resize(frame,(1368,768))
	
	#take the screenchot of the screen and get the image of the area where pointer is moving 
	if(c%2==0):
		im=np.array(pyautogui.screenshot())
		cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
		if(wx-100>0 and wx+100<1368 and wy+100<768 and wy-100>0):
			cv2.imshow("image",im[wy-100:wy+100,wx-100:wx+100])
	cv2.imshow('new', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


#release the object
video_capture.release()
cv2.destroyAllWindows()

