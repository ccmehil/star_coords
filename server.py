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
    h.write("\naddress=Greenwich\n")
    h.write("\ntz=1\n")
    h.write("\nlatitude=51.6712\n")
    h.write("\nlongitude=8.3406\n")
    h.close()

config = configparser.ConfigParser()
config.read("server.ini")
server_name = config.get("server", "name") #e.g. 10.0.0.1
server_port = config.getint("server", "port") #e.g. 4030
site_address = config.get("site", "address") #e.g. Greenwich
site_tz = config.get("site", "tz") #e.g. 1
site_latitude = config.get("site", "latitude") #e.g. 51.4176
site_longitude = config.get("site", "longitude") #e.g. 8.1923

# Debug statements in each function start with 'FUNCTION xxxxx' 
# or simply with ' ' to display all 
debug = True
debug_function = ' '

def debug_info(str):
    if debug:
        if debug_function in str:
            sys.stdout.write("%s\n" % str)

def obs_time():
    debug_info("FUNCTION obs_time")
    now = dt.now()
    times = [now]
    t = Time(times, scale='utc')
    obstime = Time(t) + np.linspace(0, 6, 10000) * u.hour
    return obstime

#Set local site (AltAz)
obs = obs_time()
location = EarthLocation.of_address(site_address)
debug_info("Location %r" % location)

m33 = SkyCoord.from_name('M33')
m33altaz = m33.transform_to(AltAz(obstime=obs,location=location))
print(f"M33's Altitude = {m33altaz.alt:.2}")
print(f"M33's Az = {m33altaz.az:.2}")