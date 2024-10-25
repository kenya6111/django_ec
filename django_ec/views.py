from django.shortcuts import render

from django_ec.models import items

# Create your views here.

def index(request):
    return render(request, 'index.html')

def listfunc(request):
    object_list = items.objects.all()
    print(object_list)
    
    return render(request, 'django_ec/list.html',{"object_list":object_list})
