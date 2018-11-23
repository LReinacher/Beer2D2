import RPi.GPIO as GPIO  # sudo apt-get install python-rpi.gpio


class Driver:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.R_EN = 21
        self.L_EN = 22
        self.RPWM = 23
        self.LPWM = 24
        GPIO.setup(self.R_EN, GPIO.OUT)
        GPIO.setup(self.RPWM, GPIO.OUT)
        GPIO.setup(self.L_EN, GPIO.OUT)
        GPIO.setup(self.LPWM, GPIO.OUT)

    def setup(self):
        GPIO.output(self.L_EN, GPIO.HIGH)
        GPIO.output(self.R_EN, GPIO.HIGH)

    def right(self):
        GPIO.output(self.R_EN, GPIO.HIGH)
        GPIO.output(self.RPWM, GPIO.HIGH)
        GPIO.output(self.LPWM, GPIO.LOW)


if __name__ == "__main__":
    driver = Driver()
    driver.setup()
    driver.right()
