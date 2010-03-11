#!/usr/bin/env python

import PyFilter

server = PyFilter.Server
server.smtp.run(("127.0.0.1", 2525), "127.0.0.1")
