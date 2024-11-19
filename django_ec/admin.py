from django.contrib import admin

from django_ec.models import ItemModel,CartModel,CartItemModel

# Register your models here.
admin.site.register(ItemModel)
admin.site.register(CartModel)
admin.site.register(CartItemModel)