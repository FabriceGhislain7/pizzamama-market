from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def radice_api(richiesta):  # best practice comune: parametro chiamato "request"
    return Response({
        "nome": "API PizzaMama Market",
        "versione": "v1",
        "stato": "attiva",
    })


urlpatterns = [
    path("", radice_api, name="radice-api"),
]
