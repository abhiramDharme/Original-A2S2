import platform
import time
import math
import subprocess as sp
import re
import time
import numpy as np

MULTIPLY = np.array([[-10349.3216, 21401.1892], [-28356.9694, -10614.5441]])
ADD = np.array([[-1355995.58, 1629000.4379]])


def get_location():
    if(platform.system()=="Darwin"):
        import objc
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
    elif(platform.system()=="Windows"):
        wt = 5 # Wait time -- I purposefully make it wait before the shell command
        accuracy = 3 #Starting desired accuracy is fine and builds at x1.5 per loop

        pshellcomm = ['powershell']
        pshellcomm.append('add-type -assemblyname system.device; '\
                        '$loc = new-object system.device.location.geocoordinatewatcher;'\
                        '$loc.start(); '\
                        'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '\
                        '{start-sleep -milliseconds 100}; '\
                        '$acc = %d; '\
                        'while($loc.position.location.horizontalaccuracy -gt $acc) '\
                        '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; '\
                        '$loc.position.location.latitude; '\
                        '$loc.position.location.longitude; '\
                        '$loc.stop()' %(accuracy))

        p = sp.Popen(pshellcomm, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.STDOUT, text=True)
        (out, err) = p.communicate()
        out = re.split('\n', out)

        lat = float(out[0])
        long = float(out[1])

    return (lat, long)

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

def pixel_distance(x1, y1, x2, y2):
    factor = 4.18820594354041  #could best fit?
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist * factor

def coord_to_pixel(x, y):
    [[pixel_x, pixel_y]] = MULTIPLY @ np.array([x,y]) + ADD
    pixel_x = round(pixel_x)
    pixel_y = round(pixel_y)
    return (pixel_x, pixel_y)