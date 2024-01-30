from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("<str:entries>", views.entry_page, name="entry_page"),
    path("<str:entries>/edit", views.edit, name="edit")
]
