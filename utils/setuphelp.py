#!/usr/bin/env python
import requests
import urllib.parse

myaddress = 'Greenwich'
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(myaddress) +'?format=json'

response = requests.get(url).json()
print("For %s the Latitude is %s and the Longitude is %s" % (myaddress, response[0]["lat"], response[0]["lon"]))