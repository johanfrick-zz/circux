#!/usr/bin/python
# script for communicating with http://getcirc.com/
import sys, getopt

def usage():
	print
	print "Usage:"
	print "   circ <operation> [<files>] [<dest>]"
	print
	print "Example: "
	print "   circ --ls photos/christmas2012 # list all files under photos/christmas2012 on Circ server"
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


