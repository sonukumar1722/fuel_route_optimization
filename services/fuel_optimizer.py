from domain.dto import (
    CandidateStation,
    FuelStop,
    OptimizationResult,
    VehicleConfig,
)

from utils.exceptions import (
    RouteNotReachableError,
)


class FuelOptimizer:

    def optimize(
        self,
        route_distance: float,
        stations: list[CandidateStation],
        vehicle: VehicleConfig,
    ) -> OptimizationResult:

        stations = sorted(
            stations,
            key=lambda s: s.route_position
        )

        current_position = 0.0

        remaining_range = (
            vehicle.max_range
        )

        total_cost = 0.0

        fuel_stops = []

        while current_position < route_distance:

            reachable = (
                self._get_reachable_stations(
                    current_position,
                    vehicle.max_range,
                    stations,
                )
            )

            if not reachable:

                if (
                    route_distance
                    - current_position
                    <= remaining_range
                ):
                    break

                raise RouteNotReachableError(
                    "No reachable station found."
                )

            best_station = (
                self._find_best_station(
                    reachable
                )
            )

            distance_to_station = (
                best_station.route_position
                - current_position
            )

            if (
                distance_to_station
                > remaining_range
            ):

                fuel_needed = (
                    distance_to_station
                    - remaining_range
                )

                gallons = (
                    fuel_needed
                    / vehicle.mpg
                )

                cost = (
                    gallons
                    * best_station.fuel_price
                )

                fuel_stops.append(
                    FuelStop(
                        station_id=(
                            best_station.station_id
                        ),
                        station_name=(
                            best_station.name
                        ),
                        route_position=(
                            best_station.route_position
                        ),
                        gallons_purchased=(
                            round(
                                gallons,
                                2
                            )
                        ),
                        fuel_price=(
                            best_station.fuel_price
                        ),
                        cost=(
                            round(
                                cost,
                                2
                            )
                        ),
                        latitude=(
                            best_station.latitude
                        ),
                        longitude=(
                            best_station.longitude
                        ),
                    )
                )

                total_cost += cost

                remaining_range += (
                    fuel_needed
                )

            travelled = (
                distance_to_station
            )

            remaining_range -= travelled

            current_position = (
                best_station.route_position
            )

            cheaper_station = (
                self._find_cheaper_station_ahead(
                    current_station=best_station,
                    stations=stations,
                    vehicle=vehicle,
                )
            )

            if cheaper_station:

                continue

            refill_range = (
                vehicle.max_range
                - remaining_range
            )

            if refill_range > 0:

                gallons = (
                    refill_range
                    / vehicle.mpg
                )

                cost = (
                    gallons
                    * best_station.fuel_price
                )

                fuel_stops.append(
                    FuelStop(
                        station_id=(
                            best_station.station_id
                        ),
                        station_name=(
                            best_station.name
                        ),
                        route_position=(
                            best_station.route_position
                        ),
                        gallons_purchased=(
                            round(
                                gallons,
                                2
                            )
                        ),
                        fuel_price=(
                            best_station.fuel_price
                        ),
                        cost=(
                            round(
                                cost,
                                2
                            )
                        ),
                        latitude=(
                            best_station.latitude
                        ),
                        longitude=(
                            best_station.longitude
                        ),
                    )
                )

                total_cost += cost

                remaining_range = (
                    vehicle.max_range
                )

        total_gallons = sum(
            stop.gallons_purchased
            for stop in fuel_stops
        )

        return OptimizationResult(
            total_cost=round(
                total_cost,
                2
            ),
            total_gallons=round(
                total_gallons,
                2
            ),
            fuel_stops=fuel_stops,
        )

    def _get_reachable_stations(
        self,
        current_position,
        max_range,
        stations,
    ):

        max_position = (
            current_position
            + max_range
        )

        return [
            station
            for station in stations
            if (
                current_position
                < station.route_position
                <= max_position
            )
        ]

    def _find_best_station(
        self,
        stations,
    ):

        return min(
            stations,
            key=lambda s: s.fuel_price,
        )

    def _find_cheaper_station_ahead(
        self,
        current_station,
        stations,
        vehicle,
    ):

        max_reachable = (
            current_station.route_position
            + vehicle.max_range
        )

        for station in stations:

            if (
                station.route_position
                <= current_station.route_position
            ):
                continue

            if (
                station.route_position
                > max_reachable
            ):
                break

            if (
                station.fuel_price
                < current_station.fuel_price
            ):
                return station

        return None