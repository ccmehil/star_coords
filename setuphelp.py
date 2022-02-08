#!/usr/bin/env python
import requests

myaddress = 'Greenwich'

response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s' % myaddress)
payload = response.json()
print(payload['results'][0]['geometry']['location'])