#!/usr/bin/env python3
"""Static file server for Ryan's Vinyl Collection."""
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silence logs

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('', 3010), Handler)
    print('✦  Vinyl Collection → http://localhost:3010')
    server.serve_forever()
