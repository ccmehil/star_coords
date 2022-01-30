#!/usr/bin/env python
"""
Use AstroPy to output AltAz for a object in the sky
Craig Cmehil - https://github.com/ccmehil
"""

import os
import sys
import subprocess
import time
import datetime
import numpy as np
from datetime import datetime as dt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

print("Checking Configuration")
config_file = "server.ini"
if not os.path.isfile(config_file):
    print("Using default settings")
    h = open("server.ini", "w")
    #Default to Greenwich as the site, 1 as tz
    h.write("[site]\n")
    h.write("\naddress=Greenwich")
    h.write("\nlatitude=51.4874277")
    h.write("\nlongitude=-0.012965")
    h.close()

config = configparser.ConfigParser()
config.read("server.ini")
#server_name = config.get("server", "name") #e.g. 10.0.0.1
#server_port = config.getint("server", "port") #e.g. 4030
site_address = config.get("site", "address") #e.g. Greenwich
site_latitude = config.get("site", "latitude") #e.g. 51.4874277
site_longitude = config.get("site", "longitude") #e.g. -0.012965

# Debug statements in each function start with 'FUNCTION xxxxx' 
# or simply with ' ' to display all 
debug = True
debug_function = ' '

def debug_info(str):
    if debug:
        if debug_function in str:
            sys.stdout.write("%s\n" % str)

#Set local site (AltAz)
location = EarthLocation.of_address(site_address)
debug_info("Location %r" % location)

skyobject = SkyCoord.from_name('M39')
skyobjectaltaz = skyobject.transform_to(AltAz(obstime=dt.utcnow(),location=location))
az = skyobjectaltaz.az.to_string()
print("Turn Base to = %s" % az.rpartition('d')[0])
print("Raise/Lower Scope to = %s" % skyobjectaltaz.alt)
