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
