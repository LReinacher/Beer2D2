#! /usr/bin/python3
# -*- coding: utf-8 -*-
import gi

# import gtk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
from threading import Thread
import TouchScreen.vars as vars
import time


def start():
    vars.builder = Gtk.Builder()
    vars.builder.add_from_file("TouchScreen/layout.glade")
    vars.builder.connect_signals(Handler())

    for object in vars.objects:
        vars.objects[object] = vars.builder.get_object(object)

    vars.objects['info_label'].modify_font(Pango.FontDescription('Sans 20'))

    window = vars.builder.get_object("base")
    window.show_all()

    touch_data_handler = Thread(target=set_data_handler, args=(), name="TouchMain", daemon=False)
    touch_data_handler.start()

    Gtk.main()


def set_data_handler():
    while True:
        for object in vars.screen_data:
            if 'text' in vars.screen_data[object] and vars.screen_data[object]['text'] != vars.screen_data_old[object]['text']:
                vars.screen_data_old[object]['text'] = vars.screen_data[object]['text']
                set_item_text(object, vars.screen_data[object]['text'])
            if 'enabled' in vars.screen_data[object] and vars.screen_data[object]['enabled'] != vars.screen_data_old[object]['enabled']:
                vars.screen_data_old[object]['enabled'] = vars.screen_data[object]['enabled']
                set_button_enabled(object, vars.screen_data[object]['enabled'])
            if 'label' in vars.screen_data[object] and vars.screen_data[object]['label'] != vars.screen_data_old[object]['label']:
                vars.screen_data_old[object]['label'] = vars.screen_data[object]['label']
                set_button_label(object, vars.screen_data[object]['label'])
        time.sleep(0.1)


def set_item_text(item, text):
    item_object = vars.objects[item]
    item_object.set_text(text)


def set_button_label(item, text):
    item_object = vars.objects[item]
    item_object.set_label(text)


def set_button_enabled(item, state):
    item_object = vars.objects[item]
    item_object.set_sensitive(state)


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def confirm_1_ButtonPressed(self, button):
        import TouchScreen.touchscreen_functions as touchscreen_functions
        touchscreen_functions.set_order_confirmed(1)

    def confirm_2_ButtonPressed(self, button):
        import TouchScreen.touchscreen_functions as touchscreen_functions
        touchscreen_functions.set_order_confirmed(2)

    def confirm_3_ButtonPressed(self, button):
        import TouchScreen.touchscreen_functions as touchscreen_functions
        touchscreen_functions.set_order_confirmed(3)

    def confirm_4_ButtonPressed(self, button):
        import TouchScreen.touchscreen_functions as touchscreen_functions
        touchscreen_functions.set_order_confirmed(4)

    def confirm_5_ButtonPressed(self, button):
        import TouchScreen.touchscreen_functions as touchscreen_functions
        touchscreen_functions.set_order_confirmed(5)

    def confirm_6_ButtonPressed(self, button):
        import TouchScreen.touchscreen_functions as touchscreen_functions
        touchscreen_functions.set_order_confirmed(6)

