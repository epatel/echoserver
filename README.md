# Echo Server

I created this echo server for a couple of personal projects. I run it on a private server and use it to connect devices and create a simple push feature between the connected devices. Recently I bought a Ring ZERO (a bluetooth enabled ring that can recognise gestures) and wanted to make a Spotify client that could play in the background and recieve ring gestures. This could not be made with the ordinary ring0 SDK so I came up with the idea to use this echo server. So to share this solution I now share the echo server here. I also added the echo server connection to the `Simple Track Playback` sample code here https://github.com/epatel/ios-sdk (see branch `epatel/ring0`)

```
./echoserver.py
```

Look inside to change the key and port.

Please note that all the demos use the same channel ID (`RX-03E4`) which should be changed if you wish to run on my private server while testing. Please setup your own echo server for your own purpose, I will not guarantee that I will be running my echo server for any period of time.

When connecting to the echo server it initialy takes 2 lines, the first has to be a specific UUID key and the second a string that will be used as a "channel" name. All clients connected to the same "channel" will receive the same data and they can send data to all connected clients (but no feedback of own data).

One way to test/listen in on a channel is to connect to the server with `nc`

```
( echo $ECHO_KEY ; echo $ECHO_CHANNEL; cat ) | nc $ECHO_HOST $ECHO_PORT
```

# ring0-setup

`ring0-setup` is a command line tool that can be used in the OSX Terminal to listen in on a channel and control Spotify, generate some key events i.e. controlling a presentation app like Deckset, or just say the gesture made.

```
source ring0-setup
ring echo
```

# ring.cgi

`ring.cgi` is a tiny cgi script available on the same server as the echo server. With this the Ring ZERO iOS app can post events into a channel and thus control a Spotify client, using the Open URI feature in the Ring ZERO app.

```
curl http://echo.memention.net/ring.cgi/RX-03E4/right
```

# Command line demo

[![asciicast](https://asciinema.org/a/6k7kmitlapxg1p9rqqeixll34.png)](https://asciinema.org/a/6k7kmitlapxg1p9rqqeixll34)

# Youtube demos

Desktop

[![Desktop](https://img.youtube.com/vi/fD2CYi0AcE0/0.jpg)](https://www.youtube.com/watch?v=fD2CYi0AcE0)

Spotify on iPhone

[![Spotify on iPhone](https://img.youtube.com/vi/dS920OrCZGc/0.jpg)](https://www.youtube.com/watch?v=dS920OrCZGc)

Ring ZERO app configuration, Open URI for the "right" gesture

![Open URI](http://echo.memention.net/open-uri.jpg)
