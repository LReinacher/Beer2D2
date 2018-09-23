import settings
if settings.localhost:
    from GPIOEmulator.EmulatorGUI import GPIO as GPIO
else:
    import RPi.GPIO as GPIO
import LED.configuration as configuration
import system_vars

def init():
    GPIO.setup(configuration.r_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(configuration.g_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(configuration.b_pin, GPIO.OUT, initial=GPIO.LOW)


def set_led(color):
    if color in configuration.colors:
        r, g, b = configuration.colors[color]
        if r == 1:
            GPIO.output(configuration.r_pin, GPIO.HIGH)
        else:
            GPIO.output(configuration.r_pin, GPIO.LOW)
        if g == 1:
            GPIO.output(configuration.g_pin, GPIO.HIGH)
        else:
            GPIO.output(configuration.g_pin, GPIO.LOW)
        if b == 1:
            GPIO.output(configuration.b_pin, GPIO.HIGH)
        else:
            GPIO.output(configuration.b_pin, GPIO.LOW)
    else:
        print(system_vars.colorcode['error'] + "ERROR: UNKNOWN LED COLOR" +
              system_vars.colorcode['reset'])