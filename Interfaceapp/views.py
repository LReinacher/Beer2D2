# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse, Http404, HttpResponseNotAllowed


def login(request):
    return render(request, 'login.html', {})


def dashboard(request):
    return render(request, 'dashboard.html', {'username': 'Lion Reinacher'})
