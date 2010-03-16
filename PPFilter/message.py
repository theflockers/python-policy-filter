import email.parser

class Message:
        
    def __init__(self, filepath):
        self.parser = email.parser.Parser()
        self.filepath = filepath
        
        fd = open(filepath)
        self.message = self.parser.parse(fd)
        fd.close()

    def get_message(self):
        return self.message
        
    def write_message(self):
        fd = open(self.filepath, 'w')
        fd.write(str(self.message))
        fd.close()
                 
