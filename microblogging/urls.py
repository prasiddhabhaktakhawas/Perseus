from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("likeUnlike/<int:postid>", views.likeUnlike, name="likeUnlike"),
    path("edit/<int:postid>", views.editPost, name="edit"),
    path("user/<str:userName>", views.profilePage, name="profilepage"),
    path("user/toggleFollow/<str:userName>", views.toggleFollow, name="toggleFollow"),
    path("deletepost/<int:postid>", views.removepost, name="deletepost")
]
