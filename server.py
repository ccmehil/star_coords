#!/usr/bin/env python
"""
Use AstroPy to output AltAz for a object in the sky
Craig Cmehil - https://github.com/ccmehil
"""

import os
import sys
import getopt
import subprocess
import time
import datetime
from datetime import datetime as dt
from time import sleep
# Astro
import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
# oled Display
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010

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
debug_function = 'none'

def debug_info(str):
    if debug:
        if debug_function in str:
            sys.stdout.write("%s\n" % str)

def main(argv):
    global location
    argumentList = sys.argv[1:]
    options = "hm:"
    long_options = ["Help", "Messier_Object ="]    
    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        for currentArgument, currentValue in arguments:    
            if currentArgument in ("-h", "--Help"):
                print("Displaying Help\n")
                print("server.py -m <messierobject>\n")
                sys.exit()          
            elif currentArgument in ("-m", "--Messier_Object"):
                print("Displaying Messier Object:", currentValue)
                return currentValue    
    except getopt.error as err:
        print(str(err))
        sys.exit()

#Set local site (AltAz)
location = EarthLocation.of_address(site_address)
debug_info("Location %r" % location)

#Connect oled
serial = i2c(port=4, address=0x3C)
device = sh1106(serial)

if __name__ == "__main__":
    arg = main(sys.argv[1:])
    skyobject = SkyCoord.from_name(arg)
    skyobjectaltaz = skyobject.transform_to(AltAz(obstime=dt.utcnow(),location=location))
    az = skyobjectaltaz.az.to_string()
    alt = skyobjectaltaz.alt.to_string()    
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30, 40), "Star Coords", fill="white")
        draw.text((30, 40), "------------------", fill="white")
        draw.text((30, 40), "Turn Base to = %s" % az.rpartition('d')[0], fill="white")        
        draw.text((30, 40), "Raise/Lower Scope to = %s" % alt.rpartition('d')[0], fill="white")
    sleep(10)