from django.contrib.gis.measure import D

from fuel.models import FuelStation


class FuelStationRepository:

    @staticmethod
    def find_near_route(
        route_geometry,
        corridor_miles: int = 20
    ):
        """
        Returns stations within X miles
        of the route geometry.
        """

        return (
            FuelStation.objects
            .filter(
                location__distance_lte=(
                    route_geometry,
                    D(mi=corridor_miles)
                )
            )
        )