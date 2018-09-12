import cv2
import imutils
from pyzbar import pyzbar
import handler
import glob_vars


def main():
    motorControl = glob_vars.motorControlInstance

    video_capture = cv2.VideoCapture(-1)

    video_capture.set(3, 160)

    video_capture.set(4, 120)

    while True:

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

            handler.found_barcode(barcodeData)

        # Crop the image

        crop_img = frame[60:220, 0:160]

        # Convert to grayscale

        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # Gaussian blur

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Color thresholding

        ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        # Find the contours of the frame

        _, contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # Find the biggest contour (if detected)

        if len(contours) > 0:

            c = max(contours, key=cv2.contourArea)

            M = cv2.moments(c)

            cx = int(M['m10'] / M['m00'])

            cy = int(M['m01'] / M['m00'])

            cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)

            cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)

            cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

            if cx >= 120:
                motorControl.execute_linetracker_directive('light_left_turn')
                print("Turn Left!")

            if cx < 120 and cx > 50:
                motorControl.execute_linetracker_directive('forwards')
                print("On Track!")

            if cx <= 50:
                motorControl.execute_linetracker_directive('light_right_turn')
                print("Turn Right")

        else:
            print("Line not Found")
            motorControl.execute_linetracker_directive('stop')

        # Display the resulting frame

        cv2.imshow('frame', crop_img)
        cv2.imshow("Barcode Scanner", qr_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break