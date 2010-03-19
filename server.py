import socket
import SocketServer
import threading
import sys

class SMTPRequestHandler(SocketServer.BaseRequestHandler):

    read_data = False

    def handle(self):
        
        # run forever
        while True:
            if not self.read_data: 
                if self.request:
                    self.data = self.request.recv(1024)
                try:
                    self.parse_commands()
                except AttributeError:
                    self.request.send("500 Unknown command\r\n")

    def parse_commands(self):

        cmd = []
        cmd = self.data.split(' ')
        if len(cmd) < 2:
            cmd[0] = self.data.strip()

        print len(cmd)
        method = "self.smtp_"+ cmd[0].upper().strip() + '()'
        print method
        eval(method)
    
    def smtp_MAIL(self):
        self.request.send("220 Ok\r\n")

    def smtp_HELO(self):
        self.request.send("220 Ok\r\n")

    def smtp_QUIT(self):
        self.request.send("220 Bye\r\n")
        self.request.close()

    def smtp_DOT(self):
        self.request.send("250 Ok\r\n")

    def smtp_DATA(self):
        self.request.send("354 Start mail input; end with '.'\r\n")
        self.read_data = True
        self.data = self.request.recv(1024)
        self.read_data = False
        print self.data
        

class SMTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

HOST, PORT = 'localhost', 2525

server = SMTPServer( (HOST, PORT), SMTPRequestHandler)
ip, port = server.server_address

server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
