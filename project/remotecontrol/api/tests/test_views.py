import pytest

from django.urls import reverse

from stations.models import Station, Coordinate
from .fixtures import (api_client, api_client_with_credentials, user, station,
                       broken_station,)


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('api:station-list')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authorized_request(api_client_with_credentials):
    url = reverse('api:station-list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_station(api_client_with_credentials):
    url = reverse('api:station-list')
    response = api_client_with_credentials.post(url, data={'name': 'Test'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_station_breakdown(api_client_with_credentials, station):
    assert station.status != Station.Status.BROKEN
    url = reverse('api:station-state', kwargs={'pk': station.id})
    api_client_with_credentials.post(url, data={
        'axis': 'x',
        'distance': -1000
        })
    station = Station.objects.get(id=station.id)
    assert station.status == Station.Status.BROKEN, (
        'Станция с координатами <= 0 не сломалась')


@pytest.mark.django_db
def test_station_move(api_client_with_credentials, station):
    url = reverse('api:station-state', kwargs={'pk': station.id})
    x_before = station.coordinates.first().x
    api_client_with_credentials.post(url, data={
        'axis': 'x',
        'distance': 100
        })
    x_after = Coordinate.objects.get(station=station).x
    assert x_before + 100 == x_after, 'Испавная станция не двигается'


@pytest.mark.django_db
def test_broken_stationd_dont_move(
    api_client_with_credentials,
    broken_station):
    assert broken_station.status == Station.Status.BROKEN
    url = reverse('api:station-state', kwargs={'pk': broken_station.id})
    x_before = broken_station.coordinates.first().x
    api_client_with_credentials.post(url, data={
        'axis': 'x',
        'distance': -1000
        })
    x_after = Coordinate.objects.get(station=broken_station).x
    assert x_before == x_after, 'Сломанная станция не должна двигаться'


@pytest.mark.django_db
def test_try_change_status(api_client_with_credentials, station):
    url = reverse('api:station-detail', kwargs={'pk': station.id})
    status_before = station.status
    response = api_client_with_credentials.put(url, data={
        'status': 'broken'
        })
    status_after = Station.objects.get(pk=station.id).status
    assert status_before == status_after


@pytest.mark.django_db
def test_axis_xyz(api_client_with_credentials, station):
    for axis in ('x', 'y', 'z'):
        url = reverse('api:station-state', kwargs={'pk': station.id})
        response = api_client_with_credentials.post(url, data={
            'axis': axis,
            'distance': 1000
        })
        assert response.status_code == 201, 'Параметр axis должен быть x, y, z'


@pytest.mark.django_db
def test_axis_xyz(api_client_with_credentials, station):
    for axis in ('f', 'a', 'h'):
        url = reverse('api:station-state', kwargs={'pk': station.id})
        response = api_client_with_credentials.post(url, data={
            'axis': axis,
            'distance': 1000
        })
        assert response.status_code == 400, ('Параметр axis  может быть '
                                             'только x, y, z')


@pytest.mark.django_db
def test_update_broken_time(api_client_with_credentials, station):
    broken_data_before = station.broken_data
    url = reverse('api:station-state', kwargs={'pk': station.id})
    api_client_with_credentials.post(url, data={
        'axis': 'x',
        'distance': -1000
        })
    station = Station.objects.get(id=station.id)
    assert station.broken_data is not None, (
        'При поломки станции не установилась дата поломки')
