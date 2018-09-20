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

        self.Emergency_Stop_Pin = 25
        self.Emergency_Stop_Unlock_Pin = 26
        self.Emergency_Stop_Light_Pin = 27

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.Motor_Left_Power_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Motor_Left_Gear_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Motor_Right_Power_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Motor_Right_Gear_pin, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.Emergency_Stop_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.Emergency_Stop_Unlock_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.Emergency_Stop_Light_Pin, GPIO.OUT, initial=GPIO.LOW)

        if configuration.pwm_mode:
            self.left_pwm = GPIO.PWM(self.Motor_Left_Power_Pin, 0)
            self.right_pwm = GPIO.PWM(self.Motor_Right_Power_Pin, 50)  # frequency=50Hz
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

    def emergency_stop_handler(self):
        while True:
            if GPIO.input(self.Emergency_Stop_Pin) == True:
                vars.emergency_stop = True
                self.motor('left', 0, True)
                self.motor('right', 0, True)
                GPIO.output(self.Emergency_Stop_Light_Pin, GPIO.HIGH)
                print(system_vars.colorcode['warning'] + "WARNING: EMERGENCY STOP ENABLED!" +
                      system_vars.colorcode['reset'])

            elif GPIO.input(self.Emergency_Stop_Unlock_Pin) == True:
                vars.emergency_stop = False
                GPIO.output(self.Emergency_Stop_Light_Pin, GPIO.LOW)
                print(system_vars.colorcode['warning'] + "WARNING: EMERGENCY STOP DISABLED!" +
                      system_vars.colorcode['reset'])
            time.sleep(.1)




