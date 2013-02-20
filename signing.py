#!/usr/bin/python
import hashlib
import sys
import common
import os
import re

REDIRECT_URI = 'http://gberg.se/circux/authcode.php'
STATE = 'VGhlIEF2ZW5nZXJz'

def main():
	if not os.path.exists(common.credentialsPath):
		print 'Generating credentials file...'
		credentials = {'CLIENT_ID': raw_input('What is your client id?'),
		               'CLIENT_SECRET': raw_input('What is your client secret?')}
		common.saveCredentials(credentials)
		menu()
	else:
		print 'Verified that credentials file exists...'
		menu()

def menu():
	credentials = common.loadCredentials()
	print 'Do you want to:'
	print '1. Generate an access token for the first time'
	print '2. Refresh your access token?'
	selected = raw_input('Select one:')
	if selected == '1':
		print 'Open the following URL in your browser and login with your Circ credentials:'
		print 'https://auth.getcirc.com/?client_id=' + credentials['CLIENT_ID'] + '&response_type=code&redirect_uri=' + REDIRECT_URI + '&state=' + STATE
		response = raw_input('Enter the full response URL here:')
		try:
			code = re.search('code=(.*?)$', response).group(1)
		except KeyError:
			print 'ERROR: No code param found in response URL'
			sys.exit(2)
		grantType = 'authorization_code'
		clientSig = hashlib.md5(credentials['CLIENT_SECRET'] + 'client_id' + credentials['CLIENT_ID'] + 'code' + code + 'grant_type' + grantType + 'redirect_uri' + REDIRECT_URI + 'state' + STATE).hexdigest()
		response = common.request('access',baseUrl='https://api.circ.io/oauth/',
			client_id=credentials['CLIENT_ID'] ,
			code=code,
			grant_type=grantType,
			redirect_uri=REDIRECT_URI,
			state=STATE,
			client_sig=clientSig)
		credentials['ACCESS_TOKEN'] = response['access_token']
		credentials['REFRESH_TOKEN'] = response['refresh_token']
		credentials['CLIENT_SIG'] = clientSig
		common.saveCredentials(credentials)
	elif selected == '2':
		grantType = 'refresh_token'
		clientSig = hashlib.md5(credentials['CLIENT_SECRET'] + 'client_id' + credentials['CLIENT_ID'] + 'grant_type' + grantType + 'redirect_uri' + REDIRECT_URI + 'refresh_token' + credentials['REFRESH_TOKEN'] ).hexdigest()
		response = common.request('access',baseUrl='https://api.circ.io/oauth/',
			client_id=credentials['CLIENT_ID'] ,
			refresh_token=credentials['REFRESH_TOKEN'] ,
			grant_type=grantType,
			redirect_uri=REDIRECT_URI,
			client_sig=clientSig)
		credentials['ACCESS_TOKEN'] = response['access_token']
		credentials['CLIENT_SIG'] = clientSig
		common.saveCredentials(credentials)
	else:
		menu()

if __name__ == '__main__':
	main()
