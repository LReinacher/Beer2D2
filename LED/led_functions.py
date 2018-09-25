import settings
import LED.configuration as configuration
import system_vars
if settings.gpio_enabled:
    import pigpio


def init():
    if settings.gpio_enabled:
        system_vars.pigpio_instance.set_mode(configuration.r_pin, pigpio.OUTPUT)
        system_vars.pigpio_instance.write(configuration.r_pin,0)

        system_vars.pigpio_instance.set_mode(configuration.g_pin, pigpio.OUTPUT)
        system_vars.pigpio_instance.write(configuration.g_pin,0)

        system_vars.pigpio_instance.set_mode(configuration.b_pin, pigpio.OUTPUT)
        system_vars.pigpio_instance.write(configuration.b_pin,0)
    else:
        print(system_vars.colorcode['warning'] + "WARNING: LED INITIALIZATION SKIPPED - GPIO DISABLED" + system_vars.colorcode['reset'])


def set_led(color):
    if settings.gpio_enabled:
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
    else:
        print(system_vars.colorcode['warning'] + "WARNING: LED SETTING " + color.upper() + " IGNORED - GPIO DISABLED" +
              system_vars.colorcode['reset'])