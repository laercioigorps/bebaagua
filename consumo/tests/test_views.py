import pytest
from ..models import Consumo, ConsumoDia
from django.urls import reverse
from rest_framework import status
from datetime import datetime, date


@pytest.mark.django_db
def test_consumir(apiClient, usuarioComPerfil):
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"volume":250})
    assert response.status_code == status.HTTP_201_CREATED
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"volume":350})
    assert response.status_code == status.HTTP_201_CREATED
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"volume":500})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["volume"] == 500


    consumoDias = ConsumoDia.objects.all().filter(perfil=usuarioComPerfil.perfil)
    assert len(consumoDias) == 1
    consumoDia = consumoDias.first()
    assert consumoDia.data == date.today()
    assert consumoDia.consumo == 1100

def test_meta_consumoDia_atingida(apiClient, usuarioComPerfil):
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"volume":250})
    assert response.status_code == status.HTTP_201_CREATED
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"volume":3500})
    assert response.status_code == status.HTTP_201_CREATED

    consumoDia = ConsumoDia.objects.all().filter(perfil=usuarioComPerfil.perfil).first()

    assert consumoDia.is_meta_atingida == True
