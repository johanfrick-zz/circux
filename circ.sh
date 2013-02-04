#!/bin/bash
# Bash script for communicating with http://getcirc.com/

# calculate MD5 of request for signing
#CLIENT_SECRET="ABC"
#CLIENT_ID="53a6f338e42b3971821d71b6d04e79e5"
#CODE="JDJ5JDA4JGJoMnllRWQ4OS9sTDhQdEppM1czYi5XSHJPOVNMWldpckFaS2FRR3E5TkdIdmFRN3Q2OHBx"
#GRANT_TYPE="authorization_code"
#REDIRECT_URI="https://example.com/authcode.php"
#STATE="VGhlIEF2ZW5nZXJz"
#CLIENT_SIG=`echo -n $CLIENT_SECRET"client_id"$CLIENT_ID"code"$CODE"grant_type"$GRANT_TYPE"redirect_uri"$REDIRECT_URI"state"$STATE | md5sum | awk '{ print $1 }'`
#echo $CLIENT_SIG


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

