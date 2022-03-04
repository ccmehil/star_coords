# Usage

```python /home/pi/star_coords/server.py -d TRUE -s 10.0.0.1 -p 8080```

- > -d either TRUE or FALSE if you want to use the OLED display or not, no value defaults to TRUE
- > -s is your hostname or IP of your Raspberry Pi, mine the hostname is ```starcoords```so I would give ```starcoords.local``` no value will result in it getting the hostname and adding ```.local``` automatically.
- > -p is the port number for the server to start on, no value will default to 8080


To use the server once it is running you will need to make an HTTP request. It's important to **NOTE** that you need internet access for your Raspberry Pi to work! The Raspberry Pi needs to be connected to a hotspot or Wifi with Internet access and then you access it via a device on the same network as the Raspberry Pi.

URL parameter ```cmd```
- messier
- planet
- address
- coordinates
- display
- exit

Each of these commands have additional URL parameters that the server looks for.
- object _(used by messier and planet)_
- address _(used by address)_
- value _(used by display)_
- lat _(used by coordinates)_
- lon _(used by coordinates)_
- alt _(used by coordinates)_

## 

Your first request should be to set your location. This can be your specific street address, etc. In these examples the IP address of course is whatever that of your Raspberry Pi or your hostname you gave above when starting the server.

> http://10.0.0.1:8080?cmd=address&address=Greenwich

You can also use specific Latitude, Longitude and Altitude to set your location.

> http://10.0.0.1:8080?cmd=coordinates&lat=51.1&lon=1&alt=32

You can also deactivate or activate the OLED display from a HTTP call as well.

> http://10.0.0.1:8080?cmd=display&value=TRUE

## 

Otherwise you can use either the ```messier``` or the ```planet``` parameters to search for your object based on your current location.

> http://10.0.0.1:8080?cmd=messier&object=M41

The parameter "messier=XXX" is a object from the [Messier Catalog](https://en.wikipedia.org/wiki/Messier_object).

With the current version you can also search for a planet. This is an either or type of search either a Messier Object or a Planet, not both.

> http://10.0.0.1:8080?cmd=planet&object=mars

To stop the server once it is running you will need to make an HTTP request.

> http://10.0.0.1:8080?cmd=exit

## API or Serverless style usage

In order to get a simple response without the HTML formatting from the server you will need to use the ´´´&api=TRUE``` parameter.

For example to set the location it would be

> http://10.0.0.1:8080?cmd=address&api=TRUE&address=Greenwich

> http://10.0.0.1:8080?cmd=coordinates&api=TRUE&lat=51.1&lon=1&alt=32

As example here are some APPLE SHORTCUTS to use to interact with the server.

- Setting your Address:  [Apple Shortcut](https://www.icloud.com/shortcuts/bf4e4ee3ba7b406b9e79e641199a7112) 
- Setting your Latitude and Longitude: [Apple Shortcut](https://www.icloud.com/shortcuts/84572f58e78341bcb1f20bd619b46170)
- Messier Object: [Apple Shortcut](https://www.icloud.com/shortcuts/7012aa9bdef34de795cb8962c3bb1469) 
- Planet Object:  [Apple Shortcut](https://www.icloud.com/shortcuts/157637bebcad4013b76c17e34cf23428) 
- Shutting down the Server: [Apple Shortcut](https://www.icloud.com/shortcuts/3bacae101a91436ca7d71cdd583aa135) 

![Notifications from the Shortcut](IMG_0933.jpg "Notifications")
![Notifications from the Shortcut](IMG_PLANET_NOT.jpeg "Notifications")
