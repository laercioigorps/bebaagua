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

@pytest.mark.django_db
def test_meta_consumoDia_atingida(apiClient, usuarioComPerfil):
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"volume":250})
    assert response.status_code == status.HTTP_201_CREATED
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"volume":3500})
    assert response.status_code == status.HTTP_201_CREATED

    consumoDia = ConsumoDia.objects.all().filter(perfil=usuarioComPerfil.perfil).first()

    assert consumoDia.is_meta_atingida == True

@pytest.mark.django_db
def test_report_de_consumo_hoje_meta_atingida(apiClient, usuarioComPerfil):
    usuarioComPerfil.perfil.meta = 2500
    usuarioComPerfil.perfil.save()

    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"volume":250})
    response = apiClient.post(reverse("consumo:consumir_copo",kwargs={"username": usuarioComPerfil.username}),{"volume":3500})

    response = apiClient.get(reverse("consumo:resumo",kwargs={"username": usuarioComPerfil.username}))
    assert response.status_code == status.HTTP_200_OK

    assert response.data["meta"] == 2500
    assert response.data["consumo"] == 3750
    assert response.data["consumo_restante"] == 0
    assert response.data["porcentagem_consumida_da_meta"] == 100
    assert response.data["meta_atingida"] == True

@pytest.mark.django_db
def test_report_de_consumo_anterior(apiClient, usuarioComPerfil):
    usuarioComPerfil.perfil.meta = 2500
    usuarioComPerfil.perfil.save()

    consumo_anterior = ConsumoDia.objects.create(
        perfil= usuarioComPerfil.perfil, 
        data=date(year=2023, month=1, day=1),
        is_meta_atingida= True,
        consumo=2600
    )

    consumo_anterior = ConsumoDia.objects.create(
        perfil= usuarioComPerfil.perfil, 
        data=date(year=2023, month=1, day=2),
        is_meta_atingida= False,
        consumo=2301
    )

    response = apiClient.get(reverse(
        "consumo:resumo_data",
        kwargs={
            "username": usuarioComPerfil.username,
            "data" : "2023-01-02",
        }
    ))
    assert response.status_code == status.HTTP_200_OK

    assert response.data["meta"] == 2500
    assert response.data["consumo"] == 2301
    assert response.data["consumo_restante"] == 199
    assert response.data["porcentagem_consumida_da_meta"] == 92.04
    assert response.data["meta_atingida"] == False
