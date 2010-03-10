#!/usr/bin/env python

import PyFilter

server = PyFilter.Server
server.smtp.run(("127.0.0.1", 25), "127.0.0.1")
