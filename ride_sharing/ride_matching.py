#ride_matching.py
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D  # D is used to specify distances
from .models import Ride

def match_rides_for_passenger(passenger_pickup, passenger_dropoff):
    """
    Find rides that match the passenger's request using the 10% rule.
    Args:
        passenger_pickup (tuple): Coordinates of the passenger's pickup location (lat, lon).
        passenger_dropoff (tuple): Coordinates of the passenger's dropoff location (lat, lon).
    Returns:
        List of matching rides.
    """
    matching_rides = []

    # Get all available rides
    available_rides = Ride.objects.filter(ride_status="Available")

    for ride in available_rides:
        # Get driver's departure and destination points
        driver_departure = ride.pickup_location
        driver_destination = ride.dropoff_location
        driver_route_distance = ride.distance

        # Convert passenger coordinates to Point objects (lon, lat)
        passenger_pickup_point = Point(passenger_pickup[1], passenger_pickup[0])  # (lon, lat)
        passenger_dropoff_point = Point(passenger_dropoff[1], passenger_dropoff[0])  # (lon, lat)

        # Calculate distances from the passenger's pickup and dropoff locations
        departure_to_pickup = driver_departure.distance(passenger_pickup_point)
        dropoff_to_destination = driver_destination.distance(passenger_dropoff_point)

        # Check the 10% rule conditions
        if departure_to_pickup <= D(0.1 * driver_route_distance) and dropoff_to_destination <= D(0.1 * driver_route_distance):
            matching_rides.append(ride)
            continue

        # Alternative route checks
        pickup_to_route = driver_departure.distance(passenger_pickup_point)
        dropoff_to_route = driver_destination.distance(passenger_dropoff_point)

        if pickup_to_route <= D(0.1 * driver_route_distance) and dropoff_to_route <= D(0.1 * driver_route_distance):
            matching_rides.append(ride)

    return matching_rides
