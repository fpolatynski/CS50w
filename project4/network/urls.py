
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.add_post, name="new_post"),
    path("posts", views.posts),
    path("like", views.like),
    path("edit", views.edit_post),
    path("<int:user_id>", views.profile_page, name="profile_page"),
]
