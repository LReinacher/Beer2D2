#! /usr/bin/python3
# -*- coding: utf-8 -*-
from RestAPI.rest_api_framework import get, post, request, default_app, static_file, route
import os
import system_vars
import settings
import json
import Orders.order_functions as order_functions
import SlackBot.slack_functions as slack_functions
import MotorControl.motor_functions as motor_functions
import CamTracking.webcam_functions as webcam_functions
import RestAPI.vars as vars
from datetime import datetime
import time
from threading import Thread

dir_path = os.path.dirname(os.path.realpath(__file__))
app = default_app()


@post('/direct')
def motorDirect():
    body = request.body.read()
    body = json.loads(body)
    if 'user' and 'remote_key' in body:
        user = body['user']
        remote_key = body['remote_key']
    else:
        return {'status': 'error', 'code': 117, 'message': "parameter missing"}
    if system_vars.remote_control:
        if system_vars.remote_control_user == user:
            if vars.remote_control_key == remote_key:
                motor_l = request.query.motor_l
                motor_r = request.query.motor_r

                if motor_l is None:
                    return {'status': 'error', 'code': 105, 'message': 'speed for left motor not defined'}

                if motor_r is None:
                    return {'status': 'error', 'code': 106, 'message': 'speed for right motor not defined'}

                vars.last_command_time = datetime.now().timestamp()
                vars.security_stopped = False
                if motor_l != "0" or motor_r != "0":
                    vars.last_active_command_time = datetime.now().timestamp()
                print('Setting Motors to: ' + str(motor_l) + ' | ' + str(motor_r) + ' by ' + user)
                response = motor_functions.set_motors_api(motor_l, motor_r)

                if response == 0:
                    return {'status': 'success', 'code': 100,
                            'message': 'left motor set to ' + motor_l + ' - right motor set to  ' + motor_r}
                elif response == 1:
                    return {'status': 'error', 'code': 107, 'message': 'Unknown left speed Identifier'}
                elif response == 2:
                    return {'status': 'error', 'code': 108, 'message': 'Unknown right speed Identifier'}
                elif response == 3:
                    return {'status': 'error', 'code': 109,
                            'message': 'Invalid left speed Identifier - speed Identifier has to be float'}
                elif response == 4:
                    return {'status': 'error', 'code': 110,
                            'message': 'Invalid right speed Identifier - speed Identifier has to be float'}
            else:
                return {'status': 'error', 'code': 116,
                        'message': "Authorisation failed"}
        else:
            return {'status': 'error', 'code': 104,
                    'message': "already remote controlled by:" + system_vars.remote_control_user,
                    'data': {'user': system_vars.remote_control_user}}
    else:
        return {'status': 'error', 'code': 111, 'message': 'remote control not enabled'}


@route('/', method=['GET', 'POST'])
def index():
        return static_file('control.html', root=dir_path + '/static')


@post('/add-order')
def add_order():
    body = request.body.read()
    body = json.loads(body)
    if 'location' and 'user' and 'verify_key' and 'timestamp' in body:
        location = body['location']
        email = body['user']
        verify_key = body['verify_key']
        timestamp = body['timestamp']
    else:
        return {'status': 'error', 'code': 117, 'message': "parameter missing"}
    priority = request.query.priority
    if verify_call(verify_key, timestamp, email, vars.secret_keys['add_order']):
        result, response = order_functions.add_order(email, location, 'email', priority)
        if result:
            return {'status': 'success', 'code': 100, 'message': response}
        else:
            return {'status': 'error', 'code': 199, 'message': response}
    else:
        return {'status': 'error', 'code': 116, 'message': 'Authorisation failed'}


@post('/cancel-order')
def delete_order():
    body = request.body.read()
    body = json.loads(body)
    if 'user' and 'verify_key' and 'timestamp' in body:
        email = body['user']
        verify_key = body['verify_key']
        timestamp = body['timestamp']
    else:
        return {'status': 'error', 'code': 117, 'message': "parameter missing"}
    if verify_call(verify_key, timestamp, email, vars.secret_keys['cancel_order']):
        if order_functions.delete_oder(email, 'email'):
            return {'status': 'success', 'code': 100, 'message': "order canceled"}
        else:
            return {'status': 'error', 'code': 101, 'message': "no open order"}
    else:
        return {'status': 'error', 'code': 116, 'message': 'Authorisation failed'}


