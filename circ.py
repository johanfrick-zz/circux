#!/usr/bin/python
# script for communicating with http://getcirc.com/
#
# calculate MD5 of request for signing
#import hashlib
#CLIENT_SECRET 	= "ABC"
#CLIENT_ID 	= "53a6f338e42b3971821d71b6d04e79e5"
#CODE 		= "JDJ5JDA4JGJoMnllRWQ4OS9sTDhQdEppM1czYi5XSHJPOVNMWldpckFaS2FRR3E5TkdIdmFRN3Q2OHBx"
#GRANT_TYPE 	= "authorization_code"
#REDIRECT_URI 	= "https://example.com/authcode.php"
#STATE		= "VGhlIEF2ZW5nZXJz"
#CLIENT_SIG = hashlib.md5(CLIENT_SECRET + "client_id" + CLIENT_ID + "code" + CODE + "grant_type" + GRANT_TYPE + "redirect_uri" + REDIRECT_URI + "state" + STATE).hexdigest()
#print CLIENT_SIG

import sys, getopt

def usage():
	print
	print "Usage:"
	print "   circ.py <operation> [<files>] [<dest>]"
	print
	print "Example: "
	print "   circ.py --ls photos/christmas2012 # list all files under photos/christmas2012 on Circ server"
	print
	print "Options:"
	print "   --ls List files of chosen remote directory"
	print "   --send Send local files to Circ"
	print "   --get Download remote files/folders to a local folder"
	print

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["ls=", "send=", "get="])
except getopt.GetoptError, err:
	print str(err)
	usage()
	sys.exit(2)
for option, argument in opts:
	if option == "--ls":
		print "Listing " + argument + "..."
	if option == "--send":
		print "Sending " + argument + "..."
	if option == "--get":
		print "Downloading " + argument + "..."


