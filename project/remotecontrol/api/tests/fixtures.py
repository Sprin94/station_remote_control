import pytest

from stations.models import Station, Coordinate


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        username='Test',
        password='test'
    )


@pytest.fixture
def api_client_with_credentials(db, user, api_client):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def station(db):
    station = Station.objects.create(name='Sputnik')
    Coordinate.objects.create(station=station)
    return station


@pytest.fixture
def broken_station(db):
    station = Station.objects.create(name='Sputnik', status='broken')
    Coordinate.objects.create(station=station)
    return station
