from django.contrib.gis.geos import LineString


def route_to_linestring(route_geometry):

    coordinates = route_geometry["coordinates"]

    return LineString( coordinates, srid=4326 )

def create_route_buffer(route_line, miles=20 ):
    buffer_distance_meters = (miles * 1609.34)
    return route_line.buffer(buffer_distance_meters)

def build_route_linestring(route_geometry: dict) -> LineString:

    coordinates = route_geometry["coordinates"]

    return LineString(coordinates,srid=4326)

def calculate_route_position(
    point,
    route_line,
    route_distance_miles
):
    """
    Converts station location into
    mile marker along route.
    """

    fraction = (
        route_line.project(point)
        / route_line.length
    )

    return (
        fraction
        * route_distance_miles
    )