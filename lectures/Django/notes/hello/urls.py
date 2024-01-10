from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:names>", views.greet, name="greet"),
    path("filip", views.filip, name="filip"),
]