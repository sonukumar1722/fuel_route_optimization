class FuelOptimizerException(Exception):
    """
    Base exception for optimizer-related errors.
    """
    pass


class RouteNotReachableError(FuelOptimizerException):
    """
    Raised when destination cannot be reached
    with available stations and vehicle range.
    """
    pass


class RouteProviderError(Exception):
    """
    Raised when routing provider fails.
    """
    pass


class GeocodingError(Exception):
    """
    Raised when geocoding provider
    cannot resolve an address.
    """
    pass


class NoStationsFoundError(FuelOptimizerException):
    """
    Raised when no stations are found
    near the route corridor.
    """
    pass


class InvalidRouteError(FuelOptimizerException):
    """
    Raised when route geometry
    is malformed or empty.
    """
    pass