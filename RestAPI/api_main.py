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
    user = request.query.user
    #print('Motor Direct request by: ' + user)
    if system_vars.remote_control:
        if system_vars.remote_control_user == user:
            motor_l = request.query.motor_l
            motor_r = request.query.motor_r

            if motor_l is None:
                return {'status': 'error', 'message': 'speed for left motor not defined'}

            if motor_r is None:
                return {'status': 'error', 'message': 'speed for right motor not defined'}

            vars.last_command_time = datetime.now().timestamp()
            vars.security_stopped = False
            if motor_l != "0" or motor_r != "0":
                vars.last_active_command_time = datetime.now().timestamp()
            print('Setting Motors to: ' + str(motor_l) + ' | ' + str(motor_r) + ' by ' + user)
            response = motor_functions.set_motors_api(motor_l, motor_r)
        
            if response == 0:
                return {'status': 'success', 'message': 'left motor set to ' + motor_l + ' - right motor set to  ' + motor_r}
            elif response == 1:
                return {'status': 'error', 'message': 'Unknown left speed Identifier'}
            elif response == 2:
                return {'status': 'error', 'message': 'Unknown right speed Identifier'}
            elif response == 3:
                return {'status': 'error', 'message': 'Invalid left speed Identifier - speed Identifier has to be float'}
            elif response == 4:
                return {'status': 'error', 'message': 'Invalid right speed Identifier - speed Identifier has to be float'}
        else:
            return {'status': 'error', 'message': "already remote controlled by:" + system_vars.remote_control_user}
    else:
        return {'status': 'error', 'message': 'remote control not enabled'}


@route('/', method=['GET', 'POST'])
def index():
        return static_file('control.html', root=dir_path + '/static')


@get('/add-order')
def add_order():
    location = request.query.location
    email = request.query.email
    priority = request.query.priority
    result, response = order_functions.add_order(email, location, 'email', priority)
    if result:
        return {'status': 'success', 'message': response}
    else:
        return {'status': 'error', 'message': response}


@post('/cancel-order')
def delete_order():
    email = request.query.email
    if order_functions.delete_oder(email, 'email'):
        return {'status': 'success', 'message': "order canceled"}
    else:
        return {'status': 'error', 'message': "no open order"}


@post('/confirm-delivery')
def confirm_delivery():
    email = request.query.email
    id = slack_functions.get_id_by_email(email)
    index = order_functions.check_user_order(id, email)
    if index >= 0:
        return {'status': 'success', 'message': "order marked as delivered"}
    else:
        return {'status': 'error', 'message': "no open order"}


@get('/get-orders')
def get_orders():
    orders = order_functions.get_orders()
    return orders


@post('/toggle-remote-control')
def toggle_remote_control():
    status = request.query.status
    user = request.query.user
    if user is None:
        return {'status': 'error', 'message': "user not defined"}
    if status == "enable":
        if system_vars.remote_control is False:
            vars.last_command_time = datetime.now().timestamp()
            vars.security_stopped = False
            vars.last_active_command_time = datetime.now().timestamp()
            system_vars.remote_control = True
            system_vars.remote_control_user = user
            motor_functions.set_motors_api(0, 0)
            return {'status': 'success', 'message': "remote control enabled successfully"}
        else:
            return {'status': 'error', 'message': "already remote controlled by:" + system_vars.remote_control_user}
    elif status == "disable":
        if system_vars.remote_control is True:
            if system_vars.remote_control_user == user:
                system_vars.remote_control = False
                system_vars.remote_control_user = None
                return {'status': 'success', 'message': "remote control disabled successfully"}
            else:
                return {'status': 'error', 'message': "not your remote session - remote controlled by:" + system_vars.remote_control_user}
        else:
            return {'status': 'error', 'message': "no open remote session"}


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



#SEND DATA
def changed_data_handler():
    print(system_vars.colorcode['ok'] + "OK: DATA UPLOAD API ONLINE" + system_vars.colorcode[
        'reset'])
    old_remote_control = system_vars.remote_control
    old_orders = order_functions.get_orders()
    old_last_barcode = webcam_functions.get_last_barcode()
    while True:
        if system_vars.remote_control != old_remote_control:
            old_remote_control = system_vars.remote_control
        if order_functions.get_orders() != old_orders:
            old_orders = order_functions.get_orders()
        if webcam_functions.get_last_barcode() != old_last_barcode:
            old_last_barcode = webcam_functions.get_last_barcode()
        time.sleep(0.2)


def send_api_call(url, data):
    import requests
    r = requests.post(url, data={'data': data})
    print(r.status_code, r.reason)

