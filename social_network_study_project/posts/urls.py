from django.urls import path
from . import views
#что такое точка?

urlpatterns = [
    path("", views.index, name="index"),
    #главная страница - вью "индекс"
    path("group/<str:slug>", views.group_posts, name="group_posts"),
    path("new/", views.new_post, name = "new")
]