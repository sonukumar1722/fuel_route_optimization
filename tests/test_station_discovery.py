from django.test import TestCase

from services.station_discovery_service import (
    StationDiscoveryService
)


class TestStationDiscovery(
    TestCase
):

    def test_candidates_are_sorted(self):

        service = (
            StationDiscoveryService()
        )

        candidates = (
            service.get_candidates(
                route_geometry=self.route.geometry,
                route_distance_miles=1000
            )
        )

        positions = [
            c.route_position
            for c in candidates
        ]

        self.assertEqual(
            positions,
            sorted(positions)
        )