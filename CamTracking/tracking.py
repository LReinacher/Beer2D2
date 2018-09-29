import numpy as np
import cv2
import imutils
import pyzbar
import settings
from datetime import datetime
import system_vars


def main():
    import MotorControl.motor_functions as motor_functions
    import CamTracking.webcam_functions as webcam_functions
    video_capture = cv2.VideoCapture(-1)
    video_capture.set(3, 160)
    video_capture.set(4, 120)

    line_last_seen = 0

    while(True):

        # Capture the frames
        ret, frame = video_capture.read()

        qr_frame = imutils.resize(frame, width=400)

        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(qr_frame)

        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(qr_frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            webcam_functions.found_barcode(barcodeData)

        # Crop the image
        crop_img = frame[30:160, 0:480]

        # Convert to grayscale
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # Gaussian blur
        blur = cv2.GaussianBlur(gray,(5,5),0)

        # Color thresholding
        _,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

        # Find the contours of the frame
        _,contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # Find the biggest contour (if detected)
        if len(contours) > 0:
            line_last_seen = datetime.now().timestamp()
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
            #print(cx)

            if cx > 290:
                #print("6 Righ7t!")
                #motor_functions.set_motors(15, 0)
                motor_functions.execute_directive('right_8', 'line')
                
            if 290 >= cx > 260:
                #print("5 Right")
                #motor_functions.set_motors(15, 3)
                motor_functions.execute_directive('right_7', 'line')
                
            if 260 >= cx > 240:
                #print("4 Right")
                #motor_functions.set_motors(15, 5)
                motor_functions.execute_directive('right_6', 'line')

            if 240 >= cx > 220:
                #print("3 Right")
                #motor_functions.set_motors(15, 8)
                motor_functions.execute_directive('right_5', 'line')

            if 220 >= cx > 200:
                #print("2 Right")
                #motor_functions.set_motors(15, 10)
                motor_functions.execute_directive('right_4', 'line')
                
            if 200 >= cx > 190:
                #print("1 Right")
                #motor_functions.set_motors(15, 12)
                motor_functions.execute_directive('right_3', 'line')

            if 190 >= cx > 180:
                #print("1 Right")
                #motor_functions.set_motors(15, 13)
                motor_functions.execute_directive('right_2', 'line')
                
            if 180 >= cx > 170:
                #print("1 Right")
                #motor_functions.set_motors(15, 14)
                motor_functions.execute_directive('right_1', 'line')

            if 150 <= cx <= 170:
                #print("On Track!")
                #motor_functions.set_motors(15, 15)
                motor_functions.execute_directive('forwards', 'line')
                print(system_vars.colorcode['info'] + "INFO: ON LINE" + system_vars.colorcode['reset'])
                
            if 140 <= cx < 150:
                #print("1 Left")
                #motor_functions.set_motors(14, 15)
                motor_functions.execute_directive('left_1', 'line')

            if 130 <= cx < 140:
                #print("1 Left")
                #motor_functions.set_motors(13, 15)
                motor_functions.execute_directive('left_2', 'line')

            if 120 <= cx < 130:
                #print("1 Left")
                #motor_functions.set_motors(12, 15)
                motor_functions.execute_directive('left_3', 'line')
            
            if 100 <= cx < 120:
                #print("2 Left")
                #motor_functions.set_motors(10, 15)
                motor_functions.execute_directive('left_4', 'line')

            if 80 <= cx < 100:
                #print("3 Left")
                #motor_functions.set_motors(5, 15)
                motor_functions.execute_directive('left_5', 'line')

                
            if 60 <= cx < 80:
                #print("4 Left")
                #motor_functions.set_motors(6, 15)
                motor_functions.execute_directive('left_6', 'line')
                
            if 30 <= cx < 60:
                #print("5 Left")
                #motor_functions.set_motors(3, 15)
                motor_functions.execute_directive('left_7', 'line')

            if cx < 30:
                #print("6 Left")
                #motor_functions.set_motors(0, 15)
                motor_functions.execute_directive('left_8', 'line')

        else:
            print(system_vars.colorcode['error'] + "WARNING: LINE NOT IN VISIBLE!" + system_vars.colorcode['reset'])
            #motor_functions.set_motors(0, 0)
            if datetime.now().timestamp() - line_last_seen < 5:
                motor_functions.execute_directive('spin', 'line')
            else:
                motor_functions.execute_directive('stop', 'line')
                print(system_vars.colorcode['error'] + "ERROR: LINE LOST!" + system_vars.colorcode['reset'])

        #Display the resulting frame
        if settings.gui_enabled:
            cv2.imshow('frame', crop_img)
            cv2.imshow("Barcode Scanner", qr_frame)


if __name__ == "__main__":
    main()