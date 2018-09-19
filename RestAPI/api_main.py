from RestAPI.rest_api_framework import get, post, request, default_app, static_file, route
import os
import system_vars
import settings
import json
from Orders import order_functions
from SlackBot import slack_functions

dir_path = os.path.dirname(os.path.realpath(__file__))
app = default_app()


@post('/direct')
def motorDirect():
    motor = request.query.motor
    command = request.query.command
    speed = request.query.speed

    if motor is None:
        return {'status': 'error', 'message': 'Missing Motor Identifier'}

    if command is None:
        return {'status': 'error', 'message': 'Missing Command'}

    response = system_vars.motorControlInstance.motor(motor, command, speed)

    if response == 0:
        return {'status': 'success', 'message': 'Motor ' + motor + ' executing ' + command}
    elif response == 1:
        return {'status': 'error', 'message': 'Unknown Motor Identifier'}
    else:
        return {'status': 'error', 'message': 'Unknown Command'}


@route('/', method=['GET', 'POST'])
def index():
        return static_file('control.html', root=dir_path + '/static')


@post('/add-order')
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


def start():
    application = default_app()
    from paste import httpserver
    print(system_vars.colorcode['ok'] + "OK: REST-API STARTED" + system_vars.colorcode['reset'])
    if settings.localhost:
        httpserver.serve(application, host="127.0.0.1", port=8000)
    else:
        httpserver.serve(application, host=settings.ip, port=8000)