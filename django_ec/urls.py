
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from .views import listfunc


urlpatterns = [
    path("", views.index, name="index"),
    path("list", views.listfunc, name="list"),
]
