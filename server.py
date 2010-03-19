import threading
import socket
import time

max_threads = 10

class Server:
    
    server = None

    def __init__(self, host, port, listen_sockets, unix_socket=False):
    
        self.host           = host
        self.port           = port
        self.listen_sockets = listen_sockets
        self.unix_socket    = unix_socket 
        
    def create_socket(self):
        try:
            if not self.unix_socket:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.bind((self.host, self.port))
                self.server.listen(self.listen_sockets)
                
                print 'bunda'
                return self.server
                
        except Exception, e:
            print e            
        
class ThreadHandler(threading.Thread):
    
    rcpts = []
    
    def __init__(self):
        super(ThreadHandler, self).__init__()
        
    def run(self, s, data):
        
        self.data = data

        if self.data.find("HELO") == 0:
            command = self.data.split(' ')
            self.helo = command[1]
            s.send("220 theflockers.localdomain\r\n")
            
        elif self.data.find("MAIL") == 0:
            command = self.data.split(':')
            self.mail_from = command[1]
            s.send("250 Ok\r\n")            
                
        elif self.data.find("RCPT") == 0:
            command = self.data.split(':')
            self.rcpts.append(command[1])
            s.send("250 Ok\r\n")
            
        elif self.data.find("QUIT") == 0:
            return 
                   
        else:
            s.send("501 Unknown\r\n")
            
def main():
    
    server = Server("localhost", 2525, 100)
    s = server.create_socket()
    conn, addr = s.accept()

    conn.send("220 theflockers.localdomain ESMTP\r\n")
    while True:
        data = conn.recv(1024)
        t = ThreadHandler()
        t.run(conn, data)
            
if __name__ == "__main__":
    main()
