# Jwala Circle : 28.549051, 77.184498
# Himadri Circle : 28.544856, 77.194436
# SAC Circle : 28.546737, 77.185113

import platform
import time
import math


def get_location():
    if(platform.system()=="Darwin"):
        import CoreLocation
        locationManager = CoreLocation.CLLocationManager.alloc().init()
        locationManager.startUpdatingLocation()
        # Wait for a moment to allow the location to be updated
        time.sleep(2)
        location = locationManager.location()
        locationManager.stopUpdatingLocation()
        if location:
            coordinates = location.coordinate()
            latitude = coordinates.latitude
            longitude = coordinates.longitude
            return (latitude, longitude)
        else:
            print("Location data not available.")
            return None
    else:
        from geopy.geocoders import Nominatim
        import time

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode("")
        # Wait for a moment to allow the location to be updated
        time.sleep(2)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            return (latitude, longitude)
        else:
            print("Location data not available.")
            return None

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6378.1  # Radius of the Earth in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c * 1000  # Convert distance to meters
    return distance

if __name__ == "__main__":
    # Get your current location
    current_location = get_location()
    if current_location:
        # Coordinates of the destination
        destination_latitude = 28.549051  # Example latitude
        destination_longitude = 77.184498  # Example longitude
        
        # Calculate distance
        distance = haversine_distance(current_location[0], current_location[1], destination_latitude, destination_longitude)
        
        print(f"Distance to destination: {distance} meters")

