#!/usr/bin/python
# from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from src import load
from src.load import *

PORT_NUMBER = 8080


# This class will handle any incoming request from
# a browser
class SCPHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        print('Processing request with question... : ', end="")

        if self.path.__len__() < 3:
            self.path = "/?"

        question = urllib.parse.parse_qs(self.path[2:])["question"][0]

        print(question)

        model, tokenizer = m.get_model()
        status, answer = load.ask_question(question, model, tokenizer)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message

        self.wfile.write(str({"status": str(status), "answer": answer}).encode())
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), SCPHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()

