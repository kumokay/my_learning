/*
export MYSQLHOST=<cluster ip>
mysql --host=$MYSQLHOST --port=3306 --user=root --password=mypassword < setup.sql
*/

/*
setup payment_db
*/
DROP DATABASE payment_db
;

CREATE DATABASE payment_db
DEFAULT CHARACTER SET utf8
COLLATE utf8_unicode_ci
;

USE payment_db
;

CREATE TABLE transactions (
  PRIMARY KEY (id)
  , id INT NOT NULL AUTO_INCREMENT
  , payment_id INT NOT NULL
  , card_holder_name VARCHAR(32) NOT NULL
  , card_number VARCHAR(16) NOT NULL
  , price DECIMAL(15, 2) NOT NULL
  , third_party_transaction_id VARCHAR(32) NOT NULL
  , initiated_at DATETIME NOT NULL
  , status ENUM ('initiating', 'processing', 'aborted', 'completed')
)
;

INSERT INTO transactions (
  payment_id
  , card_holder_name
  , card_number
  , price
  , third_party_transaction_id
  , initiated_at
  , status
) VALUES
  (1, "user2-real-name", "000000002222-2", 11.00, "transaction-1", current_timestamp - 100, 'processing')
  , (2, "user2-real-name", "000000002222-2", 22.00, "", current_timestamp, 'processing')
  , (3, "user3-real-name", "0000000013333-3", 33.00, "", current_timestamp, 'processing')
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
WHERE table_schema = 'payment_db'
;
