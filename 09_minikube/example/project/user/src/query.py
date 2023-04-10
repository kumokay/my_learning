from typing import List, NamedTuple

from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "user-mysql"
MYSQL_PORT = 3306

DB_NAME = "user_db"

QUERY_SELECT_CREDIT_CARD = """
SELECT
  card_holder_name
  , card_number
FROM
  credit_cards
WHERE user_id = %s
  AND is_default_payment = true
;
"""


class CreditCardObj(NamedTuple):
    card_holder_name: str
    card_number: str


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
    def get_credit_card(
        cls,
        user_ids: List[int],
    ) -> List[CreditCardObj]:
        result: List[CreditCardObj] = []

        cnx = cls._start_connection()
        cursor = cnx.cursor()
        for user_id in user_ids:
            cursor.execute(QUERY_SELECT_CREDIT_CARD, (user_id, ))
            rows = cursor.fetchall()
            result = result + [
                CreditCardObj(
                    card_holder_name=card_holder_name,
                    card_number=card_number,
                ) for (
                    card_holder_name, 
                    card_number, 
                ) in rows
            ]

        cursor.close()
        cnx.close()

        return result
