#!/usr/bin/env python

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('ppfilter.ini')

listen_address    = config.get('filter','listen_address')
listen_port       = config.get('filter','listen_port')
run_user          = config.get('filter','run_user')
spam_final_action = config.get('filter','spam_final_action')
reinject_address  = config.get('filter','reinject_address')
reinject_port     = config.get('filter','reinject_port')
temp_directory    = config.get('filter','temp_directory')
spamd_socket_path = config.get('filter','spamd_socket_path')
clamd_socket_path = config.get('filter','clamd_socket_path')
