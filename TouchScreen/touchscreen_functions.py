#! /usr/bin/python3
# -*- coding: utf-8 -*-
from threading import Thread
import TouchScreen.utils as utils
import time
import system_vars

def init():
    print(system_vars.colorcode['ok'] + "OK: TOUCHSCREEN STARTED" + system_vars.colorcode['reset'])
    touch_main = Thread(target=utils.start, args=(), name="TouchMain", daemon=False)
    touch_main.start()
    time.sleep(1)
    utils.set_info_text('Ready for Order')
    set_order_list([])


def set_ready_order_list(list):
    fill = 7 - len(list)
    fill_list = []

    x = 0
    while x < fill:
        fill_list.append({'real_name': '----', 'room': '----'})
        x = x + 1

    list.extend(fill_list)
    utils.set_item_text('destination_' + str(1), list[0]['room'])
    utils.set_item_text('name_' + str(1), list[0]['real_name'])

    #i = 0
    #while i < 6:
        #utils.set_item_text('destination_' + str(i + 1), list[i]['room'])
        #time.sleep(.1)
        #utils.set_item_text('name_' + str(i + 1), list[i]['real_name'])
        #time.sleep(.1)
        #if list[i]['real_name'] == "----":
            #utils.set_button_enabled('confirm_' + str(i + 1), False)
        #else:
            #utils.set_button_enabled('confirm_' + str(i + 1), True)
        #i = i + 1


def set_order_list(list):
    fill = 7 - len(list)
    fill_list = []

    x = 0
    while x < fill:
        fill_list.append({'real_name': '----', 'room': '----'})
        x = x + 1

    list.extend(fill_list)

    i = 0
    while i < 6:
        utils.set_item_text('destination_' + str(i + 1), list[i]['room'])
        time.sleep(.1)
        utils.set_item_text('name_' + str(i + 1), list[i]['real_name'])
        time.sleep(.1)
        #utils.set_button_enabled('confirm_' + str(i + 1), False)
        i = i + 1


def set_info_text(text):
    utils.set_info_text(text)


def set_button_enabled(item, state):
    utils.set_button_enabled(item, state)


def set_order_confirmed(nr):
    import Orders.order_functions as order_functions
    utils.set_button_enabled('confirm_' + str(nr), False)
    utils.set_item_text('destination_' + str(nr), 'confirmed')
    Confirm_Thread = Thread(target=order_functions.confirm_order, args=((nr - 1),), name="ConfirmOrder", daemon=False)
    Confirm_Thread.start()


if __name__ == "__main__":
    init()
