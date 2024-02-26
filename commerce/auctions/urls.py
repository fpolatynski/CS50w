from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_id>", views.display_category, name="display_category"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
]
