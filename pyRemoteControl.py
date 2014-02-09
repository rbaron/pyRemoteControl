#!/usr/bin/env python2

from util import Networking, Controller
import socket

VERSION = '1.0'

srv = Networking.Server()
ctrl = Controller.Controller()

print 'pyRemoteControl version v{0} - running on IP: {1}'.format(VERSION, srv.localaddr)

while True:

  try:
    print 'Waiting for connection...'
    srv.accept()

    print 'New connection from '+srv.clientaddr[0]
    srv.receive()

    while(len(srv.message) > 0):
      ctrl.handle_message(srv.message)
      srv.receive()

  except socket.error, e:
    print "pyRemoteControl: Socket exception ("+str(e)+"). Re-accept()'ing."


print "pyRemoteControl: clean exit."
