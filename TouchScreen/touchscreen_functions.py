#! /usr/bin/python3
# -*- coding: utf-8 -*-
from threading import Thread
import TouchScreen.utils as utils
import time
import system_vars
import TouchScreen.vars as vars
import copy
import TouchScreen.texts as texts

def init():
    print(system_vars.colorcode['ok'] + "OK: TOUCHSCREEN STARTED" + system_vars.colorcode['reset'])
    touch_main = Thread(target=utils.start, args=(), name="TouchMain", daemon=False)
    touch_main.start()
    #utils.set_info_text('Ready for Order')
    #set_order_list([])


def set_ready_order_list(temp_list):
    list = copy.deepcopy(temp_list)
    fill = 7 - len(list)
    fill_list = []

    x = 0
    while x < fill:
        fill_list.append({'real_name': '----', 'room': '----'})
        x = x + 1

    list.extend(fill_list)

    i = 0
    while i < 6:
        vars.screen_data['destination_' + str(i + 1)]['text'] = list[i]['room']
        vars.screen_data['name_' + str(i + 1)]['text'] = list[i]['real_name']
        if 'type' in list[i]:
            vars.screen_data['confirm_' + str(i + 1)]['enabled'] = True
            vars.screen_data['confirm_' + str(i + 1)]['label'] = 'confirm order'
        else:
            vars.screen_data['confirm_' + str(i + 1)]['enabled'] = False
            vars.screen_data['confirm_' + str(i + 1)]['label'] = '----'
        i = i + 1


def set_order_list(temp_list):
    list = copy.deepcopy(temp_list)
    fill = 7 - len(list)
    fill_list = []

    x = 0
    while x < fill:
        fill_list.append({'real_name': '----', 'room': '----'})
        x = x + 1

    list.extend(fill_list)
    set_info_label(texts.ready_for_order)

    i = 0
    while i < 6:
        vars.screen_data['destination_' + str(i + 1)]['text'] = list[i]['room']
        vars.screen_data['name_' + str(i + 1)]['text'] = list[i]['real_name']
        vars.screen_data['confirm_' + str(i + 1)]['enabled'] = False
        vars.screen_data['confirm_' + str(i + 1)]['label'] = '----'
        i = i + 1


def set_button_enabled(item, state):
    utils.set_button_enabled(item, state)


def set_order_confirmed(nr):
    import Orders.order_functions as order_functions
    vars.screen_data['confirm_' + str(nr)]['label'] = 'confirmed'
    vars.screen_data['confirm_' + str(nr)]['enabled'] = False
    Confirm_Thread = Thread(target=order_functions.confirm_order, args=((nr - 1),), name="ConfirmOrder", daemon=False)
    Confirm_Thread.start()


def set_info_label(text):
    vars.screen_data['info_label']['text'] = text

if __name__ == "__main__":
    init()
