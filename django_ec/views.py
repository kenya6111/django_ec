from django.shortcuts import get_object_or_404, render, redirect

from config.settings import BASE_DIR
from django_ec.models import ItemModel,ItemModel,CartModel,CartItemModel,CheckoutModel,PurchaseDetailModel
import environ
from .constants.consts import Menu
from django.views.generic import CreateView,UpdateView,DeleteView, ListView
from django.urls import reverse_lazy
from basicauth.decorators import basic_auth_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request, 'index.html')

def listfunc(request):
    cart = get_or_create_cart(request)
    item_num_sum = cart.item_num_sum
    object_list = ItemModel.objects.all()
    return render(request, 'django_ec/list.html',{"object_list":object_list, 'item_num_sum':item_num_sum})

def detailfunc(request, pk):
    cart = get_or_create_cart(request)
    item_num_sum = cart.item_num_sum
    object = get_object_or_404(ItemModel, pk=pk)
    object_list = ItemModel.objects.order_by('created_at').reverse()[:4]
    return render(request, 'django_ec/detail.html', {'object':object,'object_list':object_list, 'item_num_sum':item_num_sum})

@basic_auth_required
def adminmenufunc(request):
    menu_list = list(Menu)
    print(menu_list)
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

@basic_auth_required
def adminpurchacelistfunc(request):
    params = {
        "create_date_from" : request.GET.get("create-date-from", None),
        "create_date_to" : request.GET.get("create-date-to", None)
    }
    checkouts = CheckoutModel.objects.prefetch_related('purchase_details')

     # 作成日の範囲でフィルタリング
    if params["create_date_from"]:
        checkouts = checkouts.filter(created_at__gte=params["create_date_from"])
    if params["create_date_to"]:
        checkouts = checkouts.filter(created_at__lte=params["create_date_to"])

    return render(request, 'django_ec/admin/purchace_list.html', {"object_list":checkouts})

@basic_auth_required
def adminpurchacedetailfunc(request, pk):
    # checkout = CheckoutModel.objects.get(pk=pk)
    checkout = CheckoutModel.objects.prefetch_related('purchase_details').get(pk=pk)
    return render(request, 'django_ec/admin/purchace_detail.html', {'checkout':checkout})

def cartdetailfunc(request):
    cart = get_or_create_cart(request)
    item_num_sum = cart.item_num_sum
    item_price_sum = cart.item_price_sum
    return render(request, 'django_ec/cart.html', {'object_list':[item for item in cart.cart_items.all()], 'item_num_sum':item_num_sum, 'item_price_sum':round(item_price_sum)})

def addcartfunc(request,pk):
    # cart = request.session.get('cart_id')
    cart = get_or_create_cart(request)
    item = get_object_or_404(ItemModel,pk=pk)
    cart_item = CartItemModel.objects.get_or_create(cart=cart, item=item)
    if request.method == "POST":
        cart_item[0].quantity += int(request.POST['input_quantity'])
    else:
        cart_item[0].quantity += 1
    cart_item[0].save()

    item_num_sum = cart.item_num_sum
    object_list = ItemModel.objects.all()

    return render(request, 'django_ec/list.html', {'object_list':object_list, 'item_num_sum':item_num_sum})


def removefromcartfunc(request, pk):
    cart = get_or_create_cart(request)
    item = get_object_or_404(ItemModel,pk=pk)
    CartItemModel.objects.get(cart=cart, item=item).delete()
    return redirect('cartdetail')

def checkoutfunc(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_items = cart.cart_items.all()
        # カート内の総額
        total_price=0
        for cart_item in cart_items:
            if cart_item.item.is_sale:
                total_price += cart_item.item.price* 0.6 * cart_item.quantity
            else:
                total_price += cart_item.item.price * cart_item.quantity

        first_name = request.POST.get("firstName", None)
        last_name = request.POST.get("lastName", None)
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        address1 = request.POST.get("address", None)
        address2 = request.POST.get("address2", None)
        country = request.POST.get("country", None)
        state = request.POST.get("state", None)
        zip_code = request.POST.get("zip", None)
        name_card = request.POST.get("nameCard", None)
        credit_number = request.POST.get("creditNum", None)
        expiration = request.POST.get("expiration", None)
        cvv = request.POST.get("cvv", None)
        checkout = CheckoutModel(cart=cart,first_name=first_name,last_name=last_name,user_name = username,email=email,address1=address1,address2=address2,country=country,state=state,zip_code=zip_code,name_on_card=name_card,credit_number=credit_number,credit_expiration=expiration,cvv=cvv, total_price=total_price)
        checkout.save()

        cart_items = cart_items.filter(cart=cart)
        order_infos=""
        for cart_item in cart_items:
            if cart_item.item.is_sale:
                price=cart_item.item.price*0.6
            else:
                price=cart_item.item.price
            PurchaseDetailModel.objects.create(
            checkout=checkout,
            item_name=cart_item.item.name,
            item_price=price,
            quantity=cart_item.quantity,
            is_sale=cart_item.item.is_sale
            )
            order_info=f""" 商品名: {cart_item.item.name}\n 個数: {cart_item.quantity}\n\n"""
            order_infos += order_info

        messages.success(request, '購入ありがとうございます')
        item_num_sum = cart.item_num_sum
        item_price_sum = round(cart.item_price_sum)

        """題名"""
        subject = "【ご購入ありがとうございます】注文確認メール"
        """本文"""
        message = f"""ご注文いただきありがとうございます。\n以下の内容でご注文を承りました。商品の発送準備が整い次第、再度ご連絡いたします。\n\n【ご注文内容】\n{order_infos} 合計金額: ¥{item_price_sum}（税込）\n\n【お届け先情報】\n  お名前: {last_name} {first_name}\n  住所: {country} {address1} {address2}\n  メールアドレス: {email}\n\n【ご注文番号】\n{cart.id}\nこのメールは送信専用です。ご質問やご不明な点がございましたら、当店のカスタマーサポートまでご連絡ください。\n--------------------------\nDjango_EC\nURL: https://example.com\nメール: support@example.com\n電話番号: 03-1234-5678\n--------------------------\n"""

        """送信元メールアドレス"""
        from_email = "kenyanke6111@gmail.com"
        """宛先メールアドレス"""
        recipient_list = [
            email
        ]


        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # カートを削除
        cart.delete()

        item_num_sum=0
        request.session.clear()
        object_list = ItemModel.objects.all()
        return render(request, 'django_ec/list.html', {'object_list':object_list, 'item_num_sum':item_num_sum, 'is_checkouted':True })
    return redirect('list')

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