from django.shortcuts import render

from config.settings import BASE_DIR
from django_ec.models import items
import environ
# Create your views here.

def index(request):
    return render(request, 'index.html')

def listfunc(request):
    object_list = items.objects.all()
    return render(request, 'django_ec/list.html',{"object_list":object_list})
