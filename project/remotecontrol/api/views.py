from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import (StationSerializer, CoordinateSerializer,
                          DirectiveSerializer)
from stations.models import Station, Directive, Coordinate


@extend_schema_view(
    list=extend_schema(description='Список всех станций'),
    retrieve=extend_schema(description='Все атрибуты конкретной станции'),
    destroy=extend_schema(description='Удаление станции'),
    create=extend_schema(description='Создание станции'),
    update=extend_schema(description='Обновление всех полей станции'),
    partial_update=extend_schema(description='Изменение отдельных полей')
)
class StationViewSet(ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def get_serializer_class(self):
        if self.action == 'state' and self.request.method == 'GET':
            return CoordinateSerializer
        if self.action == 'state' and self.request.method == 'POST':
            return DirectiveSerializer
        return StationSerializer

    @extend_schema(responses=CoordinateSerializer, request=DirectiveSerializer,
                   description=('Отправка указания и получения '
                                'актуальных координат.'))
    @action(
        methods=['GET', 'POST'],
        detail=True,
        url_path='state'
    )
    def state(self, request, pk):
        if request.method == 'GET':
            coord = get_object_or_404(Coordinate, station_id=pk)
            serializer = self.get_serializer(
                coord,
                context={'user': self.request.user}
            )
            return Response(serializer.data)
        if request.method == 'POST':
            station = Station.objects.get(pk=pk)
            serializer = self.get_serializer(
                data=request.data,
                context={
                    'user': self.request.user,
                    'station': station,
                }
                )
            if serializer.is_valid():
                self.perform_create(serializer)
                coord = get_object_or_404(Coordinate, station_id=pk)
                serializer = CoordinateSerializer(coord)
                serializer.context['station_id'] = pk
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
