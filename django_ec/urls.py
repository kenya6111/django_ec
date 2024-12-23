
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from . import views

from .views import listfunc, detailfunc, adminmenufunc,ItemList,ItemCreate,ItemEdit,ItemDelete,cartdetailfunc,addcartfunc,removefromcartfunc,checkoutfunc,adminpurchacelistfunc,updatecartfunc


urlpatterns = [
    path("", views.index, name="index"),
    path("list", views.listfunc, name="list"),
    path("detail/<int:pk>", views.detailfunc, name="detail"),
    path("admin/menu", views.adminmenufunc, name="menu"),
    path("admin/list", ItemList.as_view(), name="admin_list"),
    path('admin/create', ItemCreate.as_view(), name="create"),
    path("admin/edit/<int:pk>", ItemEdit.as_view(), name="edit"),
    path("admin/delete/<int:pk>", ItemDelete.as_view(), name="delete"),
    path("admin/purchace_list", views.adminpurchacelistfunc, name="admin_purchace_list"),
    path("admin/purchace_detail/<int:pk>", views.adminpurchacedetailfunc, name="admin_purchace_detail"),
    path("cartdetail/", views.cartdetailfunc, name="cartdetail"),
    path("addtocart/<int:pk>", views.addcartfunc, name="addtocart"),
    path("updatecart/", views.updatecartfunc, name="updatecart"),
    path("checkRedeem/", views.checkredeemfunc, name="checkRedeem"),
    path("removefromcart/", views.removefromcartfunc, name="removefromcart"),
    path("checkout", views.checkoutfunc, name="checkout"),
]
