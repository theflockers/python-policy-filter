import socket, os

class SpamdClientException(Exception):
    pass

class SpamdClient():

    def __init__(self, sockpath, filepath):
        self.sockpath = sockpath
        self.filepath = filepath
        self.user     = 'clamav'
        
        self.prepare()
        self.connect()
        
    def connect(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if not os.path.exists(self.sockpath):
            raise SpamdClientException('could not connect do spamd')
        
        s.connect(self.sockpath)        
        self.sock = s        
        
    def prepare(self):
        f = open(self.filepath)
        self.message = f.read()
        self.content_len = len(self.message) + 2

    def send_data(self, msg):
        self.sock.send("%s\r\n" % (msg))

    def check(self): 
        self.send_data("CHECK SPAMC/1.4")
        self.send_data("Content-length: %i" % (int(self.content_len)))
        self.send_data("User: %s" % (self.user))
        self.send_data("\r\n%s\r\n" % (self.message))
        
        data = self.sock.recv(1024)
        while 1:
            line = self.sock.recv(1024)
            if len(line) == 0: break
            
            data += line
        
        self.response = data.strip()
        
    def get_response(self):
        return self.response

    def close(self):
        self.sock.close()
