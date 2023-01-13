import pytest

from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from consumo.models import Perfil, User

@pytest.fixture
def apirf():
    return APIRequestFactory()


@pytest.fixture
def apiClient():
    return APIClient()

@pytest.fixture
def usuarioComPerfil(db):
    perfil = Perfil.objects.create(peso=70.20, meta=70.2 * 35)
    perfil.save()
    user = get_user_model().objects.create(username="random", perfil=perfil)
    return user
