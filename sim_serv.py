#!/usr/bin/env python
## TODO the server that runs the simulation. Should receive
## requests from the front end, dispatch the simulation,
## and update the front end with visualization data
import SimpleHTTPServer
import SocketServer

# minimal web server.  serves files relative to the
# current directory.

PORT = 8233

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()

