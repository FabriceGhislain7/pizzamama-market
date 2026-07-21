from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet, RegisterView, LogoutView, export_my_data

router = DefaultRouter()
router.register(r"addresses", AddressViewSet, basename="addresses")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/export/", export_my_data, name="export-my-data"),
]

urlpatterns += router.urls
