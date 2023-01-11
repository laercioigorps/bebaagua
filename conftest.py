import pytest

from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth import get_user_model
from perfil.models import Perfil, User
from recomendacao.models import GuiaDeHidratacaoPessoal


@pytest.fixture
def apirf():
    return APIRequestFactory()


@pytest.fixture
def apiClient():
    return APIClient()

@pytest.fixture
def usuarioComPerfil(db):
    perfil = Perfil.objects.create(peso=70.20)
    perfil.guia = GuiaDeHidratacaoPessoal.objects.create()
    recomendacao = perfil.guia.calcular_recomendacao(perfil)
    perfil.guia.recomendacao = recomendacao
    perfil.guia.meta = recomendacao
    perfil.save()
    user = get_user_model().objects.create(username="random", perfil=perfil)
    return user
