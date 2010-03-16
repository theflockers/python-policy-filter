import os, tempfile

tempdir = "/tmp/ppf"

class QueueException(Exception):
    pass

class Preamble:
 
    peer = None
    mailfrom = None
    rcpts = None
       
    def __init__(self, message):
        self.peer     = message['peer']
        self.mailfrom = message['mailfrom']
        self.rcpts    = message['rcpts']
        
    def write(self):
        preamble  = "RP: %s\t\tADDRESS: %s\n" % (self.mailfrom, self.peer[0])
        for rcpt in self.rcpts:
            preamble += "DST: %s\n" % (rcpt)
            
        return preamble

def enqueue(message):

    data = message['data']
         
    try:
        qFile = tempfile.NamedTemporaryFile(dir=tempdir, prefix='q', suffix='.tmp', delete=False)
        qFile.write(data)
        qFile.close()
        
        return qFile.name
        
    except Exception, e:
        raise QueueException(e)
