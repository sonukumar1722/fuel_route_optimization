from rest_framework.views import (
    APIView
)

from rest_framework.response import (
    Response
)

from rest_framework import status

from api.serializers import (
    RouteOptimizationSerializer
)

from services.route_service import (
    RouteService
)

from services.station_discovery_service import (
    StationDiscoveryService
)

class RouteOptimizationView(
    APIView
):

    def post(
        self,
        request,
    ):

        serializer = (
            RouteOptimizationSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        start = (
            serializer.validated_data[
                "start"
            ]
        )

        destination = (
            serializer.validated_data[
                "destination"
            ]
        )

        route_service = (
            RouteService()
        )

        route = (
            route_service.get_route(
                start,
                destination,
            )
        )

        discovery_service = (
            StationDiscoveryService()
        )

        stations = (
            discovery_service
            .get_candidates(
                route.geometry,
                route.distance_miles,
            )
        )

        return Response(
            {
                "distance_miles": (
                    route.distance_miles
                ),

                "candidate_stations": [
                    {
                        "station_id": (
                            s.station_id
                        ),

                        "name": s.name,

                        "price": (
                            s.fuel_price
                        ),

                        "route_position": (
                            s.route_position
                        ),
                    }
                    for s in stations
                ],

                "route": (
                    route.geometry
                ),
            },
            status=status.HTTP_200_OK,
        )