from typing import List, NamedTuple

from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "payment-mysql"
MYSQL_PORT = 3306

DB_NAME = "payment_db"

QUERY_SELECT_TRANSACTION_BY_PAYMENTID = """
SELECT
  id
  ,payment_id
  , third_party_transaction_id
  , status
FROM transactions
WHERE 
  payment_id = %s
;
"""

QUERY_SELECT_TRANSACTION_BY_STATUS = """
SELECT
  id
  , payment_id
  , third_party_transaction_id
  , status
FROM transactions
WHERE 
  status = %s
LIMIT %s
;
"""

class TransactionObj(NamedTuple):
    id: int
    payment_id: int
    third_party_transaction_id: str
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
    def select_transaction_by_status(
        cls,
        status: str,
        limit: int
    ) -> List[TransactionObj]:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_SELECT_TRANSACTION_BY_STATUS,
            (status, limit)
        )
        rows = cursor.fetchall()

        result = [
            TransactionObj(
                id=id,
                payment_id=payment_id,
                third_party_transaction_id=third_party_transaction_id,
                status=status,
            ) for (
                id, 
                payment_id, 
                third_party_transaction_id, 
                status
            ) in rows
        ]

        cursor.close()
        cnx.close()

        return result
    
    @classmethod
    def select_transaction_by_payment_id(
        cls,
        payment_id: int,
    ) -> List[TransactionObj]:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_SELECT_TRANSACTION_BY_PAYMENTID,
            (payment_id, )
        )
        rows = cursor.fetchall()

        result = [
            TransactionObj(
                id=id,
                payment_id=payment_id,
                third_party_transaction_id=third_party_transaction_id,
                status=status,
            ) for (
                id, 
                payment_id, 
                third_party_transaction_id, 
                status
            ) in rows
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
