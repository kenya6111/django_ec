from django.contrib import admin

from django_ec.models import ItemModel,CartModel,CartItemModel,CheckoutModel,PurchaseDetailModel

# Register your models here.
admin.site.register(ItemModel)
admin.site.register(CartModel)
admin.site.register(CartItemModel)
admin.site.register(CheckoutModel)
admin.site.register(PurchaseDetailModel)