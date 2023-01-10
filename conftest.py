import pytest

from rest_framework.test import APIRequestFactory, APIClient

@pytest.fixture
def apirf():
    return APIRequestFactory()

@pytest.fixture
def apiClient():
    return APIClient()