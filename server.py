#!/usr/bin/env python
"""
Use AstroPy to output AltAz for a object in the sky
Craig Cmehil - https://github.com/ccmehil
"""

import os
from pickle import TRUE
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
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, solar_system_ephemeris
from astropy.coordinates import get_body_barycentric, get_body, get_moon
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

print("******************************************************")
print("*                   Star Coords                      *")
print("* Hopefully you triggered this to start with boot    *")
print("* after you did the configuration and tested that    *")
print("* it is working properly. Otherwise...               *")
print("* pkill -9 -f server.py                              *")
print("******************************************************")

print("Checking Configuration")
config_file = "server.ini"
if not os.path.isfile(config_file):
    print("Using default settings")
    h = open("server.ini", "w")
    # default web server for localhost
    h.write("[server]")
    h.write("\nname=10.0.0.1")
    h.write("\nport=8080")
    #Default to Greenwich as the site, 1 as tz
    h.write("[\nsite]")
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

# Planet Objects
theplanets = ['sun',  'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

# Use OLED?
oled_active = TRUE

#Connect oled type is sh1106
if oled_active:
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial)

def outputDisplay(line1, line2):
    # Output to OLED
    if oled_active:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((3, 10), "--------------------", fill="white")
            draw.text((3, 20), line1, fill="white")
            draw.text((3, 30), line2 , fill="white")
            draw.text((3, 40), "--------------------", fill="white")
    return

# HTTP Server
class SimpleWebServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_POST(self):
        return

    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

        query = urlparse(self.path).query
        messier = parse_qs(query).get('messier', None)
        planet = parse_qs(query).get('planet', None)
        getout = parse_qs(query).get('getout', None)
        print(messier)
        print(planet)
        print(getout)

        # get Coords of Sky Object for a Messier Object
        str = ''
        if(messier is not None):
            skyobject = SkyCoord.from_name(messier[0].upper())
            skyobjectaltaz = skyobject.transform_to(AltAz(obstime=dt.utcnow(),location=location))
            az = skyobjectaltaz.az.to_string()
            alt = skyobjectaltaz.alt.to_string()
            # Output to OLED
            if oled_active:
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((3, 10), "  Star Coords - %s  " % messier[0].upper(), fill="white")
                    draw.text((3, 20), "--------------------", fill="white")
                    draw.text((3, 30), "   Base: = %s" % az.rpartition('d')[0], fill="white")        
                    draw.text((3, 40), "  Scope: = %s" % alt.rpartition('d')[0], fill="white")
            # Output to HTTP Request
            str = "%s: Base: = %s Scope: = %s" % (messier[0].upper(), az.rpartition('d')[0],  alt.rpartition('d')[0])
        elif(planet is not None):
            if (planet[0].lower() in theplanets):
                now = dt.utcnow()
                dt_string = dt_string = now.strftime("%Y-%m-%d %H:%M")
                t = Time(dt_string)
                with solar_system_ephemeris.set('builtin'):
                    planetlocation = get_body(planet[0].lower(), t, location) 
                ra = planetlocation.ra.to_string()
                dec = planetlocation.dec.to_string() 
                # Output to OLED
                if oled_active:
                    with canvas(device) as draw:
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((3, 10), "  Planet Coords     ", fill="white")
                        draw.text((3, 20), "  %s                " % planet[0].upper(), fill="white")
                        draw.text((3, 30), "--------------------", fill="white")
                        draw.text((3, 40), "   Base: = %s" % ra.rpartition('d')[0], fill="white")        
                        draw.text((3, 50), "  Scope: = %s" % dec.rpartition('d')[0], fill="white")
                # Output to HTTP Request
                str = "%s: Base: = %s Scope: = %s" % (planet[0].upper(), ra.rpartition('d')[0],  dec.rpartition('d')[0])
            else:
                # Output to OLED
                if oled_active:
                    with canvas(device) as draw:
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((3, 10), "  Planet Coords   ", fill="white")
                        draw.text((3, 20), "--------------------", fill="white")
                        draw.text((3, 30), "   Base: = ", fill="white")        
                        draw.text((3, 40), "  Scope: = ", fill="white")
                # Output to HTTP Request
                str = "Invalid Planet should be %s" % theplanets
        elif(getout is not None):
            outputDisplay("     Star Coords    ", "      Shutdown      ")
            sleep(10)
            sys.exit()
        else:
            # Output to OLED
            if oled_active:
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((3, 10), "--------------------", fill="white")
                    draw.text((3, 20), "     Star Coords    ", fill="white")
                    draw.text((3, 30), "    Planet Coords   ", fill="white")
                    draw.text((3, 40), "--------------------", fill="white")
            # Output to HTTP Request
            str = "No Messier Object or Invalid Planet should be %s" % theplanets
        return bytes(str, "UTF-8")
        
    def respond(self):
        content = self.handle_http(200, 'text/html')
        self.wfile.write(content)   

    def do_GET(self):        
        self.respond()

if __name__ == "__main__":
    #Set local site (AltAz)
    location = EarthLocation.of_address(site_address)
    print("Location %r" % location)

    # Start Web server
    httpd = HTTPServer((server_name, server_port), SimpleWebServer)
    print(time.asctime(), 'Star Coords Server UP - %s:%s' % (server_name, server_port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (server_name, server_port))
