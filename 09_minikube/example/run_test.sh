#!/bin/bash

app_ip=127.0.0.1

if [ $# != 1 ]; then
    echo "usage: $0 [<app_ip>]"
    exit 1
else
    app_ip=$1
fi


echo ""
echo "****************************************"
echo "* list_product"
echo "****************************************"
echo ""
# curl http://${app_ip}:8080/list_product/orange/3/5.2/
curl -d '{"product_name":"orange", "seller_id":3, "price":5.2}' \
-H "Content-Type: application/json" \
-X POST http://${app_ip}:8080/list_product/

echo ""
echo "****************************************"
echo "* get_catalogue"
echo "****************************************"
echo ""
curl http://${app_ip}:8080/get_catalogue/0/100/ | json_pp

echo ""
echo "****************************************"
echo "* place_bid"
echo "****************************************"
echo ""
# curl http://${app_ip}:8080/place_bid/1/3/999.99/ 
curl -d '{"product_id":1, "bidder_id":3, "price":999.99}' \
-H "Content-Type: application/json" \
http://${app_ip}:8080/place_bid/

echo ""
echo "****************************************"
echo "* get_bid_history"
echo "****************************************"
echo ""
curl http://${app_ip}:8080/get_bid_history/1/0/100/ | json_pp

echo ""
echo "****************************************"
echo "* get_winner"
echo "****************************************"
echo ""
curl http://${app_ip}:8080/get_winner/1/ | json_pp
