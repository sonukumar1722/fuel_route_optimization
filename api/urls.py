from django.urls import path

from api.views import (
    RouteOptimizationView
)

urlpatterns = [
    path(
        "routes/optimize/",
        RouteOptimizationView.as_view(),
        name="route-optimize",
    ),
]