import pytest
from ..models import Consumo, ConsumoDia
from django.urls import reverse
from rest_framework import status
from datetime import datetime, date
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_criar_perfil(apiClient):
    data = {"username": "newusername", "nome": "newuser name", "peso": "70"}
    response = apiClient.post(reverse("consumo:criar_perfil"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.count() == 1
    assert response.data["username"] == "newusername"
    assert response.data["nome"] == "newuser name"
    assert response.data["perfil"]["peso"] == "70.00"


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
    assert response.data[0]["perfil"]["peso"] == "71.00"


@pytest.mark.django_db
def test_update_perfil(apiClient, usuarioComPerfil):
    response = apiClient.put(
        reverse(
            "consumo:detalhe_perfil", 
            kwargs={"username": usuarioComPerfil.username}
        ),
        data={
            "nome": "novoNome",
            "peso" : "74.22"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nome"] == "novoNome"
    assert response.data["perfil"]["peso"] == "74.22"

@pytest.mark.django_db
def test_detalhar_perfil(apiClient, usuarioComPerfil):
    response = apiClient.get(
        reverse("consumo:detalhe_perfil", kwargs={"username": usuarioComPerfil.username})
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == usuarioComPerfil.username
    assert response.data["nome"] == usuarioComPerfil.nome
    assert float(response.data["perfil"]["peso"]) == float(usuarioComPerfil.perfil.peso)

@pytest.mark.django_db
def test_criar_perfil_gera_recomendacao_de_consumo_e_meta(apiClient):
    data = {"username": "newusername", "nome": "newuser name", "peso": "70"}
    response = apiClient.post(reverse("consumo:criar_perfil"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.count() == 1
    
    usuario = get_user_model().objects.get(username="newusername")
    assert usuario.perfil.meta == 2450

@pytest.mark.django_db
def test_atualizar_perfil_atualiza_recomendacao_de_consumo(apiClient):
    data = {"username": "newusername", "nome": "newuser name", "peso": "70"}
    response = apiClient.post(reverse("consumo:criar_perfil"), data)

    response = apiClient.put(
        reverse(
            "consumo:detalhe_perfil", 
            kwargs={"username": "newusername"}
        ),
        data={
            "nome": "NomeAtualizado",
            "peso" : "100"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    usuario = get_user_model().objects.get(username="newusername")
    assert usuario.perfil.meta == 3500

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
