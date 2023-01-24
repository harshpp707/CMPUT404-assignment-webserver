#  coding: utf-8 
import socketserver
import os
from sys import path
# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Harsh Patel
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
# some of the code is Copyright Â© 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # decode from binary
        self.data = self.data.decode("utf-8")  
        # make array from spaces
        self.data = self.data.split(" ") 
        if self.data[0] == 'GET':
            self.get_method()
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8'))
    
    def get_method(self):
        print(self.data[1])
        #checking the last char
        if self.data[1][-1] == '/':
            self.send_all_data('./www'+self.data[1]+'/index.html',"text/html")
            # print("HERE")

        #checking the last 3 char
        elif self.data[1][-3:] == 'css':
            self.send_all_data('./www'+self.data[1], "text/css")

        #checking last 4 char
        elif self.data[1][-4:] == 'html':
            self.send_all_data('./www'+self.data[1], "text/html")

        #moved to different location
        else:
            self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\n" + "Location: " + \
                self.data[1] + "/\r\n", 'utf-8'))
            
    def send_all_data(self,path,content_type):
        try:
            f= open(path)
            content = f.read()
            f.close()
            headers = "HTTP/1.1 200 OK\n" + "Content-Type: " + content_type + "\n" +  "Content-Length: " + str(len(content)) + "\r\n\r\n"
            self.request.send(headers.encode())
            self.request.send(content.encode())
            # self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n" + "\r\n" + "Content-Type: " + content_type + "\r\n" +  "Content-Length: " + str(len(content)) + "\r\n " + content + "\r\n\r\n", 'utf-8'))
        except:
            # print(e)
            message = "HTTP/1.1 404 Not Found\r\n"
            self.request.sendall(bytearray(message, 'utf-8'))
        
        


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
