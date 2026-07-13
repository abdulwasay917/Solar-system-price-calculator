from django.urls import path,include

from calculator import api

urlpatterns = [

    path("api", include("api.urls", namespace="api")),
]