#!/usr/bin/env python
"""
Use AstroPy to output AltAz for a object in the sky
Craig Cmehil - https://github.com/ccmehil
"""

import os
import argparse
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


print("******************************************************")
print("*                   Star Coords                      *")
print("* Hopefully you triggered this to start with boot    *")
print("* after you did the configuration and tested that    *")
print("* it is working properly. Otherwise...               *")
print("* pkill -9 -f server.py                              *")
print("******************************************************")

# Planet Objects
theplanets = ['sun',  'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

def outputDisplay(line1, line2, line3, line4, line5):
    # Output to OLED
    if oled_active:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((3, 10), line1, fill="white")
            draw.text((3, 20), line2, fill="white")
            draw.text((3, 30), line3, fill="white")
            draw.text((3, 40), line4, fill="white")
            draw.text((3, 50), line5, fill="white")
    return

# HTTP Server
class SimpleWebServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_POST(self):
        return

    def handle_http(self, status, content_type):
        global location, oled_active
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

        query = urlparse(self.path).query
        cmd = parse_qs(query).get('cmd', None)

        match cmd[0]:
            case "messier":
                obj = parse_qs(query).get('object', None)
                if (obj is not None):
                    skyobject = SkyCoord.from_name(obj[0].upper())
                    skyobjectaltaz = skyobject.transform_to(AltAz(obstime=dt.utcnow(),location=location))
                    az = skyobjectaltaz.az.to_string()
                    alt = skyobjectaltaz.alt.to_string()
                    outputDisplay("  Star Coords - %s  " % obj[0].upper(), "--------------------",  "   Base: = %s" % az.rpartition('d')[0], "  Scope: = %s" % alt.rpartition('d')[0], "")
                    str = "%s: Base: = %s Scope: = %s" % (obj[0].upper(), az.rpartition('d')[0],  alt.rpartition('d')[0])
                else:
                    outputDisplay("   Star Coords   ", "--------------------", "   Base: = ", "  Scope: = ", "")
                    str = "Invalid Object"
            case "planet":
                obj = parse_qs(query).get('object', None)
                if (obj is not None and obj[0].lower() in theplanets):
                    now = dt.utcnow()
                    dt_string = dt_string = now.strftime("%Y-%m-%d %H:%M")
                    t = Time(dt_string)
                    with solar_system_ephemeris.set('builtin'):
                        planetlocation = get_body(obj[0].lower(), t, location) 
                    ra = planetlocation.ra.to_string()
                    dec = planetlocation.dec.to_string()
                    outputDisplay("  Planet Coords   ", "  %s                " % obj[0].upper(), "--------------------", "   Base: = %s" % ra.rpartition('d')[0],  "  Scope: = %s" % dec.rpartition('d')[0])
                    str = "%s: Base: = %s Scope: = %s" % (obj[0].upper(), ra.rpartition('d')[0],  dec.rpartition('d')[0])
                else:
                    outputDisplay("  Planet Coords   ", "--------------------", "   Base: = ", "  Scope: = ", "")
                    str = "Invalid Planet should be %s" % theplanets
            case "address":
                address = parse_qs(query).get('address', None)
                if(address is not None):
                    location = EarthLocation.of_address(address[0])
                    print("Location %r" % location)
                    outputDisplay("--------------------", "     Star Coords    ", " Latitude/Longitude ", "--------------------", "")
                    str = "Your address has now been updated"
                else:
                    outputDisplay("--------------------", "     Star Coords    ", "       Invalid      ", "--------------------", "")
                    str = "Invalid Address"
            case "coordinates":
                latitude = parse_qs(query).get('lat', None)
                longitude = parse_qs(query).get('lon', None)
                altitude = parse_qs(query).get('alt', None)
                if(latitude is not None and longitude is not None and altitude is not None):
                    print("Deterimine location from lat: %s lon: %s and alt: %s" % (latitude[0], longitude[0], altitude[0]))
                    location = EarthLocation(lat=int(float(latitude[0]))*u.deg, lon=int(float(longitude[0]))*u.deg, height=int(float(altitude[0]))*u.m)
                    print("Location %r" % location)
                    outputDisplay("--------------------", "     Star Coords    ", " Latitude/Longitude ", "--------------------", "")
                    str = "Your Latitude and Longitude have now been updated"
                else:
                    outputDisplay("--------------------", "     Star Coords    ", "       Invalid      ", "--------------------", "")
                    str = "Invalid Latitude and Longitude"
            case "display":
                display = parse_qs(query).get('value', None)
                if(display is not None):
                    oled_active = display[0]
                    str = "Display active = %s" % oled_active
                else:
                    str = "Invalid Value"
            case "exit":
                global server_name, server_port
                outputDisplay("--------------------", "     Star Coords    ", "      Shutdown      ", "--------------------", "")
                sleep(10)
                print(time.asctime(), 'Server DOWN - %s:%s' % (server_name, server_port))
                sys.exit()
            case _:
                outputDisplay("--------------------", "     Star Coords    ", "    Planet Coords   ", "--------------------", "")
                str = "Invalid command" 
        return bytes(str, "UTF-8")
        
    def respond(self):
        content = self.handle_http(200, 'text/html')
        self.wfile.write(content)   

    def do_GET(self):        
        self.respond()

if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-s", "--Server", help = "Server")
    parser.add_argument("-p", "--Port", help = "Port")
    parser.add_argument("-d", "--Display", help = "OLED")

    # Read arguments from command line
    args = parser.parse_args()

    # Indicate server or use automatic hostname with .local
    if args.Server:
        server_name = args.Server
    else:
        server_name = "%s.local" % os.uname()[1]

    # Indicate Port number or use default 8080
    if args.Port:
        server_port = args.Port
    else:
        server_port = 8080

    # Use OLED?
    if args.Display:
        oled_active = args.Display
    else:
        oled_active = TRUE

    #Connect oled type is sh1106
    if oled_active:
        serial = i2c(port=1, address=0x3C)
        device = sh1106(serial)
    
    #Set local site (AltAz) based on Greenwich
    location = EarthLocation.of_address('Greenwich')
    print("Location %r" % location)

    # Start Web server
    httpd = HTTPServer((server_name, int(server_port)), SimpleWebServer)
    print(time.asctime(), 'Star Coords Server UP - %s:%s' % (server_name, server_port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (server_name, server_port))
