from django.urls import path
from .import views

app_name = "userac"

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.user_logout, name="user_logout"),
    path("<str:username>", views.user_profile, name="user_profile"),
    path("createPost/", views.createPost, name="createPost"),
    path("like/<int:postid>", views.like_dislike_post, name="like_dislike_post"),
    path("comment/<int:postid>", views.add_comment, name="add_comment"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("following/<str:username>", views.show_following, name="show_following"),
    path("follower/<str:username>", views.show_follower, name="show_follower"),
    path("delete/<int:postid>", views.delete_post, name="delete_post"),
    path("search/", views.find_user, name="searchuser"),
]