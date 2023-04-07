#!/bin/bash

app_ip=127.0.0.1
test_name="all"

if [ $# != 1 ] && [ $# != 2 ]; then
    echo "usage: $0 <app_ip> [test_name]"
    exit 1
else
    app_ip=$1
    if [ $# = 2 ]; then
        test_name=$2
    fi
fi


function create_auction() {
    # curl http://${app_ip}:8080/create_auction/orange/3/5.2/
    curl -d '{"auction_name":"orange", "seller_id":3, "price":5.2}' \
    -H "Content-Type: application/json" \
    -X POST http://${app_ip}:8080/create_auction/
}

function get_auctions() {
    curl http://${app_ip}:8080/get_auctions/0/100/ | json_pp
}

function place_bid() {
    # curl http://${app_ip}:8080/place_bid/1/3/999.99/ 
    curl -d '{"auction_id":1, "bidder_id":3, "price":999.99}' \
    -H "Content-Type: application/json" \
    http://${app_ip}:8080/place_bid/
}

function get_bid_history() {
    curl http://${app_ip}:8080/get_bid_history/1/0/100/ | json_pp
}

function get_highest_bid() {
    curl http://${app_ip}:8080/get_highest_bid/1/ | json_pp
}

function test_get_credit_card() {
    curl http://${app_ip}:8080/test_get_credit_card/1/ | json_pp
}

function test_payment_complete() {
    curl -d '{"payment_id":1}' \
    -H "Content-Type: application/json" \
    http://${app_ip}:8080/test_payment_complete/
}

function test_process_payment() {
    curl -d '{"payment_id": 10, "card_holder_name": "user10-real-name", "card_number": "000000001111-10", "price": 23}' \
    -H "Content-Type: application/json" \
    http://${app_ip}:8080/test_process_payment/
}

declare -a testcases=(
    # public urls
    create_auction
    get_auctions
    place_bid
    get_bid_history
    get_highest_bid
    # test only urls
    test_get_credit_card
    test_payment_complete
    test_process_payment
)

function print_test_header() {
    echo ""
    echo "****************************************"
    echo "* " $1
    echo "****************************************"
    echo ""
}

case ${test_name} in

  all)
    for testcase in ${testcases[@]}; do
        print_test_header ${testcase}
        ${testcase}
    done 
    ;;

  *)
    print_test_header ${test_name}
    ${test_name}
    ;;
esac