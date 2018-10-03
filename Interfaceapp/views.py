# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse, Http404, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json

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
    hash = hashlib.sha224((identifier + secret_key + str(datetime.utcnow().timestamp())).encode('UTF-8')).hexdigest()
    return hash


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
            return HttpResponse('Timestamp missing', status=200)
        if verify_call(verify_key, timestamp, '', secret_keys['update_order_list']):
            orders = json.loads(request.POST.get('data'))
            #update orders here
            return HttpResponse(status=204)
        else:
            return HttpResponse('Authorisation Failed', status=200)

@csrf_exempt
def update_remote_control(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        verify_key = request.POST.get('verify_key')
        timestamp = request.POST.get('timestamp')
        if timestamp is None:
            return HttpResponse('Timestamp missing', status=200)
        if verify_call(verify_key, timestamp, '', secret_keys['update_remote_control_status']):
            data = json.loads(request.POST.get('data'))
            remote_control_enabled = data['remote_control_enabled']
            remote_control_user = data['remote_control_user']
            print('updated remote')
            #remote info here
            return HttpResponse(status=204)
        else:
            return HttpResponse('Authorisation Failed', status=200)

@csrf_exempt
def update_last_barcode(request):
    if request.method == 'GET':
        return HttpResponse(status=405)
    elif request.method == 'POST':
        verify_key = request.POST.get('verify_key')
        timestamp = request.POST.get('timestamp')
        if timestamp is None:
            return HttpResponse('Timestamp missing', status=200)
        if verify_call(verify_key, timestamp, '', secret_keys['update_last_barcode']):
            last_barcode = request.POST.get('data')
            #update last barcode here
            print('updated barcode')
            return HttpResponse(status=204)
        else:
            return HttpResponse('Authorisation Failed', status=200)