@post('/confirm-delivery')
def confirm_delivery():
    body = request.body.read()
    body = json.loads(body)
    if 'user' and 'verify_key' and 'timestamp' in body:
        email = body['user']
        verify_key = body['verify_key']
        timestamp = body['timestamp']
    else:
        return {'status': 'error', 'code': 117, 'message': "parameter missing"}
    id = slack_functions.get_id_by_email(email)
    index = order_functions.check_user_order(id, email)
    if verify_call(verify_key, timestamp, email, vars.secret_keys['confirm_order']):
        if index >= 0:
            return {'status': 'success', 'code': 100, 'message': "order marked as delivered"}
        else:
            return {'status': 'error', 'code': 101, 'message': "no open order"}
    else:
        return {'status': 'error', 'code': 116, 'message': 'Authorisation failed'}


@get('/get-orders')
def get_orders():
    orders = order_functions.get_orders()
    return {'status': 'success', 'code': 100, 'message': "open orders", 'data': {'orders': orders}}


@post('/toggle-remote-control')
def toggle_remote_control():
    body = request.body.read()
    body = json.loads(body)
    if 'user' and 'status' in body:
        user = body['user']
        status = body['status']
    else:
        return {'status': 'error', 'code': 117, 'message': "parameter missing"}
    if user is None:
        return {'status': 'error', 'code': 115, 'message': "user not defined"}
    if status == "enable":
        if system_vars.remote_control is False:
            if 'timestamp' and 'verify_key' in body:
                verify_key = body['verify_key']
                timestamp = body['timestamp']
            else:
                return {'status': 'error', 'code': 117, 'message': "parameter missing"}
            if verify_call(verify_key, timestamp, user, vars.secret_keys['enable_remote']):
                vars.last_command_time = datetime.now().timestamp()
                vars.security_stopped = False
                vars.last_active_command_time = datetime.now().timestamp()
                system_vars.remote_control = True
                system_vars.remote_control_user = user
                remote_key = gen_control_key()
                vars.remote_control_key = remote_key
                send_remote_control_update_call()
                motor_functions.set_motors_api(0, 0)
                return {'status': 'success', 'code': 100, 'message': "remote control enabled successfully", 'data': {'remote_key': remote_key}}
            else:
                return {'status': 'error', 'code': 116, 'message': 'Authorisation failed'}
        else:
            return {'status': 'error', 'code': 103,
                    'message': "already remote controlled by:" + system_vars.remote_control_user,
                    'data': {'user': system_vars.remote_control_user}}
    elif status == "disable":
        if system_vars.remote_control is True:
            if 'remote_key' in body:
                remote_key = body['remote_key']
            else:
                return {'status': 'error', 'code': 117, 'message': "parameter missing"}
            if system_vars.remote_control_user == user:
                if vars.remote_control_key == remote_key:
                    system_vars.remote_control = False
                    system_vars.remote_control_user = None
                    vars.remote_control_key = None
                    send_remote_control_update_call()
                    return {'status': 'success', 'code': 100, 'message': "remote control disabled successfully"}
                else:
                    return {'status': 'error', 'code': 116,
                            'message': "Authorisation failed"}
            else:
                return {'status': 'error', 'code': 104,
                        'message': "not your remote session - remote controlled by:" + system_vars.remote_control_user,
                        'data': {'user': system_vars.remote_control_user}}
        else:
            return {'status': 'error', 'code': 102, 'message': "no open remote session"}


def api_security_stop_timer():
    print(system_vars.colorcode['ok'] + "OK: REST-API-SECURITY-STOP-SYSTEM STARTED" + system_vars.colorcode[
        'reset'])
    while True:
        if system_vars.remote_control:
            if vars.last_command_time is not None:
                if (vars.security_stopped is False and vars.last_command_time - datetime.now().timestamp()) < (vars.security_stop_timer * -1):
                    vars.security_stopped = True
                    motor_functions.set_motors_api(0, 0)
                    print(system_vars.colorcode['warning'] + "WARNING: SECURITY-STOP EXECUTED!" + system_vars.colorcode[
                        'reset'])
        time.sleep(0.1)


