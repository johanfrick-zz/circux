#!/usr/bin/python

import urllib
import json
import sys
import signal
def signal_handler(signal, frame):
	print '\n Aborting...'
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

try:
	token = 'access_token=' + sys.argv[1]
except:
	print 'Usage: list_files.py <access_token>'
	sys.exit(2)

baseUrl = 'https://api.circ.io/2/'

def get(method,param=''):
	url = baseUrl + method + '?' + token
	if param != "":
		url = url + '&' + param
	result = json.load(urllib.urlopen(url))
	return result['response']

set1 = get('sets')
for entry in set1:
	files = get('sets/files','set_id=' + str(entry['id']))
	for file in files:
		print file['name']

