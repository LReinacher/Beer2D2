import settings
import LED.configuration as configuration
import system_vars
import pigpio

def init():
    system_vars.pigpio_instance.set_mode(configuration.r_pin, pigpio.OUTPUT)
    system_vars.pigpio_instance.write(configuration.r_pin,0)
    
    system_vars.pigpio_instance.set_mode(configuration.g_pin, pigpio.OUTPUT)
    system_vars.pigpio_instance.write(configuration.g_pin,0)
    
    system_vars.pigpio_instance.set_mode(configuration.b_pin, pigpio.OUTPUT)
    system_vars.pigpio_instance.write(configuration.b_pin,0)


def set_led(color):
    if color in configuration.colors:
        r, g, b = configuration.colors[color]
        if r == 1:
            system_vars.pigpio_instance.write(configuration.r_pin,1)
        else:
            system_vars.pigpio_instance.write(configuration.r_pin,0)
        if g == 1:
            system_vars.pigpio_instance.write(configuration.g_pin,1)
        else:
            system_vars.pigpio_instance.write(configuration.g_pin,0)
        if b == 1:
            system_vars.pigpio_instance.write(configuration.b_pin,1)
        else:
            system_vars.pigpio_instance.write(configuration.b_pin,0)
    else:
        print(system_vars.colorcode['error'] + "ERROR: UNKNOWN LED COLOR" +
              system_vars.colorcode['reset'])