from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("get_user_details/", views.get_user_details, name="get_user_details"),
]
