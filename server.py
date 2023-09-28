#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Directory path of current file
dir_path = os.path.dirname(os.path.realpath(__file__))

# Dictionary storing MIME types
mimes = {".html": "text/html", ".css": "text/css"}

class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):  # sourcery skip: use-fstring-for-concatenation, use-next
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

        # Break data into the method, requested path, and the rest
        data = self.data.decode('utf-8').split('\r\n')
        method, initial_path, _ = data[0].split()
        path = ""
        
        # Figure out content type
        content_type = ""
        for content, mime in mimes.items():
            if content in initial_path:
                content_type = mime
                break
            
        # If not a GET request
        if (method != "GET"):
            # If not a GET request send 405 status
            send = "HTTP/1.1 405 Not FOUND!\r\n"
            self.request.sendall(send.encode('utf-8'))
        # If it is a GET request
        else:
            # Check if path doesn't contain "index.html" or "css"
            if all(
                substring not in initial_path
                for substring in ("index.html", "css")
            ):
                if (initial_path.endswith("/")):
                    # If path ends with a forward slash, redirect to same path with index.html appended
                    initial_path += "index.html"
                else:
                    # Send 301 status with new location
                    send = "HTTP/1.1 301 Moved Permanently\r\nLocation:" + initial_path + "/\r\n301 Moved Permanently"
                    # print(send)
                    self.request.sendall(send.encode('utf-8'))
            path = "./www" + initial_path

        # Check if file exists
        if (os.path.exists(path)):
            with open(path, 'r') as file:
                data = file.read()
            # Response with 200 status and file contents
            send = 'HTTP/1.1 200 OK\r\n'+"Content-Type:" + content_type +"\r\n\r\n" + data # Blank between HTTP heads and body
        else:
            # If not existent, send 404 status
            send = "HTTP/1.1 404 Not Found\r\n404 Not Found"
            
        self.request.sendall(send.encode('utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
