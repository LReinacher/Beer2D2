import subprocess
import time
import system_vars

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from Display import vars
from Orders import order_functions
from MotorControl import motor_functions


class DisplayHandler(object):
    def __init__(self):
        self.temp_text_override = False

        self.RST = None
        self.DC = 23
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0

        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=self.RST)

        self.disp.begin()

        self.disp.clear()
        self.disp.display()

        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        self.draw = ImageDraw.Draw(self.image)

        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding
        self.x = 0

        self.font = ImageFont.truetype("DisplayHandler/font/segoeui.ttf", 11)  # Schriftart, Schriftgröße
        self.font_b = ImageFont.truetype("DisplayHandler/font/segoeuib.ttf", 12)
        self.font_c = ImageFont.truetype("DisplayHandler/font/segoeuib.ttf", 18)

    def run_default_screen(self):
        print(system_vars.colorcode['ok'] + "OK: DISPLAY STARTED" + system_vars.colorcode['reset'])
        while True:
            if self.temp_text_override is False:
                self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

                cmd = "iwgetid -r"
                SSID = subprocess.check_output(cmd, shell=True)
                cmd = "hostname -I | cut -d\' \' -f1"
                IP = subprocess.check_output(cmd, shell=True)

                if system_vars.remote_control:
                    mode = "Remote"
                else:
                    mode = "LineTracking"

                m1, m2 = motor_functions.get_motor_state()
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

                if vars.display_custom_text:
                    top_offset = 10
                    self.draw.text((self.x, self.top + top_offset), str(vars.header), font=self.font_c, fill=255)
                    self.draw.text((self.x, self.top + top_offset + 20), str(vars.line2), font=self.font_b, fill=255)
                    self.draw.text((self.x, self.top + top_offset + 28), str(vars.line3), font=self.font_b, fill=255)
                else:
                    self.draw.text((self.x, self.top), "SSID: " + str(SSID.decode('UTF-8')), font=self.font, fill=255)
                    self.draw.text((self.x, self.top + 10), "IP: " + str(IP.decode('UTF-8')), font=self.font, fill=255)
                    self.draw.text((self.x, self.top + 25), "Mode: " + str(mode), font=self.font, fill=255)
                    self.draw.text((self.x, self.top + 37), "Dest: " + str(order_functions.get_current_destination()), font=self.font, fill=255)
                    self.draw.text((self.x, self.top + 52), "Motors: " + str(m1) + " - " + str(m2), font=self.font, fill=255)

                # Display image.
                self.disp.image(self.image)
                self.disp.display()
            time.sleep(.1)