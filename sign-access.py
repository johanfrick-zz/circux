#!/usr/bin/python

import hashlib
import credentials

CODE 		= "ENTER CODE HERE"
GRANT_TYPE 	= "authorization_code"
REDIRECT_URI 	= "http://gberg.se/circux/authcode.php"
STATE		= "VGhlIEF2ZW5nZXJz"

CLIENT_SIG = hashlib.md5(credentials.CLIENT_SECRET + "client_id" + credentials.CLIENT_ID + "code" + CODE + "grant_type" + GRANT_TYPE + "redirect_uri" + REDIRECT_URI + "state" + STATE).hexdigest()

print CLIENT_SIG

