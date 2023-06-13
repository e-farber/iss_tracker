import requests as req
import json
from geopy import distance
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent='a.larry@web.de')

seconds = 3

response1 = req.get("http://api.open-notify.org/iss-now.json")  # get location data twice with 'seconds' delay
time.sleep(seconds)
response2 = req.get("http://api.open-notify.org/iss-now.json")

lat1 = response1.json()['iss_position']['latitude']             # extract lat and lon
lon1 = response1.json()['iss_position']['longitude']

lat2 = response2.json()['iss_position']['latitude']
lon2 = response2.json()['iss_position']['longitude']

location1 = geolocator.reverse((lat1, lon1), language="en")     # get map information from coordinates
location2 = geolocator.reverse((lat2, lon2), language="en")


def jprint(obj):                                                # function for printing json data
    text = json.dumps(obj, indent=2, sort_keys=True)
    print(text)


print('First measuring: latitude: {}, longitude:{} \n'
      'Second measuring: latitude: {}, longitude: {}'.format(lat1, lon1, lat2, lon2))

if location2 is None:
    print('ISS location not found. Probably above the ocean.')
else:
    print('ISS location currently above {}'.format(location2.raw['display_name']))

print('Distance travelled in past {} seconds on earth: {:.1f}km'
      .format(seconds, distance.distance((lat1, lon1), (lat2, lon2)).km))

dist_factor = (6370+408)/6370       # (earth radius + ISS height) / earth radius
print('Distance travelled in past {} seconds in space: {:.1f}km'
      .format(seconds, distance.distance((lat1, lon1), (lat2, lon2)).km*dist_factor))
