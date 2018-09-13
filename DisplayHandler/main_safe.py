import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import glob_vars

import subprocess


temp_text_override = False

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

disp.begin()

disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0

font = ImageFont.load_default()

def main():
    while True:
        if temp_text_override is False:
            draw.rectangle((0,0,width,height), outline=0, fill=0)

            # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            cmd = "iwgetid -r"
            SSID = subprocess.check_output(cmd, shell=True)
            cmd = "hostname -I | cut -d\' \' -f1"
            IP = subprocess.check_output(cmd, shell = True )

            if glob_vars.remote_system_motor_override:
                mode = "Remote"
            elif glob_vars.executing_slack_direct:
                mode = "SlackDirect"
            else:
                mode = "LineTracking"

            m1, m2 = glob_vars.current_motor_state
            if m1 == "forwards":
                m1 = "Fwd"
            elif m1 == "backwards":
                m1 = "Bwd"
            else:
                m1 = "Stp"

            if m2 == "forwards":
                m2 = "Fwd"
            elif m2 == "backwards":
                m2 = "Bwd"
            else:
                m2 = "Stp"

            # Write two lines of text.

            draw.text((x, top),       "SSID: " + str(SSID.decode('UTF-8')),  font=font, fill=255)
            draw.text((x, top+8),     "IP: " + str(IP.decode('UTF-8')), font=font, fill=255)
            draw.text((x, top+20),    "Mode: " + str(mode),  font=font, fill=255)
            draw.text((x, top+28),    "Dest: " + str(glob_vars.current_destination),  font=font, fill=255)
            draw.text((x, top + 38), "Motors: " + str(m1) + " - " + str(m2), font=font, fill=255)

            # Display image.
            disp.image(image)
            disp.display()
            time.sleep(.1)


def show_temp_text(line1, line2, line3, duration):
    temp_text_override = True

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((x, top), "SSID: " + str(SSID.decode('UTF-8')), font=font, fill=255)
    draw.text((x, top + 8), "IP: " + str(IP.decode('UTF-8')), font=font, fill=255)
    draw.text((x, top + 20), "Mode: " + str(mode), font=font, fill=255)
    draw.text((x, top + 28), "Dest: " + str(glob_vars.current_destination), font=font, fill=255)
    draw.text((x, top + 38), "Motors: " + str(m1) + " - " + str(m2), font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)

    temp_text_override = False