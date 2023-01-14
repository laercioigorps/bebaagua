import pytest
from ..models import Consumo, ConsumoDia, Perfil
from django.urls import reverse
from rest_framework import status
from datetime import datetime, date
from decimal import *


@pytest.mark.django_db
def test_criar_perfil(apiClient):
    data = {"username": "newusername", "nome": "newuser name", "peso": "70"}
    response = apiClient.post(reverse("consumo:criar_perfil"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Perfil.objects.count() == 1
    assert response.data["username"] == "newusername"
    assert response.data["nome"] == "newuser name"
    assert response.data["peso"] == "70.00"
    assert response.data["meta"] == 2450


@pytest.mark.django_db
def test_criar_perfil_duplicado(apiClient):
    Perfil.objects.create(username="newusername", nome="outro", peso=70, meta=3000)
    data = {"username": "newusername", "nome": "newuser name", "peso": "70"}
    response = apiClient.post(reverse("consumo:criar_perfil"), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Perfil.objects.count() == 1


@pytest.mark.django_db
def test_listar_perfis(apiClient):
    data = {"username": "newusername", "nome": "newuser name1", "peso": "71"}
    response = apiClient.post(reverse("consumo:criar_perfil"), data)
    data = {"username": "newusername2", "nome": "newuser name2", "peso": "72"}
    response = apiClient.post(reverse("consumo:criar_perfil"), data)

    response = apiClient.get(reverse("consumo:listar_perfis"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["username"] == "newusername"
    assert response.data[0]["nome"] == "newuser name1"
    assert response.data[0]["peso"] == "71.00"
    assert response.data[0]["meta"] == 2485


@pytest.mark.django_db
def test_update_perfil(apiClient, perfil):
    response = apiClient.put(
        reverse("consumo:detalhe_perfil", kwargs={"username": perfil.username}),
        data={"nome": "novoNome", "peso": "74.22"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nome"] == "novoNome"
    assert response.data["peso"] == "74.22"


@pytest.mark.django_db
def test_update_perfil_sem_atualizar_meta(apiClient, perfil):
    response = apiClient.put(
        reverse("consumo:detalhe_perfil", kwargs={"username": perfil.username}),
        data={"nome": "novoNome", "peso": "74.22", "meta": "3000"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nome"] == "novoNome"
    assert response.data["peso"] == "74.22"
    assert response.data["meta"] == 3000


@pytest.mark.django_db
def test_detalhar_perfil(apiClient, perfil):
    response = apiClient.get(
        reverse("consumo:detalhe_perfil", kwargs={"username": perfil.username})
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == perfil.username
    assert response.data["nome"] == perfil.nome
    assert response.data["peso"] == "70.20"


@pytest.mark.django_db
def test_consumir(apiClient, perfil):
    response = apiClient.post(
        reverse("consumo:consumir", kwargs={"username": perfil.username}),
        {"volume": 250},
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = apiClient.post(
        reverse("consumo:consumir", kwargs={"username": perfil.username}),
        {"volume": 350},
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = apiClient.post(
        reverse("consumo:consumir", kwargs={"username": perfil.username}),
        {"volume": 500},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["volume"] == 500

    consumoDias = ConsumoDia.objects.all().filter(perfil=perfil)
    assert len(consumoDias) == 1
    consumoDia = consumoDias.first()
    assert consumoDia.data == date.today()
    assert consumoDia.consumo == 1100


@pytest.mark.django_db
def test_meta_consumoDia_atingida(apiClient, perfil):
    response = apiClient.post(
        reverse("consumo:consumir", kwargs={"username": perfil.username}),
        {"volume": 250},
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = apiClient.post(
        reverse("consumo:consumir", kwargs={"username": perfil.username}),
        {"volume": 3500},
    )
    assert response.status_code == status.HTTP_201_CREATED

    consumoDia = ConsumoDia.objects.all().filter(perfil=perfil).first()

    assert consumoDia.meta_atingida == True


@pytest.mark.django_db
def test_report_de_consumo_hoje_meta_atingida(apiClient, perfil):
    perfil.meta = 2500
    perfil.save()

    response = apiClient.post(
        reverse("consumo:consumir", kwargs={"username": perfil.username}),
        {"volume": 250},
    )
    response = apiClient.post(
        reverse("consumo:consumir", kwargs={"username": perfil.username}),
        {"volume": 3500},
    )
    perfil.meta = 2512
    perfil.save()

    response = apiClient.get(
        reverse("consumo:resumo", kwargs={"username": perfil.username})
    )
    assert response.status_code == status.HTTP_200_OK

    assert response.data["meta"] == 2500
    assert response.data["consumo"] == 3750
    assert response.data["consumo_restante"] == 0
    assert response.data["porcentagem_consumida_da_meta"] == 100
    assert response.data["meta_atingida"] == True


@pytest.mark.django_db
def test_report_de_consumo_anterior(apiClient, perfil):
    perfil.meta = 2500
    perfil.save()

    consumo_anterior = ConsumoDia.objects.create(
        perfil=perfil,
        data=date(year=2023, month=1, day=1),
        meta_atingida=True,
        consumo=2600,
        meta=2500,
    )

    consumo_anterior = ConsumoDia.objects.create(
        perfil=perfil,
        data=date(year=2023, month=1, day=2),
        meta_atingida=False,
        consumo=2301,
        meta=2500,
    )

    response = apiClient.get(
        reverse(
            "consumo:resumo_data",
            kwargs={
                "username": perfil.username,
                "data": "2023-01-02",
            },
        )
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["meta"] == 2500
    assert response.data["consumo"] == 2301
    assert response.data["consumo_restante"] == 199
    assert response.data["porcentagem_consumida_da_meta"] == 92.04
    assert response.data["meta_atingida"] == False
    assert response.data["data"] == "02/01/2023"


@pytest.mark.django_db
def test_report_de_consumo_anterior_com_data_invalida(apiClient, perfil):
    perfil.meta = 2500
    perfil.save()

    consumo_anterior = ConsumoDia.objects.create(
        perfil=perfil,
        data=date(year=2023, month=1, day=1),
        meta_atingida=True,
        consumo=2600,
    )

    response = apiClient.get(
        reverse(
            "consumo:resumo_data",
            kwargs={
                "username": perfil.username,
                "data": "2023-14-02",
            },
        )
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_historico_de_consumo_de_agua(apiClient, perfil):
    consumoDia1 = ConsumoDia.objects.create(
        perfil=perfil,
        data=date(year=2023, month=1, day=1),
        meta_atingida=True,
        consumo=2600,
        meta=2500,
    )
    consumoDia2 = ConsumoDia.objects.create(
        perfil=perfil,
        data=date(year=2023, month=1, day=2),
        meta_atingida=False,
        consumo=2600,
        meta=2700,
    )
    consumoDia3 = ConsumoDia.objects.create(
        perfil=perfil,
        data=date(year=2023, month=1, day=3),
        meta_atingida=True,
        consumo=2700,
        meta=2700,
    )

    response = apiClient.get(
        reverse(
            "consumo:historico_consumo",
            kwargs={"username": perfil.username},
        )
    )
    data = response.data
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3
    assert response.data[0]["meta"] == 2700
    assert response.data[0]["consumo"] == 2700
    assert response.data[0]["consumo_restante"] == 0
    assert response.data[0]["porcentagem_consumida_da_meta"] == 100
    assert response.data[0]["meta_atingida"] == True
    assert response.data[0]["data"] == "03/01/2023"
