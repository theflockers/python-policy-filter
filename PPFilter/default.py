import scanner
import socket, string
import re, os
import syslog
import spamc
import config
#syslog.openlog('ppfilter/cfilter', syslog.LOG_PID, syslog.LOG_MAIL)

class DefaultFilter(scanner.ContentFilter):
    scanner_name = 'clamav daemon'
    
    def scan_virus(self):
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            if not os.path.exists(config.clamd_socket_path):
                raise scanner.ContentFilterException('coult not open clamav socket')
                      
            s.connect(config.clamd_socket_path)
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
        client = spamc.SpamdClient(config.spamd_socket_path, self.filepath)
        client.check()
        if self.parse_spamd_response(client.get_response())['result']:
            client.close()
            raise scanner.ContentFilterSpamException(self.parse_spamd_response(client.get_response())['score'])
                        
        client.close()       
        
    def parse_spamd_response(self, response):
        #m = re.match('SPAMD.* ([0-9]) (.*)', response)
        #sa = m.groups()

        lines = response.split("\r\n")
        for line in lines:
            if len(line) != 0:
                m = re.match('Spam: (.*) ; (.*)', line)
                if m != None:
                    print m
                    sa = {'result': eval(m.group(1)), 'score': m.group(2)}
                    return sa
