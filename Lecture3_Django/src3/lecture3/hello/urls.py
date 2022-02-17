from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet"),
    path("xana", views.xana, name="xana"),
    path("facu", views.facu, name="facu"),
]