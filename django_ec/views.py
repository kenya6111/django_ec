from django.shortcuts import render, get_object_or_404

from config.settings import BASE_DIR
from django_ec.models import items
import environ
# Create your views here.

def index(request):
    return render(request, 'index.html')

def listfunc(request):
    object_list = items.objects.all()
    print(object_list)
    print(object_list[0].pk)
    return render(request, 'django_ec/list.html',{"object_list":object_list})


def detailfunc(request, pk):
    object = get_object_or_404(items, pk=pk)

    object_list = items.objects.order_by('first_name')
    return render(request, 'django_ec/detail.html', {'object':object})