import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from decimal import *


@pytest.mark.django_db
def test_criar_perfil(apiClient):
    data = {"username": "newusername", "nome": "newuser name", "peso": "70"}
    response = apiClient.post(reverse("perfil:criar_perfil"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.count() == 1
    assert response.data["username"] == "newusername"
    assert response.data["nome"] == "newuser name"
    assert response.data["perfil"]["peso"] == "70.00"


@pytest.mark.django_db
def test_listar_perfis(apiClient):
    data = {"username": "newusername", "nome": "newuser name1", "peso": "71"}
    response = apiClient.post(reverse("perfil:criar_perfil"), data)
    data = {"username": "newusername2", "nome": "newuser name2", "peso": "72"}
    response = apiClient.post(reverse("perfil:criar_perfil"), data)

    response = apiClient.get(reverse("perfil:listar_perfis"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["username"] == "newusername"
    assert response.data[0]["nome"] == "newuser name1"
    assert response.data[0]["perfil"]["peso"] == "71.00"


@pytest.mark.django_db
def test_update_perfil(apiClient, usuarioComPerfil):
    response = apiClient.put(
        reverse(
            "perfil:detalhe_perfil", 
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
        reverse("perfil:detalhe_perfil", kwargs={"username": usuarioComPerfil.username})
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == usuarioComPerfil.username
    assert response.data["nome"] == usuarioComPerfil.nome
    assert float(response.data["perfil"]["peso"]) == float(usuarioComPerfil.perfil.peso)


@pytest.mark.django_db
def test_criar_perfil_gera_recomendacao_de_consumo_e_meta(apiClient):
    data = {"username": "newusername", "nome": "newuser name", "peso": "70"}
    response = apiClient.post(reverse("perfil:criar_perfil"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.count() == 1
    
    usuario = get_user_model().objects.get(username="newusername")
    assert usuario.perfil.guia.recomendacao == 70*35
    assert usuario.perfil.guia.meta == 70*35