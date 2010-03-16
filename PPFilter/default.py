import scanner
import socket, string
import re, os
import syslog
import spamc

#syslog.openlog('ppfilter/cfilter', syslog.LOG_PID, syslog.LOG_MAIL)

class DefaultFilter(scanner.ContentFilter):
    scanner_name = 'clamav daemon'
    
    def scan_virus(self):
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            if not os.path.exists("/var/run/clamav/clamd.ctl"):
                raise scanner.ContentFilterException('coult not open clamav socket')
                      
            s.connect("/var/run/clamav/clamd.ctl")
            s.send("CONTSCAN %s" % ( self.filepath ) )
            data = s.recv(1024)
            s.close()            
        
            if string.find(data, 'ERROR') != -1:
                syslog.syslog("clamav error: %s" % (data))
                raise scanner.ContentFilterException(data)
                
            if string.find(data, 'OK') != -1 :
                syslog.syslog("%s result: CLEAN" % (self.scanner_name))
                return 
                
            m = re.match('.*: (.*) FOUND', data)
            result = m.groups()
            print data
            if m:
                syslog.syslog("%s result: VIRUS (%s)" % (self.scanner_name, result[0]) )
                raise scanner.ContentFilterVirusException(result[0])
                
        except Exception, e:
            raise e

    def scan_spam(self):
        client = spamc.SpamdClient("/tmp/spamd.sock", self.filepath)
        client.check()
        print self.parse_spamd_response(client.get_response())
        client.close()       
        
    def parse_spamd_response(self, response):
        #m = re.match('SPAMD.* ([0-9]) (.*)', response)
        #sa = m.groups()
        
        print response
        m2 = re.match('Spam: (.*)', response)
        res = m2.groups()
        print res
           
        return (sa[0], res[0])
