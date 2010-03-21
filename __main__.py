#!/usr/bin/env python

import smtplib, tempfile
from PPFilter import *
import syslog, os, sys, pwd
import ppsmtpd, socket
import threading

syslog.openlog('ppfilter', syslog.LOG_PID|syslog.LOG_NOWAIT, syslog.LOG_MAIL)

class NonRootException(Exception):
    pass

class SMTPD(ppsmtpd.SMTPServer):

    message  = None

    def process_message(self, mail_from, rcpts_to, message):
   
        self.message = message 
        filepath = None

        try:
            self.message = {'mailfrom': mail_from, 'rcpts': rcpts_to, 'data': message}
            filepath = enqueuer.enqueue(self.message)
            if filepath != None:
                sc = default.DefaultFilter(filepath)
                sc.scan()
                self.send_back(filepath)
                
        except enqueuer.QueueException, e:
            return "451 Requested action aborted: %s" % (e.message)
                       
        except scanner.ContentFilterException, e:
            return "451 Requested action aborted: %s" % (e.message)

        except scanner.ContentFilterVirusException, e:
            return        
  
        except scanner.ContentFilterSpamException, e:
            if spam_final_action == "tag":
                msg = message.Message(filepath)
                eml = msg.get_message()
                eml.add_header("X-Spam-Status", "Spam, score: %s" % (e) )
                msg.write_message()
                self.send_back(filepath)
            elif spam_final_action == "discard":
                pass
                    
    def send_back(self, filepath):
        try:
            client = smtplib.SMTP(config.reinject_address, config.reinject_port)
            #client.set_debuglevel(True)
            client.sendmail(self.message['mailfrom'], self.message['rcpts'], open(filepath).read()) 
            os.unlink(filepath)
            return 
            
        except Exception, e:
            self.push('451 '+ e.message + "\n")

def run_as_user(user):
    if os.getuid() != 0:
        raise NonRootException('this program must to be started as root')

    user_info = pwd.getpwnam(config.run_user)
    uid = user_info[2]
    os.setuid(uid)

if __name__ == "__main__":

    try:

        run_as_user(config.run_user)
        HOST, PORT = config.listen_address, config.listen_port

        syslog.syslog("starting Python Policy Filter (%s, %s)" % (HOST, PORT))
        server = SMTPD( (HOST, int(PORT)), ppsmtpd.SMTPRequestHandler)
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        ip, port = server.server_address

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
       

        #SMTPD((config.listen_address, int(config.listen_port)), None)
        #asyncore.loop()
        
    except NonRootException, e:
        print e
        syslog.closelog()
        
    except KeyboardInterrupt:
        syslog.syslog("stopping Python Policy Filter (%s, %s)" % (address, port))
        syslog.closelog()
