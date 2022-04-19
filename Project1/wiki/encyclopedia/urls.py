from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry_title>", views.entry_page, name="entry title"),
    path("random-page/", views.random_page, name="random page"),
    path("search/", views.search, name="search"),
    
    path("new-page/", views.new_page, name="new page"),
    path("edit-page/",views.edit_page, name='edit_page'),
    path("save/", views.save_page, name="save_page"),
    path("save-edit/",views.save_page_edit, name='save_edit')
]
