
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from .views import listfunc, detailfunc, adminmenufunc,adminlistfunc,admincreatefunc,admineditfunc,admindeletefunc

urlpatterns = [
    path("", views.index, name="index"),
    path("list", views.listfunc, name="list"),
    path("detail/<int:pk>", views.detailfunc, name="detail"),
    path("admin/menu", views.adminmenufunc, name="admin_menu"),
    path("admin/list", views.adminlistfunc, name="admin_list"),
    path("admin/create", views.admincreatefunc, name="admin_create"),
    path("admin/edit", views.admineditfunc, name="admin_edit"),
    path("admin/delete", views.admindeletefunc, name="admin_delete"),
]
