from django.shortcuts import get_object_or_404, render

from config.settings import BASE_DIR
from django_ec.models import ItemModel
import environ
from .constants.consts import Menu

# Create your views here.

def index(request):
    return render(request, 'index.html')

def listfunc(request):
    object_list = ItemModel.objects.all()
    return render(request, 'django_ec/list.html',{"object_list":object_list})

def detailfunc(request, pk):
    object = get_object_or_404(ItemModel, pk=pk)
    print(object.created_at)
    print(object.pk)

    object_list = ItemModel.objects.order_by('created_at').reverse()[:4]

    print(object_list)
    return render(request, 'django_ec/detail.html', {'object':object,'object_list':object_list})


def adminmenufunc(request):
    menu_list = list(Menu)
    print(menu_list)
    for ob in menu_list:
        print(ob.name)
        print(ob.id)
    return render(request, 'django_ec/admin/menu.html', {'menu_list':menu_list})

def adminlistfunc(request):
    object_list = ItemModel.objects.all()
    return render(request, 'django_ec/admin/list.html', {'object_list':object_list})
def admincreatefunc(request):
    return render(request, 'django_ec/admin/create.html', {})
def admineditfunc(request):
    return render(request, 'django_ec/admin/edit.html', {})
def admindeletefunc(request):
    return render(request, 'django_ec/admin/delete.html', {})
