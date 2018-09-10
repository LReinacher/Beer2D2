from GPIOEmulator.EmulatorGUI import GPIO as GPIO
#import RPi.GPIO as GPIO

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

    def stop(self):
        GPIO.output(self.Motor_Left_Power_Pin, GPIO.LOW)
        GPIO.output(self.Motor_Left_Gear_pin, GPIO.LOW)
        GPIO.output(self.Motor_Right_Power_Pin, GPIO.LOW)
        GPIO.output(self.Motor_Right_Gear_pin, GPIO.LOW)

    def forwards(self):
        GPIO.output(self.Motor_Left_Power_Pin, GPIO.HIGH)
        GPIO.output(self.Motor_Left_Gear_pin, GPIO.LOW)
        GPIO.output(self.Motor_Right_Power_Pin, GPIO.HIGH)
        GPIO.output(self.Motor_Right_Gear_pin, GPIO.LOW)

    def backwards(self):
        GPIO.output(self.Motor_Left_Power_Pin, GPIO.HIGH)
        GPIO.output(self.Motor_Left_Gear_pin, GPIO.HIGH)
        GPIO.output(self.Motor_Right_Power_Pin, GPIO.HIGH)
        GPIO.output(self.Motor_Right_Gear_pin, GPIO.HIGH)

    def right(self):
        GPIO.output(self.Motor_Left_Power_Pin, GPIO.HIGH)
        GPIO.output(self.Motor_Left_Gear_pin, GPIO.LOW)
        GPIO.output(self.Motor_Right_Power_Pin, GPIO.HIGH)
        GPIO.output(self.Motor_Right_Gear_pin, GPIO.HIGH)

    def left(self):
        GPIO.output(self.Motor_Left_Power_Pin, GPIO.HIGH)
        GPIO.output(self.Motor_Left_Gear_pin, GPIO.HIGH)
        GPIO.output(self.Motor_Right_Power_Pin, GPIO.HIGH)
        GPIO.output(self.Motor_Right_Gear_pin, GPIO.LOW)




