from rest_framework.serializers import ModelSerializer

from stations.models import Station, Coordinate, Directive
from .services import execute_derective


class StationSerializer(ModelSerializer):
    class Meta:
        model = Station
        fields = ('id', 'name', 'status', 'create_data', 'broken_data')
        read_only_fields = ('status', 'create_data', 'broken_data')

    def create(self, validated_data):
        station = Station.objects.create(**validated_data)
        Coordinate.objects.create(station=station)
        return station


class DirectiveSerializer(ModelSerializer):
    class Meta:
        model = Directive
        fields = ('user', 'station', 'axis', 'distance')
        read_only_fields = ('user', 'station')

    def create(self, validated_data):
        execute_derective(**validated_data)
        return Directive.objects.create(**validated_data)


class CoordinateSerializer(ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ('x', 'y', 'z')
        read_only_fields = ('x', 'y', 'z')
