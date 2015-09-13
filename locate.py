import cv2
import numpy as np
import picamera
import time
import serial
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

backlight = 4
GPIO.setup(backlight, GPIO.OUT)

########### Initialise Serial Comms. with machine ###########
#ser = serial.Serial('/dev/ttyUSB0', 115200)

###########     Position camera over backlight   ###########
#ser.write('G28\r\n')               ##comment out if camera is already in position
#ser.write('G1 Z25 F5000\r\n')
#ser.write('G1 X145 Y90 F9000\r\n')

###########         Prepare Camera Settings       ###########
camera = picamera.PiCamera()
#camera.vflip = True
camera.exposure = _mode = 'manual'
camera.meter_mode = 'backlit'
camera.brightness = 60
camera.exposure = 100
camera.contrast = 100

#time.sleep(18)     ##comment out if camera is already in position

###########   Display Camera view and save image   ###########
#camera.start_preview()
#time.sleep(3)
#camera.stop_preview()
GPIO.output(backlight, 1)
time.sleep(0.1)
camera.capture('img.jpg')
time.sleep(0.2)
GPIO.output(backlight, 0)

###########      Convert image to grayscale        ###########
im = cv2.imread("img.jpg")
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
cv2.imwrite('grayIMG.jpg', gray)

###########  Convert grayscale to black and white    ###########
ret, threshImg = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)   #([image], [threshold], [colour], [method])
cv2.imwrite('threshImg.jpg', threshImg)

###########  Display output image    ###########
#cv2.imshow("Output Image", threshImg)
#cv2.waitKey(0)


##################################################################

## Find part in image

##################################################################


######### Import image, convert to grayscale  #########

im = cv2.imread('threshImg.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

######### scroll through contours and find one of suitable size  #########
drawID = 0
for count in range(len(contours)):
    area = cv2.contourArea(contours[count])
    #print(area)                         #Display area of each contour found
    if(area >3000 and area < 4000):
        print area,": Model ID: 1"
        chosen = count
        cnt = contours[count]
        drawID = 1
    if(area >33000 and area < 36000):
        print area,": Model ID: 2"
        chosen = count
        cnt = contours[count]
        drawID = 2
    if(drawID <> 0):
######### approximate contour as polygon with 10% deviation  #########

        epsilon = 0.005*cv2.arcLength(cnt, True)            #([contour], [closed contour(T/F)])
        approx = cv2.approxPolyDP(cnt, epsilon, True)

######### approximate contour as bounding rectangle  #########
        rect = cv2.minAreaRect(cnt)
        print rect
        box =cv2.boxPoints(rect)
        box = np.int0(box)
        if(drawID==1):
            im = cv2.drawContours(im, [box], 0, (0, 0, 255), 2)
        elif(drawID==2):
            im = cv2.drawContours(im, [box], 0, (0, 255, 0), 2)
        drawID = 0
#im = cv2.drawContours(im, contours, chosen, (0, 255, 0), 1)

cv2.imshow("Keypoints", im)
cv2.waitKey(0)

cv2.imwrite('FoundImg.jpg', im)
GPIO.cleanup()





