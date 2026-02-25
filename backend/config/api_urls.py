"""
Central API routing for version v1.
Keeps routing modular and scalable.
"""

from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


# -------------------------------------------------------------------
# API Root
# -------------------------------------------------------------------

@api_view(["GET"])
def radice_api(request):
    return Response({
        "nome": "API PizzaMama Market",
        "versione": "v1",
        "stato": "attiva",
    })


urlpatterns = [
    path("", radice_api, name="radice-api"),

    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    path("accounts/", include("apps.accounts.api.urls")),
    path("products/", include("apps.products.api.urls")),
    path("orders/", include("apps.orders.api.urls")),
]