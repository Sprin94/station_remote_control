from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StationViewSet

router = DefaultRouter()

router.register('', StationViewSet)

app_name = 'api'

urlpatterns = [
    path('stations/', include(router.urls))
]
