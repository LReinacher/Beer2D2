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
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
            print(cx)

            if cx > 290:
                print("6 Right!")
                motor_functions.set_motors(15, 0)
                
            if 290 >= cx > 260:
                print("5 Right")
                motor_functions.set_motors(15, 3)
                
            if 260 >= cx > 240:
                print("4 Right")
                motor_functions.set_motors(15, 5)

            if 240 >= cx > 220:
                print("3 Right")
                motor_functions.set_motors(15, 8)

            if 220 >= cx > 200:
                print("2 Right")
                motor_functions.set_motors(15, 10)
                
            if 200 >= cx > 190:
                print("1 Right")
                motor_functions.set_motors(15, 12)

            if 190 >= cx > 180:
                print("1 Right")
                motor_functions.set_motors(15, 13)
                
            if 180 >= cx > 170:
                print("1 Right")
                motor_functions.set_motors(15, 14)

            if 150 <= cx <= 170:
                print("On Track!")
                motor_functions.set_motors(15, 15)
                
            if 140 <= cx < 150:
                print("1 Left")
                motor_functions.set_motors(14, 15)

            if 130 <= cx < 140:
                print("1 Left")
                motor_functions.set_motors(13, 15)

            if 120 <= cx < 130:
                print("1 Left")
                motor_functions.set_motors(12, 15)
            
            if 100 <= cx < 120:
                print("2 Left")
                motor_functions.set_motors(10, 15)

            if 80 <= cx < 100:
                print("3 Left")
                motor_functions.set_motors(5, 15)
                
            if 60 <= cx < 80:
                print("4 Left")
                motor_functions.set_motors(6, 15)
                
            if 30 <= cx < 60:
                print("5 Left")
                motor_functions.set_motors(3, 15)

            if cx < 30:
                print("6 Left")
                motor_functions.set_motors(0, 15)

        else:
            print("I don't see the line")
            motor_functions.set_motors(0, 0)

        #Display the resulting frame
        cv2.imshow('frame',crop_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
if __name__ == "__main__":
    main()