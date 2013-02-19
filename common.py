#!/usr/bin/python

import json
import os
import urllib

CREDENTIALS_FILE = 'credentials.json'
credentialsPath = os.path.join(os.getcwd(), CREDENTIALS_FILE)

def request(method, baseUrl, **param):
	url = baseUrl + method + '?' + urllib.urlencode(param)
	return json.load(urllib.urlopen(url))

def saveCredentials(dict):
	with open(credentialsPath, 'wb') as fp:
		json.dump(dict, fp)

def loadCredentials():
	with open(credentialsPath, 'rb') as fp:
		return json.load(fp)
