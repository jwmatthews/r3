if [ $# -lt 1 ]; then
    echo "Usage: $0 NAME"
    exit 1
fi
NAME=$1
SERVER_IP="127.0.0.1"
URL="pulp/cds/${NAME}"

echo ""
echo "Response:"
curl -k -X DELETE https://${SERVER_IP}/${URL}/ 
echo ""

