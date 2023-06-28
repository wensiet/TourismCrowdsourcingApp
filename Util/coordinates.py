import math
from google.cloud.firestore_v1._helpers import GeoPoint as GP


def calculate_boundaries(latitude, longitude, distance):
    """
    :param latitude: users latitude
    :param longitude: users longitude
    :param distance: distance in km that will be a boundary
    :return:
    """
    # Earth's radius in kilometers
    earth_radius = 6371

    # Convert distance to radians
    distance_rad = distance / earth_radius

    # Convert latitude and longitude to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # Calculate the latitude boundaries
    min_lat = math.degrees(lat_rad - distance_rad)
    max_lat = math.degrees(lat_rad + distance_rad)

    # Calculate the longitude boundaries
    delta_lon = math.asin(math.sin(distance_rad) / math.cos(lat_rad))
    min_lon = math.degrees(lon_rad - delta_lon)
    max_lon = math.degrees(lon_rad + delta_lon)

    return {
        "minimal_point": GP(min_lat, min_lon),
        "maximal_point": GP(max_lat, max_lon)
    }
