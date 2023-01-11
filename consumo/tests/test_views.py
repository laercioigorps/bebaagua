import pytest
from ..models import Copo
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_listar_opcoes_de_copos(apiClient):
    copo1 = Copo.objects.create(nome="Pequeno", volume=250)
    copo2 = Copo.objects.create(nome="Médio", volume=350)
    copo3 = Copo.objects.create(nome="Grande", volume=500)

    assert Copo.objects.count() == 3

    response = apiClient.get(reverse("consumo:listar_copos"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
    assert response.data[0]["nome"] == "Pequeno"
    assert response.data[1]["nome"] == "Médio"
    assert response.data[2]["nome"] == "Grande"


