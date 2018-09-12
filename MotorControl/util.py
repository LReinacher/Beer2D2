import settings
import time
import glob_vars
import MotorControl.configuration as configuration
if settings.localhost:
    from GPIOEmulator.EmulatorGUI import GPIO as GPIO
else:
    import RPi.GPIO as GPIO

class MotorControl(object):
    def __init__(self):
        self.Motor_Left_Power_Pin = 22
        self.Motor_Left_Gear_pin = 23

        self.Motor_Right_Power_Pin = 17
        self.Motor_Right_Gear_pin = 18

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

    def execute_qr_directive(self, directive):
        if glob_vars.remote_system_motor_override is False:
            current_state_left_motor, current_state_right_motor = glob_vars.current_motor_state
            glob_vars.qr_system_motor_override = True
            left_cmd, right_cmd, duration = configuration.commandIdentifiers[directive]
            glob_vars.current_motor_state = left_cmd, right_cmd
            self.motor("left", left_cmd)
            self.motor("right", right_cmd)
            if duration is not None:
                time.sleep(duration)
                if configuration.stop_after_qr_directive:
                    self.motor("left", 'stop')
                    self.motor("right", 'stop')
                    glob_vars.current_motor_state = 'stop', 'stop'
                else:
                    glob_vars.current_motor_state = current_state_left_motor, current_state_right_motor
                    self.motor("left", current_state_left_motor)
                    self.motor("right", current_state_right_motor)
            glob_vars.qr_system_motor_override = False
        else:
            print("QR-Directive Remote Override!")

    def execute_linetracker_directive(self, directive):
        if glob_vars.remote_system_motor_override is False:
            if glob_vars.qr_system_motor_override is False:
                current_state_left_motor, current_state_right_motor = glob_vars.current_motor_state
                left_cmd, right_cmd, duration = configuration.commandIdentifiers[directive]
                glob_vars.current_motor_state = left_cmd, right_cmd
                self.motor("left", left_cmd)
                self.motor("right", right_cmd)
                if duration is not None:
                    time.sleep(duration)
                    if configuration.stop_after_linetracker_directive:
                        self.motor("left", 'stop')
                        self.motor("right", 'stop')
                        glob_vars.current_motor_state = 'stop', 'stop'
                    else:
                        glob_vars.current_motor_state = current_state_left_motor, current_state_right_motor
                        self.motor("left", current_state_left_motor)
                        self.motor("right", current_state_right_motor)
                glob_vars.qr_system_motor_override = False
            else:
                print("Line Tracker QR-Directive Override!")
        else:
            print("Line Tracker Remote Override!")



