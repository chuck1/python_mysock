#!/usr/bin/env python
# This is a simple port-forward / proxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license
import socket
import select
import time
import sys

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001

class Client(object):
    input_list = []

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
        except Exception, e:
            print e

    def send(self, data):
        self.sock.send(data)

    def sendrecv(self, data):
        self.send(data)
        return self.recv()

    def on_close(self):
        self.sock.close()

    def recv(self):
        return self.sock.recv(buffer_size)

class Server(object):
    input_list = []

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

        #print "listening"

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

    def on_accept(self):
        clientsock, clientaddr = self.server.accept()
            
        #print clientaddr, "has connected"
        self.input_list.append(clientsock)

    def on_close(self):
        #print self.s.getpeername(), "has disconnected"
        #remove objects from input_list
        self.input_list.remove(self.s)

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
	print "data"
	print repr(data)
        
        # echo
        self.s.send(data)

if __name__ == '__main__':

    if sys.argv[1] == "S":

        server = Server('', 8000)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)

    elif sys.argv[1] == "C":

        client = Client()
        client.connect("localhost",8000)

        client.send("hello")

        client.recv()








