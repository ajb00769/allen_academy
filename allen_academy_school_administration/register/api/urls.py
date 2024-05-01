from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("reg_key/", views.reg_key, name="reg_key"),
]
