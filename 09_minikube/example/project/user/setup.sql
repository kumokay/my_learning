/*
export MYSQLHOST=<cluster ip>
mysql --host=$MYSQLHOST --port=3306 --user=root --password=mypassword < setup.sql
*/

/*
setup user_db
*/
DROP DATABASE user_db
;

CREATE DATABASE user_db
DEFAULT CHARACTER SET utf8
COLLATE utf8_unicode_ci
;

USE user_db
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

CREATE TABLE credit_cards (
  PRIMARY KEY (id)
  , id INT NOT NULL AUTO_INCREMENT
  , user_id INT NOT NULL
  , card_holder_name VARCHAR(32)
  , card_number VARCHAR(16)
  , is_default_payment BOOLEAN
  , CONSTRAINT credit_cards_user_id_fk
    FOREIGN KEY (user_id) REFERENCES users (id)
)
;

INSERT INTO credit_cards (
  user_id
  , card_holder_name
  , card_number
  , is_default_payment
) VALUES
  (1, "user1-real-name","000000001111-1", true)
  , (1, "user1-real-name","000000001111-2", false)
  , (1, "user1-real-name","000000001111-3", false)
  , (2, "user2-real-name","000000002222-1", true)
  , (2, "user2-real-name","000000002222-2", false)
  , (3, "user3-real-name","000000003333", true)
  , (4, "user4-real-name","000000004444", true)
  , (5, "user5-real-name","000000005555", true)
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
WHERE table_schema = 'user_db'
;