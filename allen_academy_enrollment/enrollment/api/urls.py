from django.urls import path
from . import views

urlpatterns = [
    path("get_dept_list/", views.get_dept_list, name="dept_list"),
    path("get_course_list/", views.get_course_list, name="course_list"),
    path("get_subject_list/", views.get_subject_list, name="subject_list"),
    path(
        "get_subject_schedule_list/",
        views.get_subject_schedule_list,
        name="subject_sched",
    ),
    path("enroll_course/", views.enroll_course, name="enroll_course"),
    path(
        "enroll_subject_schedule/",
        views.enroll_subject_schedule,
        name="enroll_subject_schedule",
    ),
    path("get_user_schedule/", views.get_user_schedule, name="user_schedule"),
    path("get_course/", views.get_course, name="get_course"),
    path("get_subject_block_list/", views.get_subject_block, name="subject_block_list"),
    path(
        "get_block_schedule_list/", views.get_block_schedule, name="block_schedule_list"
    ),
]
