import numpy as np
import cv2


def main():
    import MotorControl.motor_functions as motor_functions
    video_capture = cv2.VideoCapture(-1)
    video_capture.set(3, 160)
    video_capture.set(4, 120)

    while(True):

        # Capture the frames
        ret, frame = video_capture.read()

        # Crop the image
        crop_img = frame[60:120, 0:160]

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
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
            #print(cx)

            if cx > 150:
                print("4 Left!")
                motor_functions.set_motors(0, 20)

            if 150 >= cx > 130:
                print("3 Left")
                motor_functions.set_motors(5, 20)

            if 130 >= cx > 110:
                print("2 Left")
                motor_functions.set_motors(10, 20)

            if 110 >= cx > 90:
                print("1 Left")
                motor_functions.set_motors(15, 20)

            if 70 <= cx <= 90:
                print("On Track!")
                motor_functions.set_motors(20, 20)

            if 50 <= cx < 70:
                print("1 Right")
                motor_functions.set_motors(20, 15)

            if 30 <= cx < 50:
                print("2 Right")
                motor_functions.set_motors(20, 10)

            if 10 <= cx < 30:
                print("3 Right")
                motor_functions.set_motors(20, 5)

            if cx < 10:
                print("4 Right")
                motor_functions.set_motors(20, 0)

        else:
            print("I don't see the line")
            motor_functions.set_motors(0, 0)

        #Display the resulting frame
        cv2.imshow('frame',crop_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break