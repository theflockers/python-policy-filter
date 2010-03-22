import socket
import SocketServer
import threading
import sys
import re
import signal

class SMTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def process_message(self, mail_from, rcpts_to, message):
        pass

class SMTPRequestHandler(SocketServer.BaseRequestHandler):

    read_data = False
    helo_host = None
    mail_from = None
    rcpts_to = []
    message = None
    hostname = socket.gethostname()
    message = ''

    def handle(self):
        try:
            self.f_socket = self.request.makefile()
            self.send_data("220 %s PPFilter ESMTP" % (self.hostname) )
            while True:
                if self.read_data:
                    self.data = self.request.recv(4096)
                    print self.data + '*'
                    for text in self.data.split('\r\n'):
                        if text and text[0] == '.':
                            self.data = 'DOT'
                            self.parse_commands()
                        else:
                            self.message += text + "\r\n"

                else:
                    self.data = self.request.recv(1024)
                    print self.data + '*'
                    self.parse_commands()
                
        finally:
            self.request.close()
#        except AttributeError:
#            self.request.send('500 Unknown command\r\n')
#        except Exception:
#            pass

    def send_data(self, data):
        print data
        self.request.send(data + "\r\n")
        self.f_socket.flush()

    def parse_commands(self):
        cmd = []
        cmd = self.data.split(' ')
        if (len(cmd) < 2):
            cmd[0] = self.data.strip()

        method = (('self.smtp_' + cmd[0].upper().strip()) + '()')
        print method
        eval(method)

    def smtp_MAIL(self):
        self.mail_from = self.data.split(':')[1].strip()
        self.send_data('250 Ok')

    def smtp_EHLO(self):
        self.smtp_HELO()

    def smtp_HELO(self):
        self.helo_host = self.data.split(' ')[1].strip()
        self.send_data(("250 %s" % self.hostname))

    def smtp_QUIT(self):
        self.send_data('221 Bye')
        self.request.close()

    def smtp_DOT(self):
        response = self.server.process_message(self.mail_from, self.rcpts_to, self.message)
        if type(response).__name__ == 'str':
            self.send_data((response))
        else:
            self.send_data('250 Ok')
        self.read_data = False

    def smtp_RCPT(self):
        self.rcpts_to.append(self.data.split(':')[1].strip())
        self.send_data('250 Ok')

    def smtp_DATA(self):
        print 'waiting for data'
        self.send_data("354 Start mail input; end with '.'")
        self.read_data = True
