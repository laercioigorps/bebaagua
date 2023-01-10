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
