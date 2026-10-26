from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/add/", views.employee_create, name="employee_create"),
    path("employees/<int:pk>/", views.employee_detail, name="employee_detail"),
    path("employees/<int:pk>/edit/", views.employee_update, name="employee_update"),
    path("employees/<int:pk>/delete/", views.employee_delete, name="employee_delete"),
    path("salary-slips/", views.slip_list, name="slip_list"),
    path("salary-slips/add/", views.slip_create, name="slip_create"),
    path("salary-slips/<int:pk>/", views.slip_detail, name="slip_detail"),
    path("salary-slips/<int:pk>/delete/", views.slip_delete, name="slip_delete"),
]
