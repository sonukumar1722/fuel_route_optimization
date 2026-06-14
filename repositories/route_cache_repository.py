from routing.models import RouteCache


class RouteCacheRepository:

    @staticmethod
    def get_route(
        origin: str,
        destination: str
    ):
        return (
            RouteCache.objects
            .filter(
                origin=origin,
                destination=destination
            )
            .first()
        )

    @staticmethod
    def save_route(
        origin: str,
        destination: str,
        distance_miles: float,
        geometry: dict
    ):
        return RouteCache.objects.create(
            origin=origin,
            destination=destination,
            distance_miles=distance_miles,
            geometry=geometry
        )
