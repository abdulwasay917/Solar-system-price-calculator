from django.urls import path, include
from .views import home

urlpatterns = [
    path("",home,name="calculator-home"),
    path("api/",include("calculator.api.urls")),
]
