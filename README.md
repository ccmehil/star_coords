# Star Coordinates

Get the AltAz coordinates for a given object using astropy and output on a OLED screen.

As a very very newcomer to the astronomy scene and living in a area with a bit higher light pollution I find it's necessary to get the AltAz coordinates for an object to help me find it.

My understanding is the the Alt is a degree point ona 360 degree circle where 0 is True North. and Az is a degree of elevation or tilt the telescope has within a range of -90 to 90 degrees. Where as other from 0 to 90 is visible, although based on my elevation anything from 30 to 90 is more likely.

# Dependencies

> [luma.oled](https://pypi.org/project/luma.oled/)

# Usage

> python3 server.py

To use the server once it is running you will need to make an HTTP request.

> http://10.0.0.1:8080?messier=M41

The IP address of course is whatever that of your Raspberry Pi is and the parameter "messier=XXX" is a object from the [Messier Catalog](https://en.wikipedia.org/wiki/Messier_object).

# Hardware

![Example Running](IMG_0931.jpg "Live")

![Wiring](Raspberry_Pi_OLED_Display_128_64.jpg "RPi Wiring")
