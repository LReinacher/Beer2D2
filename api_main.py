#! /usr/bin/python3
# -*- coding: utf-8 -*-
from rest_api_framework import get, post, request, default_app, static_file, route
import os
import vars as vars
from datetime import datetime
import time
from threading import Thread
import settings
import emu_functions

dir_path = os.path.dirname(os.path.realpath(__file__))
app = default_app()


@post('/direct')
def motorDirect():
    user = request.query.user
    #print('Motor Direct request by: ' + user)
    if vars.remote_control:
        if vars.remote_control_user == user:
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
            print('Motor Direct by: ' + user)
            response = settings.motor_control_response

            if response == 0:
                return {'status': 'success', 'code': 100, 'message': 'left motor set to ' + motor_l + ' - right motor set to  ' + motor_r}
            elif response == 1:
                return {'status': 'error', 'code': 107, 'message': 'Unknown left speed Identifier'}
            elif response == 2:
                return {'status': 'error', 'code': 108, 'message': 'Unknown right speed Identifier'}
            elif response == 3:
                return {'status': 'error', 'code': 109, 'message': 'Invalid left speed Identifier - speed Identifier has to be float'}
            elif response == 4:
                return {'status': 'error', 'code': 110, 'message': 'Invalid right speed Identifier - speed Identifier has to be float'}
        else:
            return {'status': 'error', 'code': 104, 'message': "already remote controlled by:" + vars.remote_control_user, 'data': {'user': vars.remote_control_user}}
    else:
        return {'status': 'error', 'code': 111, 'message': 'remote control not enabled'}


@post('/add-order')
def add_order():
    location = request.query.location
    email = request.query.user
    priority = request.query.priority
    result, response = emu_functions.add_order(email, location, 'email', priority)
    if result:
        return {'status': 'success', 'code': 100, 'message': response}
    else:
        return {'status': 'error', 'code': 199, 'message': response}


@post('/cancel-order')
def delete_order():
    email = request.query.user
    if emu_functions.delete_oder(email, 'email'):
        return {'status': 'success', 'code': 100, 'message': "order canceled"}
    else:
        return {'status': 'error', 'code': 101, 'message': "no open order"}


@post('/confirm-delivery')
def confirm_delivery():
    email = request.query.user
    index = emu_functions.check_user_order(email)
    if index >= 0:
        return {'status': 'success', 'code': 100, 'message': "order marked as delivered"}
    else:
        return {'status': 'error', 'code': 101, 'message': "no open order"}


@get('/get-orders')
def get_orders():
    orders = emu_functions.get_orders()
    return {'status': 'success', 'code': 100, 'message': "open orders", 'data': {'orders': orders}}


@post('/toggle-remote-control')
def toggle_remote_control():
    status = request.query.status
    user = request.query.user
    if user is None:
        return {'status': 'error', 'code': 115, 'message': "user not defined"}
    if status == "enable":
        if vars.remote_control is False:
            vars.remote_control = True
            vars.remote_control_user = user
            return {'status': 'success', 'code': 100, 'message': "remote control enabled successfully"}
        else:
            return {'status': 'error', 'code': 103, 'message': "already remote controlled by:" + vars.remote_control_user, 'data': {'user': vars.remote_control_user}}
    elif status == "disable":
        if vars.remote_control is True:
            if vars.remote_control_user == user:
                vars.remote_control = False
                vars.remote_control_user = None
                return {'status': 'success', 'code': 100, 'message': "remote control disabled successfully"}
            else:
                return {'status': 'error', 'code': 104, 'message': "not your remote session - remote controlled by:" + vars.remote_control_user, 'data': {'user': system_vars.remote_control_user}}
        else:
            return {'status': 'error', 'code': 102, 'message': "no open remote session"}


def start():
    application = default_app()
    from paste import httpserver
    if settings.localhost:
        httpserver.serve(application, host="127.0.0.1", port=8000)
    else:
        httpserver.serve(application, host=settings.ip, port=8000)


if __name__ == "__main__":
    start()