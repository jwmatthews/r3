#!/bin/sh

export SERVER="172.31.2.53"
if [ $# -lt 2 ]; then
    echo "Usage: $0 username password"
    exit 1
fi

export USERNAME=$1
export PASSWORD=$2

export AUTH=`python -c "import base64; print base64.encodestring(\"${USERNAME}:${PASSWORD}\")[:-1]"`

#curl -v -s -S -k -H "Authorization: Basic $AUTH" -X OPTIONS https://${SERVER}/pulp/api/v2/repositories/ 

curl -s -S -k -H "Authorization: Basic $AUTH" -X GET https://${SERVER}/pulp/api/v2/repositories/ | python -mjson.tool




