from django.urls import path
import App1.views as v
urlpatterns = [
    path("",v.Home,name="index")
]
