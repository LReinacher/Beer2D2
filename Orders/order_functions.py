#! /usr/bin/python3
# -*- coding: utf-8 -*-
import Orders.vars as vars
import settings
import system_vars
import SQLite.database_functions as database_functions


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


def check_user_ready_order(user, ident2=None):
    i = len(vars.ready_order_list)
    while i > 0:
        if vars.ready_order_list[i - 1]['user'] == user or vars.ready_order_list[i - 1]['user'] == ident2:
            return i - 1
        i = i - 1
    return -1


def add_order(user, room, type, priority=False):
    import SlackBot.slack_functions as slack_functions
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

        import UI.ui_functions as ui_functions
        ui_functions.force_order_update()
        database_functions.upload_order(room, user)
        return True, position
    else:
        return False, result


def delete_oder(identifier, type):
    import SlackBot.slack_functions as slack_functions
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
        import UI.ui_functions as ui_functions
        ui_functions.force_order_update()
        database_functions.set_canceled(identifier)
        return True
    else:
        return False


def check_user_already_placed_order(identifier, type):
    import SlackBot.slack_functions as slack_functions
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
    while i < len(vars.order_que) and 'room' in vars.order_que[i] and vars.order_que[i]['room'] == destination:
        order = vars.order_que[i]
        order.update({'open': True})
        orders.append(order)
        i = i + 1
    return orders


def get_ready_order_list():
    return vars.ready_order_list


def start_drop_off():
    import SlackBot.slack_functions as slack_functions
    import MotorControl.motor_functions as motor_functions
    import LED.led_functions as led_functions
    led_functions.set_led('green')

    system_vars.destination_reached = True
    motor_functions.stop_both()

    orders = get_destination_all_orders(get_current_destination())
    vars.ready_order_list = orders
    vars.drop_off_running = True

    wait_time = calc_order_wait_time()
    mins, secs = divmod(wait_time, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    vars.order_countdown = timeformat

    if settings.touchscreen_enabled:
        import UI.ui_functions as ui_functions
        ui_functions.start_drop_off()

    i = 0
    import SlackBot.responses as responses
    while i < len(orders):
        if 'type' in orders[i]:
            if orders[i]['type'] == 'slack':
                slack_functions.send_dm(orders[i]['user'], responses.order_ready % vars.order_countdown)
            else:
                user_id = slack_functions.get_id_by_email(orders[i]['user'])
                if user_id is not None:
                    slack_functions.send_dm(orders[i]['user'], responses.order_ready % vars.order_countdown)
                else:
                    import mail_system
                    mail_system.send_mail(responses.order_ready % vars.order_countdown, responses.order_ready % vars.order_countdown, orders[i]['user'])
        i = i + 1

    order_countdown(wait_time)
    end_drop_off()


def end_drop_off():
    import Locations.location_functions as location_functions
    import CamTracking.webcam_functions as webcam_functions
    import LED.led_functions as led_functions
    import UI.ui_functions as ui_functions
    led_functions.set_led('blue')

    i = 0
    while i < len(vars.ready_order_list):
        if 'type' in vars.ready_order_list[i]:
            delete_oder(0, 'index')
        i = i + 1
    vars.drop_off_running = False
    vars.ready_order_list = []
    ui_functions.force_order_update()

    location_functions.leave_location(webcam_functions.get_last_barcode())


def calc_order_wait_time():
    time = 0
    i = 0
    while i < len(vars.ready_order_list):
        if 'type' in vars.ready_order_list[i]:
            time = time + (settings.order_waiting_time / (i + 1))
        i = i + 1
    return int(round(time))


def order_countdown(t):
    import time
    import LED.led_functions as led_functions
    while t and len(get_open_ready_orders()) > 0:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        vars.order_countdown = timeformat
        if t == 20:
            led_functions.set_led('yellow')
        time.sleep(1)
        if system_vars.door_is_open is False:
            t -= 1


def get_order_countdown():
    return vars.order_countdown


def get_open_ready_orders():
    orders = []
    i = 0
    while i < len(vars.ready_order_list):
        if 'open' in vars.ready_order_list[i]:
            if vars.ready_order_list[i]['open'] is True:
                orders.append(vars.ready_order_list[i])
        i = i + 1
    return orders


def confirm_order(user_or_index, type=None):
    import SlackBot.slack_functions as slack_functions
    if type == "slack":
        email = slack_functions.get_email_by_id(user_or_index)
        if vars.drop_off_running:
            index = check_user_ready_order(user_or_index, email)
            if index > -1:
                vars.ready_order_list[index]['open'] = False
                return True
        index = check_user_order(user_or_index, email)
        if index > -1:
            delete_oder(index, "index")
            import UI.ui_functions as ui_functions
            ui_functions.force_order_update()
            return True
        else:
            return False
    elif type == "interface":
        user_id = slack_functions.get_id_by_email(user_or_index)
        if vars.drop_off_running:
            index = check_user_ready_order(user_or_index, user_id)
            if index > -1:
                vars.ready_order_list[index]['open'] = False
                return True
        index = check_user_order(user_or_index, user_id)
        if index > -1:
            delete_oder(index, "index")
            import UI.ui_functions as ui_functions
            ui_functions.force_order_update()
            return True
        else:
            return False
    elif type is None:
        vars.ready_order_list[user_or_index]['open'] = False
