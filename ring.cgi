#!/bin/bash

ECHO_HOST=echo.memention.net
ECHO_PORT=2000
ECHO_KEY=498412F0-01BC-4A60-83C4-FD3972EA92E9
ECHO_CHANNEL=`dirname $PATH_INFO`
ECHO_COMMAND=`basename $PATH_INFO`

echo "Content-type: text/html; charset=UTF-8"
echo

( echo $ECHO_KEY ; basename $ECHO_CHANNEL ; echo $ECHO_COMMAND ) | nc localhost $ECHO_PORT

echo "$ECHO_COMMAND Posted"
