from urllib import response

import requests

from django.conf import settings

from domain.dto import RouteData

from utils.exceptions import (
    GeocodingError,
    RouteProviderError,
)


class OpenRouteServiceProvider:

    BASE_URL = "https://api.openrouteservice.org"

    def __init__(self):

        self.headers = {
            "Authorization": settings.ORS_API_KEY,
            "Content-Type": "application/json",
        }

    def geocode(
        self,
        address: str
    ) -> tuple[float, float]:

        url = (
            f"{self.BASE_URL}"
            "/geocode/search"
        )

        params = {
            "api_key": settings.ORS_API_KEY,
            "text": address,
            "size": 1,
        }

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        if response.status_code != 200:

            print(
                "STATUS:",
                response.status_code
            )

            print(
                "BODY:",
                response.text
            )

            raise GeocodingError(
                f"Failed to geocode {address}"
            )

        data = response.json()

        features = data.get(
            "features",
            []
        )

        if not features:
            return None

        longitude, latitude = (
            features[0]["geometry"]
            ["coordinates"]
        )

        return latitude, longitude

    def get_route(
        self,
        start_coordinates,
        end_coordinates,
    ) -> RouteData:

        url = (
            f"{self.BASE_URL}"
            "/v2/directions/driving-car/geojson"
        )

        payload = {
            "coordinates": [
                start_coordinates,
                end_coordinates,
            ]
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=60,
        )

        if response.status_code != 200:

            raise RouteProviderError(
                "Route generation failed"
            )

        data = response.json()

        feature = data["features"][0]

        distance_meters = (
            feature["properties"]
            ["summary"]
            ["distance"]
        )

        distance_miles = (
            distance_meters
            / 1609.34
        )

        geometry = feature[
            "geometry"
        ]

        return RouteData(
            distance_miles=distance_miles,
            geometry=geometry,
        )