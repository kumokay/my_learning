/*
export MYSQLHOST=<cluster ip>
mysql --host=$MYSQLHOST --port=3306 --user=root --password=mypassword < setup.sql
*/

/*
setup bidding_db
*/
DROP DATABASE bidding_db
;

CREATE DATABASE bidding_db
DEFAULT CHARACTER SET utf8
COLLATE utf8_unicode_ci
;

USE bidding_db
;

CREATE TABLE bids (
  PRIMARY KEY (id)
  , id INT NOT NULL AUTO_INCREMENT
  , auction_id INT NOT NULL
  , bidder_id INT NOT NULL
  , price DECIMAL(15, 2) NOT NULL
  , bid_at DATETIME NOT NULL
  /*
  , CONSTRAINT bid_auction_id_fk
    FOREIGN KEY (auction_id) REFERENCES auctions (id)
  , CONSTRAINT bid_bidder_id_fk
    FOREIGN KEY (bidder_id) REFERENCES users (id)
  */
)
;

INSERT INTO bids (
  auction_id
  , bidder_id
  , price
  , bid_at
) VALUES
  (1, 3, 13.00, current_timestamp)
  , (1, 4, 20.00, current_timestamp + 1)
  , (1, 4, 23.00, current_timestamp + 5)
;

/*
Display result
*/
SELECT
  table_name
  , table_type
  , table_rows
  , create_time
  , update_time
FROM INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'bidding_db'
;
