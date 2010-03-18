import SocketServer, re, sys, threading

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
    
        self.data = self.request.recv(1024)
        self.rcpts = []

        m = re.match('(\w+).?(\w+).?(.+)?', self.data)
        
        print m.groups()
        if m:
            if m.group(1) == "HELO":
                self.helo_host = m.group(2)
                self.request.send("220 localhost\r\n")
             
            if m.group(1) == "MAIL":
                self.mail_from = m.group(2)
                self.request.send("250 Ok\r\n")            
                
            if m.group(1) == "RCPT":
                self.rcpts.append(m.group(2))
                self.request.send("250 Ok\r\n")
                
            if m.group(1) == "DATA": 
                self.request.send("354 Enter mail, end with \".\" on a line by itself\r\n")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 2525

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    #server_thread.setDaemon(True)
    server_thread.start()
