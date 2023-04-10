#!/bin/bash

app_ip=`kubectl get services | grep webapp | awk '{ print $4 }'`
test_name="all"

if [ $# -ne 0 ] && [ $# -gt 1 ]; then
    echo "usage: $0 [test_name]"
    exit 1
elif [ $# = 1 ]; then
    test_name=$1
fi

curlcmd="curl --silent"

function create_auction() {
    ${curlcmd} -d '{"auction_name":"orange", "seller_id":3, "price":5.2}' \
    -H "Content-Type: application/json" \
    -X POST http://${app_ip}:8080/create_auction/
}

function get_auctions() {
    echo "=== ongoing auctions ==="
    ${curlcmd} http://${app_ip}:8080/get_auctions/0/ongoing/100/ | json_pp

    echo "=== ended auctions ==="
    ${curlcmd} http://${app_ip}:8080/get_auctions/0/ended/100/ | json_pp
}

function place_bid() {
    ${curlcmd} -d '{"auction_id":1, "bidder_id":3, "price":999.99}' \
    -H "Content-Type: application/json" \
    http://${app_ip}:8080/place_bid/
}

function get_bid_history() {
    ${curlcmd} http://${app_ip}:8080/get_bid_history/1/0/100/ | json_pp
}

function get_highest_bid() {
    ${curlcmd} http://${app_ip}:8080/get_highest_bid/1/ | json_pp
}

function test_get_credit_card() {
    ${curlcmd} http://${app_ip}:8080/test_get_credit_card/1/ | json_pp
}

function test_payment_complete() {
    ${curlcmd} -d '{"payment_id":1}' \
    -H "Content-Type: application/json" \
    http://${app_ip}:8080/test_payment_complete/
}

function test_process_payment() {
    json_input='
        {"payment_id": 10, "card_holder_name": "user10-real-name",
        "card_number": "000000001111-10", "price": 23}
    '
    ${curlcmd} -d "${json_input}" \
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