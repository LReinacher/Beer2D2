# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponseNotAllowed

def index(request):
    return render(request, 'index.html', {})
