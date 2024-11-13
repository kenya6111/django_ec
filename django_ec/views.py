from django.shortcuts import get_object_or_404, render, redirect

from config.settings import BASE_DIR
from django_ec.models import ItemModel,ItemModel,CartModel,CartItemModel
import environ
from .constants.consts import Menu
from django.views.generic import CreateView,UpdateView,DeleteView, ListView
from django.urls import reverse_lazy
from basicauth.decorators import basic_auth_required
from django.utils.decorators import method_decorator
# Create your views here.

def index(request):
    return render(request, 'index.html')

def listfunc(request):
    cart = get_or_create_cart(request)
    item_num_sum = sum(item.quantity for item in cart.cart_items.all())
    object_list = ItemModel.objects.all()
    return render(request, 'django_ec/list.html',{"object_list":object_list, 'item_num_sum':item_num_sum})

def detailfunc(request, pk):
    cart = get_or_create_cart(request)
    item_num_sum = sum(item.quantity for item in cart.cart_items.all())
    object = get_object_or_404(ItemModel, pk=pk)
    object_list = ItemModel.objects.order_by('created_at').reverse()[:4]
    return render(request, 'django_ec/detail.html', {'object':object,'object_list':object_list, 'item_num_sum':item_num_sum})

@basic_auth_required
def adminmenufunc(request):
    menu_list = list(Menu)
    print(menu_list)
    for ob in menu_list:
        print(ob.name)
        print(ob.id)
    return render(request, 'django_ec/admin/menu.html', {'menu_list':menu_list})
@method_decorator(basic_auth_required, name='dispatch')
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

@method_decorator(basic_auth_required, name='dispatch')
class ItemCreate(CreateView):
    template_name = 'django_ec/admin/create.html'
    model = ItemModel
    fields = ('name','star','image','price','is_sale')
    success_url = reverse_lazy('admin_list') # データの作成完了した後の遷移先

    def form_invalid(self, form):
        print(form.errors)  # デバッグ用にエラー内容を出力
        return super().form_invalid(form)
@method_decorator(basic_auth_required, name='dispatch')
class ItemEdit(UpdateView):
    template_name = 'django_ec/admin/edit.html'
    model = ItemModel
    fields = ('name','star','image','price','is_sale')
    success_url = reverse_lazy('admin_list')

@method_decorator(basic_auth_required, name='dispatch')
class ItemDelete (DeleteView):
    template_name = 'django_ec/admin/delete.html'
    model = ItemModel
    success_url = reverse_lazy('admin_list')

def cartdetailfunc(request):
    cart = get_or_create_cart(request)
    item_num_sum = sum(item.quantity for item in cart.cart_items.all())
    item_price_sum = sum(item.Item.price*0.6*item.quantity if item.Item.is_sale else item.Item.price*item.quantity for item in cart.cart_items.all())

    # sessionからカート内情報取得
    # cart = request.session.get('cart', {})
    # id_list = cart.keys()

    print([item for item in cart.cart_items.all()])
    # objects = ItemModel.objects.filter(pk__in=id_list)

    # 表示用リストを作成
    # object_list = {}
    # for k, v in cart.items():
    #     object = ItemModel.objects.get(id = k)
    #     object_list[object] = v

    return render(request, 'django_ec/cart.html', {'object_list':[item for item in cart.cart_items.all()], 'item_num_sum':item_num_sum, 'item_price_sum':round(item_price_sum)})

def addcartfunc(request,pk):
    # cart = request.session.get('cart_id')
    cart = get_or_create_cart(request)
    print(111)
    print(cart)
    item = get_object_or_404(ItemModel,pk=pk)
    print(222)
    print(item)

    # CartItem = CartItemModel.objects.get(cart=cart , Item=item)
    # CartItemを取得または作成し、数量を増やす
    cart_item = CartItemModel.objects.get_or_create(cart=cart, Item=item)
    print(333)
    print(cart_item)
    if request.method == "POST":
        cart_item[0].quantity += int(request.POST['input_quantity'])
    else:
        cart_item[0].quantity += 1
    cart_item[0].save()

    item_num_sum = sum(item.quantity for item in cart.cart_items.all())

    print(444)
    print(cart.cart_items.all())
    print(444)
    print(item_num_sum)

    object_list = ItemModel.objects.all()

    return render(request, 'django_ec/list.html', {'object_list':object_list, 'item_num_sum':item_num_sum})


def removefromcartfunc(request, pk):
    cart = get_or_create_cart(request)
    item = get_object_or_404(ItemModel,pk=pk)
    CartItemModel.objects.get(cart=cart, Item=item).delete()

    # cart = request.session.get('cart')
    # cart.pop(pk)
    # request.session['cart'] = cart
    # object_list = ItemModel.objects.all()
    return redirect('cartdetail')


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

def get_or_create_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(CartModel, id=cart_id)
    else:
        cart = CartModel.objects.create()
        request.session['cart_id'] = cart.id
    return cart