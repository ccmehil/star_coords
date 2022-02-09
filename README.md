# Star Coordinates

Get the AltAz coordinates for a given object using astropy and output on a OLED screen.

As a very very newcomer to the astronomy scene and living in a area with a bit higher light pollution I find it's necessary to get the AltAz coordinates for an object to help me find it.

My understanding is the the Alt is a degree point ona 360 degree circle where 0 is True North. and Az is a degree of elevation or tilt the telescope has within a range of -90 to 90 degrees. Where as other from 0 to 90 is visible, although based on my elevation anything from 30 to 90 is more likely.

# Dependencies

The whole thing has been written using Python 3+

- [luma.oled](https://pypi.org/project/luma.oled/)
- [numpy](https://pypi.org/project/mumpy/)
- [astropy](https://www.astropy.org)


# Install

```
sudo apt-get install git python3-pip libatlas3-base libopenjp2-7 i2c-tools
sudo pip3 install luma.oled
sudo pip3 install astropy
sudo pip3 install numpy
cd /home/pi/
git clone https://github.com/ccmehil/star_coords.git
```

# Configuration

To determine the address for your OLED screen

```sudo i2cdetect -y 1```

You will need to possibly modify ```server.py``` lines: 163-164

```
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
```

# Troubleshooting

If you are getting odd errors related to ```numpy``` you may need to do the following.

```
pip3 uninstall numpy
sudo apt-get remove python3-numpy
sudo pip3 install numpy
```

# Usage

```python /home/pi/star_coords/server.py -d TRUE -s 10.0.0.1 -p 8080```

- > -d either TRUE or FALSE if you want to use the OLED display or not, no value defaults to TRUE
- > -s is your hostname or IP of your Raspberry Pi, mine the hostname is ```starcoords```so I would give ```starcoords.local``` no value will result in it getting the hostname and adding ```.local``` automatically.
- > -p is the port number for the server to start on, no value will default to 8080


To use the server once it is running you will need to make an HTTP request.

Your first request should be to set your location. This can be your specific street address, etc. If you do this via an [Apple Shortcut](https://www.icloud.com/shortcuts/9d29a74ce7744c2580c74f36ab9dfa5a) you can use the mapping function to get your address. In these examples the IP address of course is whatever that of your Raspberry Pi or your hostname you gave above when starting the server.

> http://10.0.0.1:8080?address=Greenwich

You can also deactivate or activate the OLED display from a HTTP call as well.

> http://10.0.0.1:8080?display=TRUE

Otherwise you can use either the ```messier``` or the ```planet``` parameters to search for your object based on your current location.

> http://10.0.0.1:8080?messier=M41

The parameter "messier=XXX" is a object from the [Messier Catalog](https://en.wikipedia.org/wiki/Messier_object).

If you are an Apple user you can use this [Apple Shortcut](https://www.icloud.com/shortcuts/ba09a1a658c7462484d6e64e5392c1a3) I made to interact with the server while star gazing. Siri will even react via voice input over your Apple Watch or by asking "Hey Siri"

![Notifications from the Shortcut](docs/IMG_0933.jpg "Notifications")

With the current version you can also search for a planet. This is an either or type of search either a Messier Object or a Planet, not both.

> http://10.0.0.1:8080?planet=mars

Another [Apple Shortcut](https://www.icloud.com/shortcuts/8eb5d1e27f044187959cbe59aadaaea7) I made is to interact with the server while looking for a planet. Siri will even react via voice input over your Apple Watch or by asking "Hey Siri"

![Notifications from the Shortcut](docs/IMG_PLANET_NOT.jpeg "Notifications")

To stop the server once it is running you will need to make an HTTP request.

> http://10.0.0.1:8080?getout=true


# Hardware

I'm using a sh1106 module for the OLED display and a [Raspberry Pi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-w/) 

![Example Running](docs/IMG_0931.jpg "Live")

![Wiring](docs/Raspberry_Pi_OLED_Display_128_64.jpg "RPi Wiring")

# Extras

This is a project by a hobby newbie, I've had a telescope for less than a month when I created this project and I'm still learning, lingo and other associations. All feedback, contribution and engagement is welcome! Python is also relatively new to me. 

- [Code of Conduct](docs/CODE_OF_CONDUCT.md)
- [License](docs/LICENSE)

# OPTIONAL (not tested)

Don't do this unless you are sure it's running properly with your information saved and taken care.

```
sudo nano /etc/profile
```

Scroll to the bottom and add the following line

```
sudo python /home/pi/star_coords/server.py
```

This will start the server on boot/reboot.