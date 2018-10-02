#! /usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import imutils
from pyzbar import pyzbar
import settings
from datetime import datetime
import system_vars
import CamTracking.vars as vars
import CamTracking.webcam_functions as webcam_functions
import time


def check(frame):
    qr_frame = imutils.resize(frame, width=400)
    
    barcodes = pyzbar.decode(qr_frame)
    
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(qr_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(qr_frame, text, (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        webcam_functions.found_barcode(barcodeData)


def main():
    print(system_vars.colorcode['ok'] + "OK: QR STARTED" + system_vars.colorcode['reset'])
    import MotorControl.motor_functions as motor_functions
    import CamTracking.webcam_functions as webcam_functions
    
    while(True):
        # Capture the frames
        
        frame = vars.frame
        try:
            qr_frame = imutils.resize(frame, width=400)
            
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(qr_frame)
            
            for barcode in barcodes:
                # extract the bounding box location of the barcode and draw
                # the bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(qr_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(qr_frame, text, (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                webcam_functions.found_barcode(barcodeData)

            #Display the resulting frame
            cv2.imshow('qr frame',qr_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            time.sleep(.1)
        
    else:
        time.sleep(.1)
