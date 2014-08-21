export SERVER_IP="127.0.0.1"
export PORT="443"
URL="/pulp/cds/"

if [ $# -lt 1 ]; then
    echo "Usage: $0 NAME"
    exit 1
fi
HOSTNAME=$1

export DATA="{\"hostname\": \"${HOSTNAME}\"}"

echo "Will attempt to create n cds with the values:"
echo "${DATA}" | python -m json.tool

echo ""
echo "Response:"
curl -k -H "Content-Type: application/json" -X POST -d "${DATA}" https://${SERVER_IP}:${PORT}/${URL}/ 
echo ""

