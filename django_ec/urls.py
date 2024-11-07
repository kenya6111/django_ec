
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from .views import listfunc, detailfunc, adminmenufunc,ItemList,admindeletefunc,ItemCreate,ItemEdit,ItemDelete

urlpatterns = [
    path("", views.index, name="index"),
    path("list", views.listfunc, name="list"),
    path("detail/<int:pk>", views.detailfunc, name="detail"),
    path("admin/menu", views.adminmenufunc, name="menu"),
    path("admin/list", ItemList.as_view(), name="list"),
    path('admin/create', ItemCreate.as_view(), name="create"),
    path("admin/edit/<int:pk>", ItemEdit.as_view(), name="edit"),
    path("admin/delete/<int:pk>", ItemDelete.as_view(), name="delete"),
]
