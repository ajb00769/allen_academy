from django.urls import path
from . import views

urlpatterns = [
    path("create_dept", views.create_department, name="create_dept"),
    path("create_course", views.create_course, name="create_course"),
    path("create_subject", views.create_subject, name="create_subject"),
    path("create_schedule", views.create_schedule, name="create_schedule"),
    path("update_salary", views.update_salary, name="update_salary"),
]
