/*
export MYSQLHOST=<cluster ip>
mysql --host=$MYSQLHOST --port=3306 --user=root --password=mypassword < setup.sql
*/

/*
setup product_db
*/
DROP DATABASE product_db
;

CREATE DATABASE product_db
DEFAULT CHARACTER SET utf8
COLLATE utf8_unicode_ci
;

USE product_db
;

CREATE TABLE users (
  PRIMARY KEY (id)
  , id INT NOT NULL AUTO_INCREMENT
  , name VARCHAR(255) NOT NULL
  , email VARCHAR(255) NOT NULL
  , UNIQUE KEY users_email_uidx (email)
)
;

INSERT INTO users (
  name
  , email
) VALUES
  ('user1', 'user1@email')
  , ('user2', 'user2@email')
  , ('user3', 'user3@email')
  , ('user4', 'user4@email')
  , ('user5', 'user5@email')
;

CREATE TABLE products (
  PRIMARY KEY (id)
  , id INT NOT NULL AUTO_INCREMENT
  , name VARCHAR(255) NOT NULL
  , price DECIMAL(15, 2) NOT NULL
  , seller_id INT NOT NULL
  , is_active BOOLEAN DEFAULT true
  , CONSTRAINT products_seller_id_fk
    FOREIGN KEY (seller_id) REFERENCES users (id)
)
;

INSERT INTO products (
  name
  , price
  , seller_id
) VALUES
  ('prod1_from_user1', 3.99, 1)
  , ('prod2_from_user1', 2.99, 1)
  , ('prod3_from_user1', 4.99, 1)
  , ('prod4_from_user2', 399.99, 2)
  , ('prod5_from_user3', 10.99, 3)
  , ('prod6_from_user3', 123.45, 3)
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
WHERE table_schema = 'product_db'
