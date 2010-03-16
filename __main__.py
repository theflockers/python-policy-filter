#!/usr/bin/env python

import smtpd, asyncore, asynchat
import smtplib, tempfile
from PPFilter import *
import syslog, os, sys, pwd

address = '127.0.0.1'
port = 2525
run_user = 'clamav'
spam_final = 'tag'

syslog.openlog('ppfilter', syslog.LOG_PID|syslog.LOG_NOWAIT, syslog.LOG_MAIL)

class NonRootException(Exception):
    pass

class SMTPD(smtpd.SMTPServer):

    message  = None

    def process_message(self, peer, mailfrom, rcpttos, data):
    
        filepath = None

        try:
            syslog.syslog("connect from peer: %s" % (peer[0]) )
            self.message = {'peer': peer, 'mailfrom': mailfrom, 'rcpts': rcpttos, 'data': data}
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
            msg = message.Message(filepath)
            eml = msg.get_message()
            eml.add_header("X-Spam-Status", "Spam, score: %s" % (e) )
            msg.write_message()
            self.send_back(filepath)
                    
    def send_back(self, filepath):
        try:
            client = smtplib.SMTP('127.0.0.1', 10025)
            #client.set_debuglevel(True)
            client.sendmail(self.message['mailfrom'], self.message['rcpts'], open(filepath).read()) 
            os.unlink(filepath)
            return 
            
        except Exception, e:
            self.push('451 '+ e.message + "\n")

def run_as_user(user):
    if os.getuid() != 0:
        raise NonRootException('this program must to be started as root')

    user_info = pwd.getpwnam(run_user)
    uid = user_info[2]
    os.setuid(uid)

if __name__ == "__main__":

    try:
        run_as_user(run_user)
        syslog.syslog("starting Python Policy Filter (%s, %s)" % (address, port))
        SMTPD((address, port), None)
        asyncore.loop()
        
    except NonRootException, e:
        print e
        syslog.closelog()
        
    except KeyboardInterrupt:
        syslog.syslog("stopping Python Policy Filter (%s, %s)" % (address, port))
        syslog.closelog()
