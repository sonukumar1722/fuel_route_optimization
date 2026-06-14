from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class CandidateStation:
    """
    Station projected onto the route.
    Used by optimizer.
    """

    station_id: int
    name: str

    route_position: float
    fuel_price: float

    latitude: float
    longitude: float


@dataclass(slots=True)
class VehicleConfig:
    """
    Vehicle assumptions from assignment.
    """

    max_range: float = 500.0
    mpg: float = 10.0


@dataclass(slots=True)
class VehicleState:
    """
    Runtime state used during optimization.
    """

    current_position: float
    remaining_range: float


@dataclass(slots=True)
class FuelStop:
    """
    One selected fuel stop.
    """

    station_id: int
    station_name: str

    route_position: float

    gallons_purchased: float

    fuel_price: float

    cost: float

    latitude: float
    longitude: float


@dataclass(slots=True)
class OptimizationResult:
    """
    Final optimizer output.
    """

    total_cost: float

    total_gallons: float

    fuel_stops: List[FuelStop]


@dataclass(slots=True)
class RouteData:
    """
    Route returned by routing provider.
    """

    distance_miles: float

    geometry: dict