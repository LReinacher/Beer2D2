from threading import Thread
import time
import system_vars
import settings
from Display import vars


def init():
    if settings.localhost is False:
        from Display import util
        vars.DisplayHandlerInstance = util.DisplayHandler
        print(system_vars.colorcode['ok'] + "OK: DISPLAY INITIALIZED" + system_vars.colorcode['reset'])
        vars.DisplayHandlerInstance.run_default_screen()
    print(system_vars.colorcode['warning'] + "WARNING: DISPLAY INITIALIZATION SKIPPED - LOCALHOST ENABLED" + system_vars.colorcode['reset'])


def display_custom_text_duration(header, line1, line2, duration):
    custom_text_thread = Thread(target=display_custom_text_duration_thread, args=(header, line1, line2, duration,), name="Custom_Display_Text", daemon=False)
    custom_text_thread.start()


def display_custom_text_duration_thread(header, line2, line3, duration):
    display_custom_text(header, line2, line3)
    time.sleep(duration)
    remove_custom_text()


def display_custom_text(header, line2, line3):
    vars.header = header
    vars.line2 = line2
    vars.line3 = line3
    vars.display_custom_text = True


def remove_custom_text():
    vars.display_custom_text = False
    vars.header = ""
    vars.line2 = ""
    vars.line3 = ""
