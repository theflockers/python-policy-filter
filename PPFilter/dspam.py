import smtplib
import scanner
import socket, string
import re, os
import syslog

class DSPAMContentFilter(scanner.ContentFilter):
    # we do not need virus check trough ppfilter. DSPAM does it for you.
    def scan_virus(self):
        pass
        
    # to-do
    def scan_spam(self):
        pass

