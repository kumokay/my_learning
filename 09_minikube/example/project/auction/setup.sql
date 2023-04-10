/*
export MYSQLHOST=<cluster ip>
mysql --host=$MYSQLHOST --port=3306 --user=root --password=mypassword < setup.sql
*/

/*
setup auction_db
*/
DROP DATABASE auction_db
;

CREATE DATABASE auction_db
DEFAULT CHARACTER SET utf8
COLLATE utf8_unicode_ci
;

USE auction_db
;

CREATE TABLE auctions (
  PRIMARY KEY (id)
  , id INT NOT NULL AUTO_INCREMENT
  , name VARCHAR(255) NOT NULL
  , start_price DECIMAL(15, 2) NOT NULL
  , seller_id INT NOT NULL
  , start_at DATETIME NOT NULL
  , end_at DATETIME NOT NULL
  , status ENUM ('created','ongoing','ended') NOT NULL
)
;

INSERT INTO auctions (
  name
  , start_price
  , seller_id
  , start_at
  , end_at
  , status
) VALUES
  ('prod1_from_user1', 3.99, 1, current_timestamp - 300, current_timestamp, 'ended')
  , ('prod2_from_user1', 2.99, 1, current_timestamp - 200, current_timestamp, 'ended')
  , ('prod3_from_user1', 4.99, 1, current_timestamp - 100, current_timestamp, 'ended')
  , ('prod4_from_user2', 399.99, 2, current_timestamp + 10, current_timestamp + 320, 'ongoing')
  , ('prod5_from_user3', 10.99, 3, current_timestamp, current_timestamp + 450, 'ongoing')
  , ('prod6_from_user3', 123.45, 3, current_timestamp + 100, current_timestamp + 580, 'ongoing')
;

CREATE TABLE payments (
  PRIMARY KEY (id)
  , id INT NOT NULL AUTO_INCREMENT
  , bid_id INT NOT NULL
  , auction_id INT NOT NULL
  , user_id INT NOT NULL
  , price DECIMAL(15, 2) NOT NULL
  , created_at DATETIME NOT NULL
  , status ENUM ('pending', 'completed')
)
;

INSERT INTO payments (
  bid_id
  , auction_id
  , user_id
  , price
  , created_at
  , status
) VALUES
  (3, 1, 2, 3.99, current_timestamp, 'pending')
  , (4, 2, 2, 2.99, current_timestamp, 'pending')
  , (5, 3, 3, 4.99, current_timestamp, 'pending')
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
WHERE table_schema = 'auction_db'
;