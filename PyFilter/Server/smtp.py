#!/usr/bin/env python

import smtpd, asyncore
import smtplib, tempfile

class Listener(smtpd.SMTPServer):

    peer     = None
    mailfrom = None
    rcpttos  = None

    def process_message(self, peer, mailfrom, rcpttos, data):
        try:
            print rcpttos
            qFile = tempfile.NamedTemporaryFile(dir='/tmp/', prefix='tmp', delete=False)
            qFile.write(data)
            qFile.close()

            self.peer = peer
            self.mailfrom = mailfrom
            self.rcpttos = rcpttos

            self.feedBack(qFile)
        except Exception, e:
            print e

           
    def feedBack(self, qFile):
        try:
            client = smtplib.SMTP('127.0.0.1', 10025)
            client.set_debuglevel(True)
            client.sendmail(self.mailfrom, self.rcpttos, open(qFile.name).read()) 
            qFile.delete
        except Exception, e:
            print e

        return


def run(localaddr, remoteaddr):
    Listener(localaddr, remoteaddr)
    asyncore.loop()
