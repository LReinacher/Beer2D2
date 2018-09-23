#! /usr/bin/python3
# -*- coding: utf-8 -*-
from Orders import vars
from SlackBot import slack_functions
from MotorControl import motor_functions
import settings
import system_vars
from Locations import location_functions
from CamTracking import webcam_functions
if settings.touchscreen_enabled:
    from TouchScreen import touchscreen_functions


def check_room_order(room):
    i = len(vars.order_que)
    while i > 0:
        if vars.order_que[i - 1]['room'] == room:
            return i - 1
        i = i - 1
    return -1


def check_user_order(user, ident2=None):
    i = len(vars.order_que)
    while i > 0:
        if vars.order_que[i - 1]['user'] == user or vars.order_que[i - 1]['user'] == ident2:
            return i - 1
        i = i - 1
    return -1


def add_order(user, room, type, priority=False):
    result = check_user_already_placed_order(user, type)
    real_name = slack_functions.get_real_name(user, type)
    if result is None:
        if priority:
            vars.order_que.insert(0, {'room': room, 'user': user, 'real_name': real_name, 'type': type})
            position = 0
        else:
            result = check_room_order(room)
            if result >= 0:
                vars.order_que.insert(result + 1, {'room': room, 'user': user, 'real_name': real_name, 'type': type})
                position = result + 1
            else:
                vars.order_que.append({'room': room, 'user': user, 'real_name': real_name, 'type': type})
                position = len(vars.order_que) - 1

        return True, position
    else:
        return False, result


def delete_oder(identifier, type):
    if type == "index":
        index = identifier
    else:
        if type == 'email':
            email = identifier
            id = slack_functions.get_id_by_email(email)
        else:
            id = identifier
            email = slack_functions.get_email_by_id(id)
        index = check_user_order(id, email)

    if index >= 0:
        vars.order_que.pop(index)
        return True
    else:
        return False


def check_user_already_placed_order(identifier, type):
    if type == 'email':
        email = identifier
        id = slack_functions.get_id_by_email(email)
    else:
        id = identifier
        email = slack_functions.get_email_by_id(id)

    index = check_user_order(id, email)
    if index >= 0:
        return vars.order_que[index]
    else:
        return None


def get_orders():
    return vars.order_que


def get_current_destination():
    if len(vars.order_que) > 0:
        return vars.order_que[0]['room']
    else:
        return "No Destination"


def get_destination_all_orders(destination):
    i = 0
    orders = []
    while vars.order_que[i]['room'] == destination:
        order = vars.order_que[i]['open'] = True
        orders.append(order)
        i = i + 1
    return orders


def get_ready_order_list():
    return vars.ready_order_list


def start_drop_off():
    system_vars.destination_reached = True
    motor_functions.stop_both()

    orders = get_destination_all_orders(get_current_destination())
    vars.ready_order_list = orders

    if settings.touchscreen_enabled:
        touchscreen_functions.set_ready_order_list(orders)

    wait_time = calc_order_wait_time()

    i = 0
    while i < len(orders):
        if orders[i]['type'] == ['Slack']:
            slack_functions.send_dm(orders[i]['user'], '')
        else:
            user_id = slack_functions.get_id_by_email(orders[i]['user'])
            if user_id is not None:
                slack_functions.send_dm(orders[i]['user'], '')
            else:
                pass
                #send e-mail
        i = i + 1

    order_countdown(wait_time)
    end_drop_off()


def end_drop_off():
    ready_order_count = len(vars.ready_order_list)
    vars.ready_order_list = []
    i = 0
    while i < ready_order_count:
        delete_oder(i, 'index')
        i = i + 1
    location_functions.leave_location(webcam_functions.get_last_barcode())


def calc_order_wait_time():
    time = 0
    i = 0
    while i < len(vars.ready_order_list):
        time = time + (settings.order_waiting_time / i)
        i = i + 1
    return time


def order_countdown(t):
    import time
    while t and len(get_open_ready_orders()) > 0:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        vars.order_countdown = timeformat
        time.sleep(1)
        if system_vars.door_is_open is False:
            t -= 1


def get_order_countdown():
    return vars.order_countdown


def get_open_ready_orders():
    orders = []
    i = 0
    while i < len(vars.ready_order_list):
        if vars.ready_order_list[i]['open'] is True:
            orders.append(vars.ready_order_list[i])
        i = i + 1
    return orders


def confirm_order(index):
    vars.ready_order_list[index]['open'] = False
