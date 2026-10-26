from django.urls import path

from . import views

app_name = "atm"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("menu/", views.menu_view, name="menu"),
    path("balance/", views.balance_view, name="balance"),
    path("withdraw/", views.withdraw_view, name="withdraw"),
    path("deposit/", views.deposit_view, name="deposit"),
    path("statement/", views.statement_view, name="statement"),
]
