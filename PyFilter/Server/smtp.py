#!/usr/bin/env python

import smtpd

def run(localaddr, remoteaddr ):
    server = smtpd.SMTPServer(localaddr, remoteaddr)  
