#! /usr/bin/python3
# -*- coding: utf-8 -*-
from threading import Thread
import system_vars
import settings
from SlackBot import slack_functions
from RestAPI import api_main
from MotorControl import motor_functions
from LED import led_functions
from AudioHandler import audio_functions
from CamTracking import tracking
import system_handler
#import SlackBot.slack_functions as slack_functions
#import RestAPI.api_main as api_main
#import MotorControl.motor_functions as motor_functions
#mport CamTracking.webcam_functions as webcam_functions


if __name__ == "__main__":
    print(system_vars.colorcode['info'] + "INFO: INITIALIZING SYSTEM..." + system_vars.colorcode['reset'])
    audio_functions.init()
    print(system_vars.colorcode['ok'] + "OK: AUDIO INITIALIZED" + system_vars.colorcode['reset'])
    audio_functions.play_sound('Beeping and whistling.mp3')
    motor_functions.init()
    print(system_vars.colorcode['ok'] + "OK: MOTOR-CONTROL INITIALIZED" + system_vars.colorcode['reset'])
    led_functions.init()
    led_functions.set_led('red')
    print(system_vars.colorcode['ok'] + "OK: LED INITIALIZED" + system_vars.colorcode['reset'])

    print(system_vars.colorcode['info'] + "INFO: STARTING SLACK-BOT..." + system_vars.colorcode['reset'])
    SlackBot_thread = Thread(target=slack_functions.init, args=(), name="SlackBot", daemon=False)
    SlackBot_thread.start()

    print(system_vars.colorcode['info'] + "INFO: STARTING REST-API..." + system_vars.colorcode['reset'])
    api_thread = Thread(target=api_main.start, args=(), name="API", daemon=False)
    api_thread.start()

    print(system_vars.colorcode['info'] + "INFO: STARTING CAM-TRACKING..." + system_vars.colorcode['reset'])
    WebCam_Thread = Thread(target=tracking.main, args=(), name="CamTracking", daemon=False)
    WebCam_Thread.start()

    if settings.touchscreen_enabled:
        from UI import ui_functions
        print(system_vars.colorcode['info'] + "INFO: STARTING TOUCHSCREEN..." + system_vars.colorcode['reset'])
        TouchScreen_Thread = Thread(target=ui_functions.init, args=(), name="TouchScreen", daemon=False)
        TouchScreen_Thread.start()

    print(system_vars.colorcode['ok'] + "OK: SYSTEM INITIALIZED" + system_vars.colorcode['reset'])
    led_functions.set_led('blue')

