#! /usr/bin/python3
# -*- coding: utf-8 -*-
import settings
import MotorControl.vars as vars
import MotorControl.configuration as configuration
import system_vars
import time
from threading import Thread
if settings.gpio_enabled:
    import pigpio

class MotorControl(object):
    def __init__(self):
        
        self.Motor_Left_Power_Pin = 13
        self.Motor_Left_Gear_Pin = 27

        self.Motor_Right_Power_Pin = 18
        self.Motor_Right_Gear_Pin = 17

        self.Emergency_Stop_Pin = 22
        self.Emergency_Stop_Unlock_Pin = 22
        self.Emergency_Stop_Light_Pin = 23

        self.Door_Status_Pin = 5

        if settings.gpio_enabled:
            self.pi = pigpio.pi()
            system_vars.pigpio_instance = self.pi

            self.pi.set_mode(self.Motor_Left_Gear_Pin, pigpio.OUTPUT)
            self.pi.write(self.Motor_Left_Gear_Pin,0)

            self.pi.set_mode(self.Motor_Right_Gear_Pin, pigpio.OUTPUT)
            self.pi.write(self.Motor_Right_Gear_Pin,0)

            self.pi.set_mode(self.Emergency_Stop_Light_Pin, pigpio.OUTPUT)
            self.pi.write(self.Emergency_Stop_Light_Pin,0)

            self.pi.set_mode(self.Motor_Left_Power_Pin, pigpio.OUTPUT)
            self.pi.set_PWM_dutycycle(self.Motor_Left_Power_Pin, 0)

            self.pi.set_mode(self.Motor_Right_Power_Pin, pigpio.OUTPUT)
            self.pi.set_PWM_dutycycle(self.Motor_Right_Power_Pin, 0)

            self.pi.set_mode(self.Emergency_Stop_Pin, pigpio.INPUT)
            self.pi.set_pull_up_down(self.Emergency_Stop_Pin, pigpio.PUD_DOWN)

            self.pi.set_mode(self.Emergency_Stop_Unlock_Pin, pigpio.INPUT)
            self.pi.set_pull_up_down(self.Emergency_Stop_Unlock_Pin, pigpio.PUD_DOWN)

            self.pi.set_mode(self.Door_Status_Pin, pigpio.INPUT)
            self.pi.set_pull_up_down(self.Door_Status_Pin, pigpio.PUD_DOWN)
        else:
            print(system_vars.colorcode['warning'] + "WARNING: MOTOR CONTROL INITIALIZATION SKIPPED - GPIO DISABLED" +
                  system_vars.colorcode['reset'])

    def motor(self, motor, speed, emergency_override=False):
        if settings.gpio_enabled:
            if vars.emergency_stop is False or emergency_override is True:
                if motor == "left":
                    vars.current_motor_state[0] = speed
                    power_pin = self.Motor_Left_Power_Pin
                    gear_pin = self.Motor_Left_Gear_Pin
                elif motor == "right":
                    vars.current_motor_state[1] = speed
                    power_pin = self.Motor_Right_Power_Pin
                    gear_pin = self.Motor_Right_Gear_Pin
                else:
                    return False

                if configuration.pwm_mode:
                    if speed in configuration.speedIdentifiers:
                        pwm_data, gear_mode = configuration.speedIdentifiers[speed]
                        if gear_mode == "fwd":
                            self.pi.write(gear_pin,0)
                        else:
                            self.pi.write(gear_pin,1)
                        self.pi.set_PWM_dutycycle(power_pin, pwm_data)
                    else:
                        print(system_vars.colorcode['error'] + "ERROR: MOTOR-CONTROL-UTIL - UNKNOWN SPEED-IDENTIFIER" + system_vars.colorcode['reset'])
                        return False

                else:
                    if speed > 0:
                        self.pi.write(gear_pin,0)
                        self.pi.write(power_pin,1)
                    elif speed < 0:
                        self.pi.write(gear_pin,1)
                        self.pi.write(power_pin,1)
                    else:
                        self.pi.write(gear_pin,0)
                        self.pi.write(power_pin,0)

                return True

            else:
                print(system_vars.colorcode['warning'] + "WARNING: MOTOR COMMAND OVERRIDE - EMERGENCY STOP ENABLED!" +
                      system_vars.colorcode['reset'])
        else:
            print(system_vars.colorcode[
                      'warning'] + "WARNING: MOTOR COMMAND " + motor.upper() + " @ " + str(speed) + " IGNORED - GPIO DISABLED" +
                  system_vars.colorcode['reset'])

    def emergency_stop_and_door_status_handler(self):
        if settings.gpio_enabled:
            while True:
                if self.pi.read(self.Emergency_Stop_Pin) == 1 and vars.emergency_stop is False:
                    vars.emergency_stop = True
                    self.motor('left', 0, True)
                    self.motor('right', 0, True)
                    self.pi.write(self.Emergency_Stop_Light_Pin,1)
                    import LED.led_functions as led_functions
                    led_functions.set_led('red')
                    print(system_vars.colorcode['warning'] + "WARNING: EMERGENCY STOP ENABLED!" +
                          system_vars.colorcode['reset'])
                    time.sleep(.2)

                elif self.pi.read(self.Emergency_Stop_Unlock_Pin) == 1 and vars.emergency_stop is True:
                    vars.emergency_stop = False
                    self.pi.write(self.Emergency_Stop_Light_Pin,0)
                    import LED.led_functions as led_functions
                    led_functions.set_led('blue')
                    print(system_vars.colorcode['warning'] + "WARNING: EMERGENCY STOP DISABLED!" +
                          system_vars.colorcode['reset'])
                    time.sleep(.2)

                if self.pi.read(self.Door_Status_Pin) == 1 and system_vars.door_is_open is False:
                    system_vars.door_is_open = True
                    print(system_vars.colorcode['info'] + "INFO: DOOR OPENED" +
                          system_vars.colorcode['reset'])
                    self.motor('left', 0)
                    self.motor('right', 0)
                elif self.pi.read(self.Door_Status_Pin) == 0 and system_vars.door_is_open is True:
                    system_vars.door_is_open = False
                    print(system_vars.colorcode['info'] + "INFO: DOOR CLOSED" +
                          system_vars.colorcode['reset'])
                time.sleep(.1)
        else:
            print(system_vars.colorcode['warning'] + "WARNING: EMERGENCY STOP AND DOOR HANDLER INITIALIZATION SKIPPED - GPIO DISABLED" +
                  system_vars.colorcode['reset'])