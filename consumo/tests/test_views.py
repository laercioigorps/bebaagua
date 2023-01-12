import pytest
from ..models import Copo, Consumo, ConsumoDia
from django.urls import reverse
from rest_framework import status
from datetime import datetime, date

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


@pytest.mark.django_db
def test_consumir_copos(apiClient, usuarioComPerfil):
    copo1 = Copo.objects.create(nome="Pequeno", volume=250)
    copo2 = Copo.objects.create(nome="Médio", volume=350)
    copo3 = Copo.objects.create(nome="Grande", volume=500)
    assert Copo.objects.count() == 3

    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"copo":copo1.id})
    assert response.status_code == status.HTTP_201_CREATED
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"copo":copo2.id})
    assert response.status_code == status.HTTP_201_CREATED
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"copo":copo3.id})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["volume"] == 500


    consumoDia = ConsumoDia.objects.all().filter(perfil=usuarioComPerfil.perfil)
    assert len(consumoDia) == 1
    consumo = consumoDia.first()
    assert consumo.data == date.today()

