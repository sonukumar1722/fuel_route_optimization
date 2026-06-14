from repositories.route_cache_repository import (
    RouteCacheRepository,
)

from services.providers.openroute_service import (
    OpenRouteServiceProvider,
)

from domain.dto import RouteData


class RouteService:

    def __init__(self):

        self.provider = (
            OpenRouteServiceProvider()
        )

    def get_route(
        self,
        origin: str,
        destination: str,
    ) -> RouteData:

        cached_route = (
            RouteCacheRepository
            .get_route(
                origin,
                destination,
            )
        )

        if cached_route:

            return RouteData(
                distance_miles=(
                    cached_route.distance_miles
                ),
                geometry=(
                    cached_route.geometry
                ),
            )

        origin_lat, origin_lon = (
            self.provider.geocode(
                origin
            )
        )

        dest_lat, dest_lon = (
            self.provider.geocode(
                destination
            )
        )

        route = (
            self.provider.get_route(
                [origin_lon, origin_lat],
                [dest_lon, dest_lat],
            )
        )

        RouteCacheRepository.save_route(
            origin=origin,
            destination=destination,
            distance_miles=(
                route.distance_miles
            ),
            geometry=route.geometry,
        )

        return route