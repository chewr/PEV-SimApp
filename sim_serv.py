#!/usr/bin/env python
## TODO the server that runs the simulation. Should receive
## requests from the front end, dispatch the simulation,
## and update the front end with visualization data

## server code courtesy of https://snipt.net/raw/f8ef141069c3e7ac7e0134c6b58c25bf/?nice
## @rochacbruno

import SimpleHTTPServer
import SocketServer
import logging
import cgi

import sys


PORT = 8233


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        logging.warning("======= POST VALUES =======")
        for item in form.list:
            logging.warning(item)
        logging.warning("\n")
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

httpd.serve_forever()
