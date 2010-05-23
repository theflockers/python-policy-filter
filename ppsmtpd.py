"""
 PPFilter simple smtpd server handler
 @author Leandro Mendes
 @copyright Leandro Mendes <theflockers@gmail.com> 
"""
import socket
import SocketServer
import threading
import sys, time, errno
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
            self.rcpts_to = []
            while True:
                if self.read_data:
                    self.data = self.request.recv(4096)
                    if len(self.data) == 0:
                        self.request.close()

                    for text in self.data.split('\r\n'):
                        print ">", text, "<"
                        if text and text.strip() == '.':
                            self.data = 'DOT'
                            self.parse_commands()
                            return
                        else:
                            self.message += text + "\r\n"

                else:
                    self.data = self.request.recv(1024)
                    print threading.currentThread()
                    if len(self.data) != 0:
                         print self.data
                         self.parse_commands()

        except IOError, e:
            if e.errno == errno.EPIPE
            return

        except AttributeError:
            self.request.send('500 Unknown command\r\n')
            self.request.close()

        finally:
            print "Finish"
            self.request.close()
            self.f_socket.close()

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

    def smtp_RSET(self):
        self.mail_from = None
        self.rcpts_to = []
        self.message = ''
        self.send_data('250 Ok')

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
