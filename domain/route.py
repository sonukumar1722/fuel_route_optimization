from dataclasses import dataclass


@dataclass
class RouteData:
    distance_miles: float
    geometry: dict