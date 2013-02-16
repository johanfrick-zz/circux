#!/usr/bin/python
# script for communicating with http://getcirc.com/
#
from __future__ import division

import getopt
import hashlib
import requests
import urllib
import json
import sys
import signal
import os
import datetime
import credentials

def signal_handler(signal, frame):
	print '\n Aborting...'
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

try:
	token = 'access_token=' + credentials.ACCESS_TOKEN
except:
	print 'Missing ACCESS_TOKEN in credentials.py'
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
	try:
		return result['response']
	except KeyError:
		print result

def ignoreTrash(set):
	return set['type'] != 6

def getSets():
	return filter(ignoreTrash, get('sets'))


def processSets(setOperation, fileOperation):
	for set in getSets():
		setOperation(set, fileOperation)

def processFiles(set, fileOperation):
	files = get('sets/files', 'set_id=' + str(set['id']))
	for file in files:
		fileOperation(file)

def deleteSets():
	for set in getSets():
		get('sets/delete', 'set_id=' + str(set['id']) + "&" + 'generation_id=' + str(set['generation_id']))

def deleteFiles():
	fileIds = ''
	print 'Getting file ids...'
	for set in getSets():
		files = get('sets/files', 'set_id=' + str(set['id']))
		print 'Found ' + str(len(files)) + ' files in set: ' + str(set['id'])
		for file in files:
			fileIds += str(file['id'])   + ','
	if fileIds != '':
		print 'Starting delete...'
		get('files/delete', 'file_id=' + fileIds)
		print 'All deleted.'
	else:
		print 'Nothing to delete.'


def listFile(file):
	date = datetime.datetime.fromtimestamp(file['date_time_taken']).strftime('%Y-%m-%d %H:%M:%S')
	print file['name'] + ' (' + picSize(file['size']) + ', ' + date + ')'
	print file

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

def upload(file):
	open(file, "r").read()
	md5Hash = hashlib.md5(open(file, "r").read()).hexdigest()
	print md5Hash
	result = get('upload/query', 'file_name=' + file + '&file_size=' + str(os.path.getsize(file)) + '&upload_signature=' +
	                             str(md5Hash))
	print result
	url = BASE_URL + 'upload/chunk' + '?' + token
	url = url + '&file_id=' + str(result['file_id']) + '&offset=0'
	requests.post(url, files={file: open(file, 'rb')})
	print 'Uploaded chunk'
	result = get('upload/finish', 'file_id=' + str(result['file_id']) + '&integrity_digest=' + str(md5Hash))
	print result


def uploadDir(dir):
	for currentDir, subDirs, files in os.walk(dir):
		for file in files:
			upload(os.path.join(currentDir, file))

try:
	opts, args = getopt.getopt(sys.argv[1:], '', ['ls=', 'send=', 'get=', 'delete-all='])
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
		processSets(processFiles, listFile)
	if option == '--send':
		print 'Sending ' + argument + '...'
		uploadDir(argument)
	if option == '--get':
		print 'Downloading ' + argument + '...'
		processSets(processFiles, downloadFile)
	if option == '--delete-all':
		print 'Deleting all ...'
#		deleteSets()
		deleteFiles()