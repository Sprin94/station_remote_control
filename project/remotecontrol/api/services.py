from stations.models import Coordinate, Station

import datetime
from django.utils import timezone

from typing import Dict, Union


def execute_derective(
    station: Station,
    axis: str,
    distance: int,
    **kwargs
) -> Coordinate:
    if station and axis and distance:
        if station.status == Station.Status.RUNNING:
            coord = station.coordinates.first()
            current_coord = getattr(coord, axis)
            new_coord = current_coord + distance
            if new_coord <= 0:
                station.broken_data = timezone.now()
                station.status = Station.Status.BROKEN
                station.save()
            setattr(coord, axis, new_coord)
            coord.save()