def api_inactivity_timer():
    print(system_vars.colorcode['ok'] + "OK: REST-API-INACTIVITY-SYSTEM STARTED" + system_vars.colorcode[
        'reset'])
    while True:
        if system_vars.remote_control:
            if vars.last_active_command_time is not None:
                if (vars.last_active_command_time - datetime.now().timestamp()) < (vars.inactivity_timer * -1):
                    motor_functions.set_motors_api(0, 0)
                    system_vars.remote_control = False
                    system_vars.remote_control_user = None
                    vars.remote_control_key = None
                    send_remote_control_update_call()
                    print(system_vars.colorcode['warning'] + "WARNING: REMOTE-CONTROL SESSION TERMINATED DUE TO INACTIVITY!" + system_vars.colorcode[
                        'reset'])
        time.sleep(0.1)

def start():
    print(system_vars.colorcode['info'] + "INFO: STARTING REST-API-SECURITY-STOP-SYSTEM..." + system_vars.colorcode['reset'])
    security_thread = Thread(target=api_security_stop_timer, args=(), name="Security-Stop", daemon=False)
    security_thread.start()
    print(system_vars.colorcode['info'] + "INFO: STARTING REST-API-INACTIVITY-SYSTEM..." + system_vars.colorcode[
        'reset'])
    inactivity_thread = Thread(target=api_inactivity_timer, args=(), name="Inactivity", daemon=False)
    inactivity_thread.start()
    application = default_app()
    from paste import httpserver
    print(system_vars.colorcode['ok'] + "OK: REST-API ONLINE" + system_vars.colorcode['reset'])
    if settings.localhost:
        httpserver.serve(application, host="127.0.0.1", port=8000)
    else:
        httpserver.serve(application, host=settings.ip, port=8000)



def send_order_update_call():
    data_update_thread = Thread(target=send_order_update_call_util, args=(), name="Update Orders Call", daemon=False)
    data_update_thread.start()


def send_order_update_call_util():
    send_api_call(vars.interface_api_url + '/update-orders', json.dumps(order_functions.get_orders()),
                  generate_verification_hash('', str(datetime.utcnow().timestamp()), vars.secret_keys['update_order_list']), str(datetime.utcnow().timestamp()))


def send_remote_control_update_call():
    data_update_thread = Thread(target=send_remote_control_update_call_util, args=(), name="Update Remote Control Call", daemon=False)
    data_update_thread.start()


def send_remote_control_update_call_util():
    send_api_call(vars.interface_api_url + '/update-remote-control',
                  json.dumps({'remote_enabled': system_vars.remote_control, 'remote_user': system_vars.remote_control_user}),
                  generate_verification_hash('', str(datetime.utcnow().timestamp()), vars.secret_keys['update_remote_control_status']), str(datetime.utcnow().timestamp()))


def send_last_barcode_update_call():
    data_update_thread = Thread(target=send_last_barcode_update_call_util, args=(), name="Update Last Barcode Call", daemon=False)
    data_update_thread.start()


def send_last_barcode_update_call_util():
    send_api_call(vars.interface_api_url + '/update-last-barcode', webcam_functions.get_last_barcode(),
                  generate_verification_hash('', str(datetime.utcnow().timestamp()), vars.secret_keys['update_last_barcode']), str(datetime.utcnow().timestamp()))


def send_api_call(url, data, verify_key, timestamp):
    import requests
    try:
        r = requests.post(url, data={'data': data, 'verify_key': verify_key, 'timestamp': timestamp})
    except:
        pass


def gen_control_key():
    import string
    import random
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def verify_call(hash, timestamp, identifier, secret_key):
    import hashlib
    from datetime import datetime
    try:
        timestamp = float(timestamp)
    except:
        return False
    if datetime.utcnow().timestamp() - timestamp < 30:
        compare_hash = hashlib.sha224((identifier + secret_key + str(timestamp)).encode('UTF-8')).hexdigest()
        if hash == compare_hash:
            return True
    return False


def generate_verification_hash(identifier, timestamp, secret_key):
    import hashlib
    hash = hashlib.sha224((identifier + secret_key + timestamp).encode('UTF-8')).hexdigest()
    return hash

