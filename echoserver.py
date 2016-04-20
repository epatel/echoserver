#!/usr/bin/python

# Echo chamber server
# -------------------
#
# Copyright (c) 2016 Edward Patel, http://memention.com/
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import signal
import socket
import time
import threading
import SocketServer

client_lock = threading.Lock()
clients = {}

entry_key = "498412F0-01BC-4A60-83C4-FD3972EA92E9"
socket_port = 2000

class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):

    channelKey = ""

    def write(self, output):
        global clients
        global client_lock

        with client_lock:
            for client in clients[self.channelKey]:
                if client != self:
                    client.wfile.write(output)

    def handle(self):
        global clients
        global client_lock

        try:

            keyset = 0
            key = self.rfile.readline().strip()

            if key == entry_key:

                self.channelKey = self.rfile.readline().strip()
                keyset = 1

                with client_lock:
                    if clients.has_key(self.channelKey):
                        channel = clients[self.channelKey]
                    else:
                        channel = []
                        clients[self.channelKey] = channel
                    channel.append(self)
                    
                while True:
                    data = self.rfile.readline()
                    if data == "" or data[0] == '\004':
                        break
                    if data == "ping\n":
                        with client_lock:
                            self.wfile.write("pong\n")
                    else:
                        self.write(data)

                with client_lock:
                    clients[self.channelKey].remove(self)
            print "close normal"
                
        except:
            if keyset == 1:
                with client_lock:
                    clients[self.channelKey].remove(self)
            print "close exception"

        finally:
            self.request.close()

            
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":

    addr = ("0.0.0.0", socket_port)

    SocketServer.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer(addr, ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        while True:
            time.sleep(1)

    except:
        print "Exception"

    finally:
        print "Exiting"
        with client_lock:
            for channel in clients.keys():
                for client in clients[channel]:
                    print "client ", client, "chan ", channel
                    client.request.close()

    server.shutdown()
    server.server_close()
