from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("/", views.random_page, name="random_page"),
    path("/", views.search, name="search"),
]
