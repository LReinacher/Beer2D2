# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse, Http404, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime


secret_keys = {'add_order': '45Aa*+=H5Nc_NdLm',
                'cancel_order': '^SF%NqDZB8av_KbB',
                'confirm_order': 'EdHD&k5X$y4UTv%z',
                'enable_remote': '@Qzc?UwqkVbh5z@W',
                'update_remote_control_status': 'A5_8umdWZd84RLar',
                'update_order_list': 'yYRJ6=P*H9e7x^nA',
                'update_last_barcode': '9qm*YAG#rQJK+fY^'}


def generate_verification_hash(identifier, secret_key):
    import hashlib
    from datetime import datetime
    timestamp = str(datetime.utcnow().timestamp())
    hash = hashlib.sha224((identifier + secret_key + timestamp).encode('UTF-8')).hexdigest()
    return hash, timestamp


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


def login(request):
    return render(request, 'login.html', {})


def dashboard(request):
    return render(request, 'dashboard.html', {'username': 'Lion Reinacher'})

@csrf_exempt
def update_orders(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        verify_key = request.POST.get('verify_key')
        timestamp = request.POST.get('timestamp')
        if timestamp is None:
            return HttpResponse('Timestamp missing', status=422)
        if verify_call(verify_key, timestamp, '', secret_keys['update_order_list']):
            orders = json.loads(request.POST.get('data'))
            #update orders here
            print('update orders')
            return HttpResponse(status=204)
        else:
            return HttpResponse('Authorisation Failed', status=401)

@csrf_exempt
def update_remote_control(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        verify_key = request.POST.get('verify_key')
        timestamp = request.POST.get('timestamp')
        if timestamp is None:
            return HttpResponse('Timestamp missing', status=422)
        if verify_call(verify_key, timestamp, '', secret_keys['update_remote_control_status']):
            data = json.loads(request.POST.get('data'))
            remote_control_enabled = data['remote_control_enabled']
            remote_control_user = data['remote_control_user']
            print('updated remote')
            #remote info here
            return HttpResponse(status=204)
        else:
            return HttpResponse('Authorisation Failed', status=401)

@csrf_exempt
def update_last_barcode(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        verify_key = request.POST.get('verify_key')
        timestamp = request.POST.get('timestamp')
        if timestamp is None:
            return HttpResponse('Timestamp missing', status=422)
        if verify_call(verify_key, timestamp, '', secret_keys['update_last_barcode']):
            last_barcode = request.POST.get('data')
            #update last barcode here
            print('updated barcode')
            return HttpResponse(status=204)
        else:
            return HttpResponse('Authorisation Failed', status=401)


def add_order(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        user = request.POST.get('user')
        location = request.POST.get('location')
        if user is not None and location is not None:
            verify_key, timestamp = generate_verification_hash(user, secret_keys['add_order'])
            response, status_code = send_api_call('/add-order', {'user': user, 'location': location}, verify_key, timestamp)
            if status_code == 200:
                return JsonResponse(response, safe=False)
            else:
                return HttpResponse('API answered with html-code: ' + str(status_code), status=900)
        else:
            return HttpResponse('missing parameter(s)', status=422)


def cancel_order(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        user = request.POST.get('user')
        if user is not None:
            verify_key, timestamp = generate_verification_hash(user, secret_keys['cancel_order'])
            response, status_code = send_api_call('/cancel-order', {'user': user}, verify_key, timestamp)
            if status_code == 200:
                return JsonResponse(response, safe=False)
            else:
                return HttpResponse('API answered with html-code: ' + str(status_code), status=900)
        else:
            return HttpResponse('missing parameter(s)', status=422)


def confirm_order(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        user = request.POST.get('user')
        if user is not None:
            verify_key, timestamp = generate_verification_hash(user, secret_keys['confirm_order'])
            response, status_code = send_api_call('/confirm-order', {'user': user}, verify_key, timestamp)
            if status_code == 200:
                return JsonResponse(response, safe=False)
            else:
                return HttpResponse('API answered with html-code: ' + str(status_code), status=900)
        else:
            return HttpResponse('missing parameter(s)', status=422)


def enable_remote(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        user = request.POST.get('user')
        if user is not None:
            verify_key, timestamp = generate_verification_hash(user, secret_keys['enable_remote'])
            response, status_code = send_api_call('/toggle-remote-control', {'user': user, 'status': 'enable'}, verify_key, timestamp)
            if status_code == 200:
                return JsonResponse(response, safe=False)
            else:
                return HttpResponse('API answered with html-code: ' + str(status_code), status=900)
        else:
            return HttpResponse('missing parameter(s)', status=422)


def disable_remote(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        user = request.POST.get('user')
        remote_key = request.POST.get('remote_key')
        if user is not None and remote_key is not None:
            response, status_code = send_api_call('/toggle-remote-control', {'user': user, 'status': 'disable', 'remote_key': remote_key}, "", "")
            if status_code == 200:
                return JsonResponse(response, safe=False)
            else:
                return HttpResponse('API answered with html-code: ' + str(status_code), status=900)
        else:
            return HttpResponse('missing parameter(s)', status=422)


def send_api_call(url, data, verify_key, timestamp):
    api_url = "http://127.0.0.1:8000"
    import requests
    data.update({'verify_key': verify_key, 'timestamp': timestamp})
    try:
        response = requests.post(api_url + url, data=json.dumps(data))
        text = response.text
        html_status_code = response.status_code
    except:
        html_status_code = 504
        text = "an exception occured handling the request"
    return text, html_status_code
