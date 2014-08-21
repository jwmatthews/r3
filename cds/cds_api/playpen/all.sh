SERVER_IP="127.0.0.1"
URL="pulp/cds/"

echo ""
echo "Response:"
curl -s -k -X GET https://${SERVER_IP}/${URL}/ | python -m json.tool 
echo ""

