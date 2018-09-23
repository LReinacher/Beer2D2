#! /usr/bin/python3
# -*- coding: utf-8 -*-
import gi

# import gtk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from threading import Thread
from TouchScreen import vars


def start():
    vars.builder = Gtk.Builder()
    vars.builder.add_from_file("test.glade")
    vars.builder.connect_signals(Handler())

    window = vars.builder.get_object("base")
    window.show_all()

    Gtk.main()


def set_item_text(item, text):
    item_object = vars.builder.get_object(item)
    item_object.set_text(text)


def set_button_enabled(item, state):
    item_object = vars.builder.get_object(item)
    item_object.set_sensitive(state)


def set_info_text(text):
    item_object = vars.builder.get_object('info_label')
    item_object.set_text(text)


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def confirm_1_ButtonPressed(self, button):
        import Orders.order_functions as order_functions
        order_functions.confirm_order(0)
        set_button_enabled('confirm_1', False)

    def confirm_2_ButtonPressed(self, button):
        import Orders.order_functions as order_functions
        order_functions.confirm_order(0)
        set_button_enabled('confirm_2', False)

    def confirm_3_ButtonPressed(self, button):
        import Orders.order_functions as order_functions
        order_functions.confirm_order(0)
        set_button_enabled('confirm_3', False)

    def confirm_4_ButtonPressed(self, button):
        import Orders.order_functions as order_functions
        order_functions.confirm_order(0)
        set_button_enabled('confirm_4', False)

    def confirm_5_ButtonPressed(self, button):
        import Orders.order_functions as order_functions
        order_functions.confirm_order(0)
        set_button_enabled('confirm_5', False)

    def confirm_6_ButtonPressed(self, button):
        import Orders.order_functions as order_functions
        order_functions.confirm_order(0)
        set_button_enabled('confirm_6', False)

