#! /usr/bin/python3
# -*- coding: utf-8 -*-
import settings
from MotorControl import vars
from MotorControl import configuration
import system_vars
import time
if settings.localhost:
    from GPIOEmulator.EmulatorGUI import GPIO as GPIO
else:
    import RPi.GPIO as GPIO


class MotorControl(object):
    def __init__(self):
        self.Motor_Left_Power_Pin = 13
        self.Motor_Left_Gear_pin = 27

        self.Motor_Right_Power_Pin = 18
        self.Motor_Right_Gear_pin = 17

        self.Emergency_Stop_Pin = 22
        self.Emergency_Stop_Unlock_Pin = 22
        self.Emergency_Stop_Light_Pin = 23

        self.Door_Status_Pin = 5

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.Motor_Left_Power_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Motor_Left_Gear_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Motor_Right_Power_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Motor_Right_Gear_pin, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.Emergency_Stop_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if self.Emergency_Stop_Unlock_Pin != self.Emergency_Stop_Pin:
            GPIO.setup(self.Emergency_Stop_Unlock_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.Emergency_Stop_Light_Pin, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.Door_Status_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        if configuration.pwm_mode:
            self.left_pwm = GPIO.PWM(self.Motor_Left_Power_Pin, 1)
            self.right_pwm = GPIO.PWM(self.Motor_Right_Power_Pin, 1)  # frequency=1Hz
            self.left_pwm.start(0)
            self.right_pwm.start(0)

    def motor(self, motor, speed, emergency_override=False):
        if vars.emergency_stop is False or emergency_override is True:
            if motor == "left":
                vars.current_motor_state[0] = speed
                power_pin = self.Motor_Left_Power_Pin
                gear_pin = self.Motor_Left_Gear_pin
                if configuration.pwm_mode:
                    pwm = self.left_pwm
            elif motor == "right":
                vars.current_motor_state[1] = speed
                power_pin = self.Motor_Right_Power_Pin
                gear_pin = self.Motor_Right_Gear_pin
                if configuration.pwm_mode:
                    pwm = self.right_pwm
            else:
                return False

            if configuration.pwm_mode:
                if speed in configuration.speedIdentifiers:
                    pwm_data, gear_mode = configuration.speedIdentifiers[speed]
                    if gear_mode == "fwd":
                        GPIO.output(gear_pin, GPIO.LOW)
                    else:
                        GPIO.output(gear_pin, GPIO.HIGH)
                    pwm.ChangeDutyCycle(pwm_data)
                else:
                    print(system_vars.colorcode['error'] + "ERROR: MOTOR-CONTROL-UTIL - UNKNOWN SPEED-IDENTIFIER" + system_vars.colorcode['reset'])
                    return False

            else:
                if speed > 0:
                    GPIO.output(gear_pin, GPIO.LOW)
                    GPIO.output(power_pin, GPIO.HIGH)
                elif speed < 0:
                    GPIO.output(gear_pin, GPIO.HIGH)
                    GPIO.output(power_pin, GPIO.HIGH)
                else:
                    GPIO.output(gear_pin, GPIO.LOW)
                    GPIO.output(power_pin, GPIO.LOW)

            return True

        else:
            print(system_vars.colorcode['warning'] + "WARNING: MOTOR COMMAND OVERRIDE - EMERGENCY STOP ENABLED!" +
                  system_vars.colorcode['reset'])

    def emergency_stop_and_door_status_handler(self):
        while True:
            if GPIO.input(self.Emergency_Stop_Pin) is True and vars.emergency_stop is False:
                vars.emergency_stop = True
                self.motor('left', 0, True)
                self.motor('right', 0, True)
                GPIO.output(self.Emergency_Stop_Light_Pin, GPIO.HIGH)
                print(system_vars.colorcode['warning'] + "WARNING: EMERGENCY STOP ENABLED!" +
                      system_vars.colorcode['reset'])
                time.sleep(.2)

            elif GPIO.input(self.Emergency_Stop_Unlock_Pin) is True and vars.emergency_stop is True:
                vars.emergency_stop = False
                GPIO.output(self.Emergency_Stop_Light_Pin, GPIO.LOW)
                print(system_vars.colorcode['warning'] + "WARNING: EMERGENCY STOP DISABLED!" +
                      system_vars.colorcode['reset'])
                time.sleep(.2)

            if GPIO.input(self.Door_Status_Pin) is True and system_vars.door_is_open is False:
                system_vars.door_is_open = True
                print(system_vars.colorcode['info'] + "INFO: DOOR OPENED" +
                      system_vars.colorcode['reset'])
                self.motor('left', 0)
                self.motor('right', 0)
            elif GPIO.input(self.Door_Status_Pin) is False and system_vars.door_is_open is True:
                system_vars.door_is_open = False
                print(system_vars.colorcode['info'] + "INFO: DOOR CLOSED" +
                      system_vars.colorcode['reset'])
            time.sleep(.1)




