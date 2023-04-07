from typing import List, NamedTuple

from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "payment-mysql"
MYSQL_PORT = 3306

DB_NAME = "payment_db"

QUERY_SELECT_TRANSACTION = """
SELECT
  payment_id
  , status
FROM transactions
WHERE 
  payment_id = %s
;
"""

class TransactionObj(NamedTuple):
    payment_id: int
    status: str

QUERY_INSERT_TRANSACTION = """
INSERT INTO transactions (
  payment_id
  , card_holder_name
  , card_number
  , price
  , third_party_transaction_id
  , initiated_at
  , status
) VALUES
  (%s, %s, %s, %s, %s, %s, %s)
;
"""

QUERY_UPDATE_TRANSACTION="""
UPDATE transactions
SET
  third_party_transaction_id = %s
  , status = %s
WHERE
  id = %s
  AND payment_id = %s
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
    def select_transaction(
        cls,
        payment_id: int,
    ) -> List[TransactionObj]:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_SELECT_TRANSACTION,
            (payment_id, )
        )
        rows = cursor.fetchall()

        result = [
            TransactionObj(
                payment_id=payment_id,
                status=status,
            ) for (payment_id, status) in rows
        ]

        cursor.close()
        cnx.close()

        return result

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
            QUERY_INSERT_TRANSACTION,
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

        lastrowid = cursor.lastrowid
        cursor.close()

        return lastrowid
    
    @classmethod
    def update_transaction(
        cls,
        transaction_id: int,
        payment_id: int,
        third_party_transaction_id: str,
        status: str
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_UPDATE_TRANSACTION,
            (
                third_party_transaction_id,
                status,
                transaction_id,
                payment_id, 
            )
        )
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count
