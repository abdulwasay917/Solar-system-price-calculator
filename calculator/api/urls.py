from django.urls import path

from .views import SolarCalculatorAPIView

urlpatterns = [
    path(
        "calculate/",
        SolarCalculatorAPIView.as_view(),
        name="solar-calculator",
    ),
]