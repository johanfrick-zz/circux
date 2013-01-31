#!/bin/bash
# Bash script for communicating with http://getcirc.com/

if [ $# -lt 2 ]
then
	echo
	echo "Usage:"
	echo "   circ.sh <operation> [<files>] [<dest>]"
	echo
	echo "Example: "
	echo "   circ.sh --ls photos/christmas2012 # list all files under photos/christmas2012 on Circ server"
	echo
	echo "Options:"
	echo "   --ls List files of chosen remote directory"
	echo "   --send Send local files to Circ"
	echo "   --get Download remote files/folders to a local folder"
	echo
else
	OP=$1
# TODO: Check params like in the following example: https://github.com/andreafabrizi/Dropbox-Uploader/blob/master/dropbox_uploader.sh
	OPTIONS="$2 $3 $4 $5 $6 $7" #Allow for more options in the future
	LS=`echo $OP| grep "\--ls"`
	SEND=`echo $OP| grep "\--send"`
	GET=`echo $OP| grep "\--get"`
	if [ -n "$LS" ]
	then
		echo "Listing files..."
	elif [ -n "$SEND" ]
	then
		echo "Sending files..."
	elif [ -n "$GET" ]
	then
		echo "Downloading files..."
	fi
fi

