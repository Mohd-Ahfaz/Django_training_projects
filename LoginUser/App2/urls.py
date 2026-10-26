from django.urls import path
import App2.views as v
urlpatterns = [
    path("signup/",v.Signup,name="Signup"),
    path("Login/",v.Emplogin,name="Login"),
    path("Empdashboard/",v.Gotoempdashboard,name="Empd"),
    path("Logout/",v.LLogout,name="Logout")
] 