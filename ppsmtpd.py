import socket
import signal
import SocketServer
import threading
import sys
import re

class SMTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def process_message(self, mail_from, rcpts_to, message):
        pass

class SMTPRequestHandler(SocketServer.BaseRequestHandler):

    read_data = False
    helo_host = 
    mail_from = 
    rcpts_to = []
    message = 
    hostname = socket.gethostname()
    message = ''

    def handle(self):
        while True:
            try:
                if (self.read_data or self.request):
                    self.data = self.request.recv(1024)
                    if self.parse_commands():
                        pass
            except AttributeError:
                self.request.send('500 Unknown command\r\n')
            except Exception:
                pass

    def parse_commands(self):
        cmd = []
        cmd = self.data.split(' ')
        if (len(cmd) < 2):
            cmd[0] = self.data.strip()
        print len(cmd)
        method = (('self.smtp_' + cmd[0].upper().strip()) + '()')
        eval(method)

    def smtp_MAIL(self):
        self.mail_from = self.data.split(':')[1].strip()
        self.request.send('250 Ok\r\n')


    def smtp_HELO(self):
        self.helo_host = self.data.split(' ')[1].strip()
        self.request.send(('250 %s\r\n' % self.hostname))

    def smtp_QUIT(self):
        self.request.send('221 Bye\r\n')
        self.request.close()

    def smtp_DOT(self):
        response = self.server.process_message(self.mail_from, self.rcpts_to, self.message)
        if ((type(response).__name__ == 'str') and self.request.send((response + '\r\n'))):
            pass
        self.read_data = False

    def smtp_RCPT(self):
        self.rcpts_to.append(self.data.split(':')[1].strip())
        self.request.send('250 Ok\r\n')

    def smtp_DATA(self):
        self.request.send("354 Start mail input; end with '.'\r\n")
        self.read_data = True
