from django.shortcuts import get_object_or_404, render

from config.settings import BASE_DIR
from django_ec.models import ItemModel
import environ
from .constants.consts import Menu
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

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
    if request.method == 'POST':
        product_name = request.POST.get("product-name")
        star_from = request.POST.get("star_from")
        star_to = request.POST.get("star_to")
        price = request.POST.get("price")
        is_sale = request.POST.get("is-sale")
        create_date_from = request.POST.get("create-date-from")
        create_date_to = request.POST.get("create-date-to")

        object_list = ItemModel.objects.all()

        error_list=[]
        validate(error_list, star_from, star_to)

        if product_name is not None:
            object_list = object_list.filter(name__contains=product_name)
        
        # if star is not None:
        #     star = object_list.filter(name=star)
        # if price is not None:
        #     object_list = object_list.filter(name=price)
        # if product_name is not None:
        #     object_list = object_list.filter(name=product_name)


        return render(request, 'django_ec/admin/list.html', {'object_list':object_list, 'error_list':error_list})
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return render(request, 'login.html', {'context':'logged in !!'})
        # else:
        #     return render(request, 'login.html', {'context':' not logged in !!'})

    # return render(request, 'login.html', {'context':'get method '})
    return render(request, 'django_ec/admin/list.html', {})
def admincreatefunc(request):
    return render(request, 'django_ec/admin/create.html', {})
def admineditfunc(request,pk):
    if request.method == 'POST':

        return render(request, 'django_ec/admin/list.html', {'object':object})

    else:
        # GETの場合
        object = get_object_or_404(ItemModel, pk=pk)
        return render(request, 'django_ec/admin/edit.html', {'object':object})

    return render(request, 'django_ec/admin/edit.html', {'object':object})
def admindeletefunc(request):
    return render(request, 'django_ec/admin/delete.html', {})

class ItemCreate(CreateView):
    template_name = 'django_ec/admin/create.html'
    model = ItemModel
    fields = ('name','star','image','price','is_sale')
    success_url = reverse_lazy('list') # データの作成完了した後の遷移先

    def form_invalid(self, form):
        print(form.errors)  # デバッグ用にエラー内容を出力
        return super().form_invalid(form)

class ItemEdit(UpdateView):
    template_name = 'django_ec/admin/edit.html'
    model = ItemModel
    fields = ('name','star','image','price','is_sale')
    success_url = reverse_lazy('list')

class ItemDelete (DeleteView):
    template_name = 'django_ec/admin/delete.html'
    model = ItemModel
    success_url = reverse_lazy('list')


def validate(error_list, star_from, star_to):
    if star_from is not None and star_to is not None:
        if star_from >= star_to:
            return error_list.append("星数の開始数は終了数より小さい値を設定してください")