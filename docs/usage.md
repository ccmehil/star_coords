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

Your first request should be to set your location. This can be your specific street address, etc. If you do this via an [Apple Shortcut](https://www.icloud.com/shortcuts/e3ac3bb7342e49e9813a2d39ec4970e2) you can use the mapping function to get your address. In these examples the IP address of course is whatever that of your Raspberry Pi or your hostname you gave above when starting the server.

> http://10.0.0.1:8080?cmd=address&address=Greenwich

You can also use specific Latitude, Longitude and Altitude to set your location, for example with this [Apple Shortcut](https://www.icloud.com/shortcuts/ea2e6b2d357d4bc9a7ceaf010d55c4a0)

> http://10.0.0.1:8080?cmd=coordinates&lat=51.1&lon=1&alt=32

You can also deactivate or activate the OLED display from a HTTP call as well.

> http://10.0.0.1:8080?cmd=display&value=TRUE

## 

Otherwise you can use either the ```messier``` or the ```planet``` parameters to search for your object based on your current location.

> http://10.0.0.1:8080?cmd=messier&object=M41

The parameter "messier=XXX" is a object from the [Messier Catalog](https://en.wikipedia.org/wiki/Messier_object).

If you are an Apple user you can use this [Apple Shortcut](https://www.icloud.com/shortcuts/45bed2102bac4d308d4f300a29d79aa9) I made to interact with the server while star gazing. Siri will even react via voice input over your Apple Watch or by asking "Hey Siri"

![Notifications from the Shortcut](IMG_0933.jpg "Notifications")

With the current version you can also search for a planet. This is an either or type of search either a Messier Object or a Planet, not both.

> http://10.0.0.1:8080?cmd=planet&object=mars

Another [Apple Shortcut](https://www.icloud.com/shortcuts/cc36a75e4ef843f687242abfc9845b84) I made is to interact with the server while looking for a planet. Siri will even react via voice input over your Apple Watch or by asking "Hey Siri"

![Notifications from the Shortcut](IMG_PLANET_NOT.jpeg "Notifications")

To stop the server once it is running you will need to make an HTTP request.

> http://10.0.0.1:8080?cmd=exit

Also an [Apple Shortcut](https://www.icloud.com/shortcuts/196ff03a109146a9ae3f5a11a2602fa5) to quickly perform the action.
