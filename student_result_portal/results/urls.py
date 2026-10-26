from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.student_create, name="student_create"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),
    path("students/<int:pk>/edit/", views.student_update, name="student_update"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("subjects/", views.subject_list, name="subject_list"),
    path("subjects/add/", views.subject_create, name="subject_create"),
    path("subjects/<int:pk>/delete/", views.subject_delete, name="subject_delete"),
    path("results/add/", views.result_create, name="result_create"),
]
