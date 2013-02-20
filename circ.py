#!/usr/bin/python
# script for communicating with http://getcirc.com/
#
from __future__ import division

import getopt
import hashlib
import requests
import urllib
import sys
import signal
import os
import datetime
import common

credentials = common.loadCredentials()

def main():
	signal.signal(signal.SIGINT, signal_handler)
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

def signal_handler(signal, frame):
	print '\n Aborting...'
	sys.exit(0)

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

def requestWithToken(method, baseUrl='https://api.circ.io/2/', **param):
	try:
		param['access_token'] = credentials['ACCESS_TOKEN']
	except:
		print 'Missing ACCESS_TOKEN in ' + common.CREDENTIALS_FILE
		sys.exit(2)
	result = common.request(method, baseUrl, **param)
	try:
		return result['response']
	except KeyError:
		print result
		sys.exit(2)

def ignoreTrash(set):
	return set['type'] != 6

def getSets():
	return filter(ignoreTrash, requestWithToken('sets'))

def processSets(setOperation, fileOperation):
	for set in getSets():
		setOperation(set, fileOperation)

def processFiles(set, fileOperation):
	files = requestWithToken('sets/files', set_id= set['id'])
	for file in files:
		fileOperation(file)

def deleteSets():
	for set in getSets():
		requestWithToken('sets/delete', set_id=set['id'],generation_id=set['generation_id'])

def deleteFiles():
	fileIds = ''
	print 'Getting file ids...'
	for set in getSets():
		files = requestWithToken('sets/files', set_id=set['id'])
		print 'Found ' + str(len(files)) + ' files in set: ' + str(set['id'])
		for file in files:
			fileIds += str(file['id'])   + ','
	if fileIds != '':
		print 'Starting delete...'
		requestWithToken('files/delete', file_id=fileIds)
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

def upload(filePath, fileName):
	uploadUrl = 'http://bulk-api.circ.io/2/upload/'
	md5Hash = hashlib.md5(open(filePath, "r").read()).hexdigest()
	result = requestWithToken('query', baseUrl=uploadUrl, file_name=fileName, file_size=os.path.getsize(filePath), upload_signature=md5Hash, client_sig=credentials['CLIENT_SIG'])
	print result
	url = uploadUrl + 'chunk' + '?access_token=' + credentials['ACCESS_TOKEN']
	url = url + '&file_id=' + str(result['file_id']) + '&offset=0'
	requests.post(url, files={fileName: open(filePath, 'rb')})
	print 'Uploaded chunk'
	result = requestWithToken('finish', baseUrl=uploadUrl, file_id=result['file_id'], integrity_digest=md5Hash)
	print result


def uploadDir(dir):
	for currentDir, subDirs, files in os.walk(dir):
		for fileName in files:
			upload(os.path.join(currentDir, fileName), fileName)

if __name__ == '__main__':
	main()
