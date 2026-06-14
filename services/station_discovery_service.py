from repositories.fuel_station_repository import (
    FuelStationRepository
)

from services.mappers import (
    to_candidate_station
)

from utils.geo import (
    build_route_linestring,
    calculate_route_position
)


class StationDiscoveryService:

    DEFAULT_CORRIDOR_MILES = 20

    def get_candidates(
        self,
        route_geometry: dict,
        route_distance_miles: float,
    ):

        route_line = build_route_linestring(
            route_geometry
        )

        stations = (
            FuelStationRepository.find_near_route(
                route_line,
                corridor_miles=self.DEFAULT_CORRIDOR_MILES
            )
        )

        candidates = []

        for station in stations:

            route_position = (
                calculate_route_position(
                    point=station.location,
                    route_line=route_line,
                    route_distance_miles=route_distance_miles
                )
            )

            candidate = (
                to_candidate_station(
                    station,
                    route_position
                )
            )

            candidates.append(candidate)

        candidates.sort(
            key=lambda x: x.route_position
        )

        return candidates