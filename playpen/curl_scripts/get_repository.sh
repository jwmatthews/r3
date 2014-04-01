#!/bin/sh

export SERVER="172.31.2.53"
if [ $# -lt 3 ]; then
    echo "Usage: $0 username password repo_id"
    exit 1
fi

export USERNAME=$1
export PASSWORD=$2
export REPO_ID=$3

export AUTH=`python -c "import base64; print base64.encodestring(\"${USERNAME}:${PASSWORD}\")[:-1]"`

#curl -v -s -S -k -H "Authorization: Basic $AUTH" -X OPTIONS https://${SERVER}/pulp/api/v2/repositories/ 

curl -s -S -k -H "Authorization: Basic $AUTH" -X GET https://${SERVER}/pulp/api/v2/repositories/${REPO_ID}/ | python -mjson.tool




