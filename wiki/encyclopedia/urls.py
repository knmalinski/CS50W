from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>",views.entry, name="entry"),
    path("error", views.error, name="error"),
    path("search", views.search, name="search"),
    path("new_page",views.new_page, name="new_page"),
    path("edit_page",views.edit_page, name="edit_page"),
    path("save_page",views.save_page, name="save_page"),
    path("rand",views.rand, name="rand"),
    ]


