from typing import List, NamedTuple

from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "payment-mysql"
MYSQL_PORT = 3306

DB_NAME = "payment_db"

QUERY_INSERT_TRANSACTIONS = """
INSERT INTO transactions (
  payment_id
  , card_holder_name
  , card_number
  , price
  , 3rd_party_transaction_id
  , initiated_at
  , status
) VALUES
  (%s, %s, %s, %s, %s, %s, %s)
;
"""

QUERY_UPDATE_TRANSACTIONS="""
UPDATE transactions
SET
  3rd_party_transaction_id = %s
  , status = %s
WHERE
  payment_id = %s
"""

class QueryExecutor:

    @staticmethod
    def _start_connection() -> MySQLConnection:
        return MySQLConnection(
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            database=DB_NAME,
        )

    @classmethod
    def insert_transaction(
        cls,
        payment_id: int,
        card_holder_name: str,
        card_number: str,
        price: float,
        third_party_transaction_id: str,
        initiated_at: str,
        status: str,
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_INSERT_TRANSACTIONS,
            (
                payment_id, 
                card_holder_name, 
                card_number, 
                price, 
                third_party_transaction_id, 
                initiated_at, 
                status,
            )
        )
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count
    
    @classmethod
    def update_transaction(
        cls,
        payment_id: int,
        third_party_transaction_id: str,
        status: str
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_UPDATE_TRANSACTIONS,
            (
                third_party_transaction_id,
                status,
                payment_id, 
            )
        )
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count
