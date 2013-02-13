#!/usr/bin/python
# script for communicating with http://getcirc.com/
#
from __future__ import division

import getopt
import urllib
import json
import sys
import signal
import os
import datetime

def signal_handler(signal, frame):
	print '\n Aborting...'
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

try:
	token = 'access_token=' + os.environ['CIRC_ACCESS_TOKEN']
except:
	print 'Missing environment variable CIRC_ACCESS_TOKEN'
	sys.exit(2)

BASE_URL = 'https://api.circ.io/2/'

def usage():
	print
	print 'Usage:'
	print '   circ.py <operation> [<files>] [<destination>]'
	print
	print 'Example: '
	print '   circ.py --ls photos/christmas2012 # list all files under photos/christmas2012 on Circ server'
	print
	print 'Options:'
	print '   --ls List files of chosen remote directory'
	print '   --send Send local files to Circ'
	print '   --get Download remote files/folders to a local folder'
	print

def get(method,param=''):
	url = BASE_URL + method + '?' + token
	if param != '':
		url = url + '&' + param
	result = json.load(urllib.urlopen(url))
	return result['response']

def processFiles(fileOperation):
	sets = get('sets')
	for set in sets:
		files = get('sets/files','set_id=' + str(set['id']))
		for file in files:
			fileOperation(file)

def listFile(file):
	date = datetime.datetime.fromtimestamp(file['date_time_taken']).strftime('%Y-%m-%d %H:%M:%S')
	print file['name'] + ' (' + picSize(file['size']) + ', ' + date + ')'

def downloadFile(file):
	url = file['media_url'] + '&size=0'
	u = urllib.urlopen(url)
	localFile = open(file['name'], 'w')
	localFile.write(u.read())
	localFile.close()
	print 'Saved: ' + file['name']
	sys.exit(0)

def picSize(size):
	res = size['width']*size['height']/1000000
	return '%.2f%s' % (res, 'MP')

try:
	opts, args = getopt.getopt(sys.argv[1:], '', ['ls=', 'send=', 'get='])
except getopt.GetoptError, err:
	print str(err)
	usage()
	sys.exit(2)

if not opts:
	usage()
	sys.exit(2)

for option, argument in opts:
	if option == '--ls':
		print 'Listing ' + argument + '...'
		processFiles(listFile)
	if option == '--send':
		print 'Sending ' + argument + '...'
	if option == '--get':
		print 'Downloading ' + argument + '...'
		processFiles(downloadFile)



