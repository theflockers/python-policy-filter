import socket

class ContentFilterException(Exception):
    pass

class ContentFilterVirusException(Exception):
    pass

class ContentFilter():

    filepath = None
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def scan(self):
        self.scan_virus()
        self.scan_spam()
        self.scan_custom()
    
    def scan_virus(self):
        pass    
    
    def scan_spam(self):
        pass
        
    def scan_custom(self):
        pass
