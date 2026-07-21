from django.urls import path
from .views import ManagerDashboardView

urlpatterns = [
    path("dashboard/", ManagerDashboardView.as_view(), name="analytics-dashboard"),
]
