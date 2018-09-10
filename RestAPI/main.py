from RestAPI.rest_api_framework import get, post, request, default_app, static_file, route
import os
import glob_vars
import settings

dir_path = os.path.dirname(os.path.realpath(__file__))
app = default_app()

@post('/direct')
def motorDirect():
    motor = request.query.motor
    command = request.query.command

    if motor is None:
        return {'status': 'Error', 'message': 'Missing Motor Identifier'}

    if command is None:
        return {'status': 'Error', 'message': 'Missing Command'}

    response = glob_vars.motorControlInstance.motor(motor, command)
    if response == 0:
        return {'status': 'Success', 'message': 'Motor ' + motor + ' executing ' + command}
    elif response == 1:
        return {'status': 'Error', 'message': 'Unknown Motor Identifier'}
    else:
        return {'status': 'Error', 'message': 'Unknown Command'}


@route('/', method=['GET', 'POST'])
def index():
        return static_file('control.html', root=dir_path + '/static')


def start():
    application = default_app()
    from paste import httpserver
    if settings.localhost:
        httpserver.serve(application, host="192.168.2.100", port=8000)
    else:
        httpserver.serve(application, host=settings.ip, port=8000)