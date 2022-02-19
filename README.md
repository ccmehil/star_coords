# Star Coordinates

Get the AltAz coordinates for a given object using astropy and output on a OLED screen.

As a very very newcomer to the astronomy scene and living in a area with a bit higher light pollution I find it's necessary to get the AltAz coordinates for an object to help me find it.

My understanding is the the Alt is a degree point ona 360 degree circle where 0 is True North. and Az is a degree of elevation or tilt the telescope has within a range of -90 to 90 degrees. Where as other from 0 to 90 is visible, although based on my elevation anything from 30 to 90 is more likely.

# Dependencies

- [luma.oled](https://pypi.org/project/luma.oled/)
- [numpy](https://pypi.org/project/mumpy/)
- [astropy](https://www.astropy.org)

Also be sure that you have enabled GPIO and I2C using ```sudo raspi-config``` if you intend to use an OLED display.

If Not you can follow some simple [instructions](https://raspberrytips.com/install-latest-python-raspberry-pi/) to update your Raspberry Pi.

# Install

```
sudo apt-get install git python3-pip libatlas3-base libopenjp2-7 i2c-tools
sudo pip3 install luma.oled astropy numpy
cd /home/pi/
git clone https://github.com/ccmehil/star_coords.git
```

# Configuration

To determine the address for your OLED screen

```sudo i2cdetect -y 1```

You will need to possibly modify ```server.py``` lines: 220-221

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

# OPTIONAL (not tested)

Don't do this unless you are sure it's running properly with your information saved and taken care.

```
sudo nano /etc/profile
```

Scroll to the bottom and add the following line

```
sudo python /home/pi/star_coords/server.py -d TRUE -s 10.0.0.1 -p 8080
```

This will start the server on boot/reboot.

# Usage

To understand about using the server please see [Usage](docs/usage.md)

# Hardware

For details about the hardware and wiring see [Hardware](docs/hardware.md)

# Extras

This is a project by a hobby newbie, I've had a telescope for less than a month when I created this project and I'm still learning, lingo and other associations. All feedback, contribution and engagement is welcome! Python is also relatively new to me. 

- [Code of Conduct](docs/CODE_OF_CONDUCT.md)
- [License](docs/LICENSE)