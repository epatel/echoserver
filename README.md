# Echo Server

I created this echo server for a couple of personal projects. I run it on a private server and use it to connect devices and create a simple push feature between the connected devices. Recently I bought a Ring ZERO (a bluetooth enabled ring that can recognise gestures) and wanted to make a Spotify client that could play in the background. This could not be made with the ordinary ring0 SDK so I came up with the idea to use this echo server. So to share this solution I now share the echo server here.

```
./echoserver.py
```

Look inside to change the key and port.

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
