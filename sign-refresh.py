#!/usr/bin/python

import hashlib
import credentials

GRANT_TYPE 	= "refresh_token"
REDIRECT_URI 	= "http://gberg.se/circux/authcode.php"
REFRESH_TOKEN	= "ENTER REFRESH TOKEN HERE"

CLIENT_SIG = hashlib.md5(credentials.CLIENT_SECRET + "client_id" + credentials.CLIENT_ID + "grant_type" + GRANT_TYPE + "redirect_uri" + REDIRECT_URI + "refresh_token" + REFRESH_TOKEN).hexdigest()
print CLIENT_SIG

