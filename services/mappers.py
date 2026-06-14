from domain.dto import CandidateStation


def to_candidate_station(
    station,
    route_position
):

    return CandidateStation(
        station_id=station.id,
        name=station.name,
        route_position=route_position,
        fuel_price=float(
            station.fuel_price
        ),
        latitude=station.location.y,
        longitude=station.location.x,
    )