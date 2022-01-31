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
# web server to send HTTP request for object locations
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

print("Checking Configuration")
config_file = "server.ini"
if not os.path.isfile(config_file):
    print("Using default settings")
    h = open("server.ini", "w")
    # default web server for localhost
    h.write("[server]\n")
    h.write("\nname=10.0.0.1")
    h.write("\nport=8080")
    #Default to Greenwich as the site, 1 as tz
    h.write("[site]\n")
    h.write("\naddress=Greenwich")
    h.write("\nlatitude=51.4874277")
    h.write("\nlongitude=-0.012965")
    h.close()

config = configparser.ConfigParser()
config.read("server.ini")
server_name = config.get("server", "name") #e.g. 10.0.0.1
server_port = config.getint("server", "port") #e.g. 8080
site_address = config.get("site", "address") #e.g. Greenwich
site_latitude = config.get("site", "latitude") #e.g. 51.4874277
site_longitude = config.get("site", "longitude") #e.g. -0.012965

# Debug statements in each function start with 'FUNCTION xxxxx' 
# or simply with ' ' to display all 
debug = True
debug_function = 'none'

#Connect oled type is sh1106
serial = i2c(port=4, address=0x3C)
device = sh1106(serial)

# HTTP Server
class SimpleWeb(BaseHTTPRequestHandler):
    def do_GET(self):        
        # Get parameter
        debug_info("FUNCTION do_GET: %r" % self)
        debug_info("FUNCTION do_GET: %r" % self.path)
        query = urlparse(self.path).query
        debug_info("FUNCTION do_GET: query - %r" % query)
        mobject = parse_qs(query).get('messier', None)
        debug_info("FUNCTION do_GET: mobject - %r" % mobject)

        if mobject:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # get Coords of Sky Object
            skyobject = SkyCoord.from_name(mobject)
            skyobjectaltaz = skyobject.transform_to(AltAz(obstime=dt.utcnow(),location=location))
            az = skyobjectaltaz.az.to_string()
            alt = skyobjectaltaz.alt.to_string()    
            # Output to OLED
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((3, 10), "    Star Coords     ", fill="white")
                draw.text((3, 20), "--------------------", fill="white")
                draw.text((3, 30), "   Base: = %s" % az.rpartition('d')[0], fill="white")        
                draw.text((3, 40), "  Scope: = %s" % alt.rpartition('d')[0], fill="white")
            # Output to HTTP Request
            self.wfile.write(bytes("<html><head><title>Star Coords</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("    Star Coords     ", "utf-8"))
            self.wfile.write(bytes("--------------------", "utf-8"))
            self.wfile.write(bytes("   Base: = %s" % az.rpartition('d')[0], "utf-8"))        
            self.wfile.write(bytes("  Scope: = %s" % alt.rpartition('d')[0], "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
    

def debug_info(str):
    if debug:
        if debug_function in str:
            sys.stdout.write("%s\n" % str)

if __name__ == "__main__":
    #Set local site (AltAz)
    location = EarthLocation.of_address(site_address)
    debug_info("Location %r" % location)

    # Start Web server
    webServer = HTTPServer((server_name, server_port), SimpleWeb)
    sys.stdout.write("Star Coords server started http://%s:%s" % (server_name, server_port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    sys.stdout.write("Server stopped")