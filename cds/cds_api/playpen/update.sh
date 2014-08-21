if [ $# -lt 1 ]; then
    echo "Usage: $0 NAME"
    exit 1
fi
NAME=$1

SERVER_IP="127.0.0.1"
URL="pulp/cds/${NAME}"

export DATA="{\"hostname\": \"${NAME}\", \"description\": \"Updated description\"}"

echo "Will attempt to update an item with the values:"
echo "${DATA}" | python -m json.tool

echo ""
echo "Response:"
curl -k -H "Content-Type: application/json" -X PUT -d "${DATA}" https://${SERVER_IP}/${URL}/ 
echo ""

