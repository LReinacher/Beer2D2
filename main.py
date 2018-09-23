#! /usr/bin/python3
# -*- coding: utf-8 -*-
from threading import Thread
import system_vars
import settings
from SlackBot import slack_functions
from RestAPI import api_main
from MotorControl import motor_functions
from CamTracking import webcam_functions
#import SlackBot.slack_functions as slack_functions
#import RestAPI.api_main as api_main
#import MotorControl.motor_functions as motor_functions
#mport CamTracking.webcam_functions as webcam_functions


if __name__ == "__main__":
    print(system_vars.colorcode['info'] + "INFO: INITIALIZING SYSTEM..." + system_vars.colorcode['reset'])
    motor_functions.init()
    print(system_vars.colorcode['ok'] + "OK: MOTOR-CONTROL INITIALIZED" + system_vars.colorcode['reset'])

    print(system_vars.colorcode['info'] + "INFO: STARTING SLACK-BOT..." + system_vars.colorcode['reset'])
    SlackBot_thread = Thread(target=slack_functions.init, args=(), name="SlackBot", daemon=False)
    SlackBot_thread.start()

    print(system_vars.colorcode['info'] + "INFO: STARTING REST-API..." + system_vars.colorcode['reset'])
    api_thread = Thread(target=api_main.start, args=(), name="API", daemon=False)
    api_thread.start()

    from Display import display_functions
    print(system_vars.colorcode['info'] + "INFO: STARTING DISPLAY..." + system_vars.colorcode['reset'])
    display_thread = Thread(target=display_functions.init, args=(), name="Display", daemon=False)
    display_thread.start()

    print(system_vars.colorcode['info'] + "INFO: STARTING CAM-TRACKING..." + system_vars.colorcode['reset'])
    WebCam_Thread = Thread(target=webcam_functions.init, args=(), name="CamTracking", daemon=False)
    WebCam_Thread.start()

    print(system_vars.colorcode['ok'] + "OK: SYSTEM INITIALIZED" + system_vars.colorcode['reset'])

