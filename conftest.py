import pytest

from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from consumo.models import Perfil


@pytest.fixture
def apirf():
    return APIRequestFactory()


@pytest.fixture
def apiClient():
    return APIClient()


@pytest.fixture
def perfil(db):
    perfil = Perfil.objects.create(
        username="newUser", nome="newUser nome", peso=70.20, meta=70.2 * 35
    )
    return perfil
