from django.shortcuts import get_object_or_404, render

from config.settings import BASE_DIR
from django_ec.models import ItemModel
import environ
from .constants.consts import Menu
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .basic_auth_view import logged_in_or_basicauth
# Create your views here.

def index(request):
    return render(request, 'index.html')

def listfunc(request):
    object_list = ItemModel.objects.all()

    cart = request.session.get('cart', {})
    item_num_sum = 0
    for v in cart.values():
        item_num_sum += v

    return render(request, 'django_ec/list.html',{"object_list":object_list, 'item_num_sum':item_num_sum})

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

@logged_in_or_basicauth()
def adminlistfunc(request):
    if request.method == 'POST':
        product_name = request.POST.get("product-name")
        star_from = request.POST.get("star_from")
        star_to = request.POST.get("star_to")
        price_from = request.POST.get("price_from")
        price_to = request.POST.get("price_to")
        is_sale = request.POST.get("is-sale")
        is_not_sale = request.POST.get("is-not-sale")
        create_date_from = request.POST.get("create-date-from")
        create_date_to = request.POST.get("create-date-to")

        # 検索条件の入力値チェック
        error_list=[]
        result = validate(error_list, star_from, star_to, price_from, price_to, create_date_from, create_date_to)
        if(result == 0):
            return render(request, 'django_ec/admin/list.html', {'error_list':error_list})

        object_list = ItemModel.objects.all()

        if product_name is not None and len(product_name) != 0:
            object_list = object_list.filter(name__contains=product_name)
        if star_from is not None and len(star_from) != 0:
            object_list = object_list.filter(star__gte=star_from)
        if star_to is not None and len(star_to) != 0:
            object_list = object_list.filter(star__lte=star_to)
        if price_from is not None and len(price_from) != 0:
            object_list = object_list.filter(price__gte=price_from)
        if price_to is not None and len(price_to) != 0:
            object_list = object_list.filter(price__lte=price_to)
        if is_sale is not None and is_not_sale is not None:
            print("")
        elif is_sale is not None:
            object_list = object_list.filter(is_sale=1)
        elif is_not_sale is not None:
            object_list = object_list.filter(is_sale=0)
        if create_date_from is not None and len(create_date_from) != 0:
            object_list = object_list.filter(created_at__gte=create_date_from)
        if create_date_to is not None and len(create_date_to) != 0:
            object_list = object_list.filter(created_at__lte=create_date_to)

        return render(request, 'django_ec/admin/list.html', {'object_list':object_list, 'error_list':error_list})

    return render(request, 'django_ec/admin/list.html', {})

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

def cartdetailfunc(request):

    # sessionからカート内情報取得
    cart = request.session.get('cart', {})
    id_list = cart.keys()


    object_list = ItemModel.objects.filter(pk__in=id_list)
    print(object_list)

    # 注文数合計取得
    item_num_sum = 0
    for v in cart.values():
        item_num_sum += v

    # 注文総額を算出
    item_price_sum = 0
    for k, v in cart.items():
        object = ItemModel.objects.get(id = k)
        if object.is_sale:
            item_price_sum += object.price * 0.6 * v
        else:
            item_price_sum += object.price * v

    return render(request, 'django_ec/cart.html', {'object_list':object_list, 'item_num_sum':item_num_sum, 'item_price_sum':round(item_price_sum)})

def addcartfunc(request,pk):
    cart = request.session.get('cart', {})

    # 追加個数分を加算
    if pk in cart:
        item_num = cart.get(pk)
        item_num+=1
        cart[pk]=item_num
    else:
        cart[pk] = 1

    # sesionに保存
    request.session['cart'] = cart

    # カート内の商品数を算出
    item_num_sum = 0
    for v in cart.values():
        item_num_sum += v
    print(cart)
    object_list = ItemModel.objects.all()
    return render(request, 'django_ec/list.html', {'object_list':object_list, 'item_num_sum':item_num_sum})


def removefromcartfunc(request):
    # cart = request.session.get('cart', {})
    request.session["cart"] = {}
    object_list = ItemModel.objects.all()
    return render(request, 'django_ec/list.html', {'object_list':object_list})

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