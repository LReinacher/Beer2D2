#from GPIOEmulator.EmulatorGUI import GPIO as GPIO
import RPi.GPIO as GPIO
import time

class MotorControl(object):
    def __init__(self):
        self.Motor_Left_Power_Pin = 17
        self.Motor_Left_Gear_pin = 18

        self.Motor_Right_Power_Pin = 22
        self.Motor_Right_Gear_pin = 23

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.Motor_Left_Power_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Motor_Left_Gear_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Motor_Right_Power_Pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Motor_Right_Gear_pin, GPIO.OUT, initial=GPIO.LOW)

    def motor(self, motor, command):
        if motor == "left":
            power_pin = self.Motor_Left_Power_Pin
            gear_pin = self.Motor_Left_Gear_pin
        elif motor == "right":
            power_pin = self.Motor_Right_Power_Pin
            gear_pin = self.Motor_Right_Gear_pin
        else:
            return 1

        if command == "forwards":
            GPIO.output(power_pin, GPIO.HIGH)
            GPIO.output(gear_pin, GPIO.LOW)
        elif command == "backwards":
            GPIO.output(power_pin, GPIO.HIGH)
            GPIO.output(gear_pin, GPIO.HIGH)
        elif command == "stop":
            GPIO.output(power_pin, GPIO.LOW)
            GPIO.output(gear_pin, GPIO.LOW)
        else:
            return 2

        return 0

    def stop(self):
        self.motor("left", "stop")
        self.motor("right", "stop")

    def forwards(self, duration=None):
        self.motor("left", "forwards")
        self.motor("right", "forwards")
        if duration is not None:
            time.sleep(duration)
            self.stop()

    def backwards(self, duration=None):
        self.motor("left", "backwards")
        self.motor("right", "backwards")
        if duration is not None:
            time.sleep(duration)
            self.stop()

    def spin_right(self, duration=None):
        self.motor("left", "forwards")
        self.motor("right", "backwards")
        if duration is not None:
            time.sleep(duration)
            self.stop()

    def spin_left(self, duration=None):
        self.motor("left", "backwards")
        self.motor("right", "forwards")
        if duration is not None:
            time.sleep(duration)
            self.stop()

    def turn_right(self, duration=None):
        self.motor("left", "forwards")
        self.motor("right", "stop")
        if duration is not None:
            time.sleep(duration)
            self.stop()

    def turn_left(self, duration=None):
        self.motor("left", "stop")
        self.motor("right", "forwards")
        if duration is not None:
            time.sleep(duration)
            self.stop()



