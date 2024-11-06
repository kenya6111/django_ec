from django.shortcuts import get_object_or_404, render

from config.settings import BASE_DIR
from django_ec.models import ItemModel
import environ
from .constants.consts import Menu
from django.views.generic import CreateView,UpdateView,DeleteView, ListView
from django.urls import reverse_lazy
from .basic_auth_view import logged_in_or_basicauth
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

@logged_in_or_basicauth()
def adminmenufunc(request):
    menu_list = list(Menu)
    print(menu_list)
    for ob in menu_list:
        print(ob.name)
        print(ob.id)
    return render(request, 'django_ec/admin/menu.html', {'menu_list':menu_list})

class ItemList(ListView):

    template_name = 'django_ec/admin/list.html'
    model = ItemModel
    def get_queryset(self):
        params = {
            "product_name": self.request.GET.get("product-name"),
            "star_from": self.request.GET.get("star_from"),
            "star_to": self.request.GET.get("star_to"),
            "price_from": self.request.GET.get("price_from"),
            "price_to": self.request.GET.get("price_to"),
            "is_sale": self.request.GET.get("is-sale"),
            "is_not_sale": self.request.GET.get("is-not-sale"),
            "create_date_from": self.request.GET.get("create-date-from"),
            "create_date_to": self.request.GET.get("create-date-to"),
        }
        return ItemModel.objects.search(**params)

@logged_in_or_basicauth()
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


def validate(error_list, star_from, star_to, price_from, price_to, create_date_from, create_date_to):
    if len(star_from) !=0 and len(star_to) != 0:
        if star_from >= star_to:
            error_list.append("星数の開始数は終了数より小さい値を設定してください")
            return False

    if len(price_from) !=0 and len(price_to) != 0:
        if price_from >= price_to:
            error_list.append("値段の開始数は終了数より小さい値を設定してください")
            return False

    if len(create_date_from) !=0 and len(create_date_to) != 0:
        if create_date_from >= create_date_to:
            error_list.append("作成日の開始日は終了日より小さい値を設定してください")
            return False
    
    return True