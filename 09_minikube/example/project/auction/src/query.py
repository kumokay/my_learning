from typing import List, NamedTuple

from mysql.connector.connection import MySQLConnection

MYSQL_USER = "root"
MYSQL_PASSWORD = "mypassword"
MYSQL_HOST = "auction-mysql"
MYSQL_PORT = 3306

DB_NAME = "auction_db"

QUERY_INSERT_AUCTION = """
INSERT INTO auctions (
  name
  , start_price
  , seller_id
  , start_at
  , end_at
  , status
) VALUES
  (%s, %s, %s, %s, %s, %s)
;
"""

QUERY_SELECT_AUCTION = """
SELECT
  id
  , name
  , start_price
  , seller_id
  , start_at
  , end_at
  , status
FROM
  auctions
WHERE id >= %s
  AND status = %s
ORDER BY id
LIMIT %s
;
"""

QUERY_UPDATE_PAYMENT="""
UPDATE payments
SET
  status = %s
WHERE
  id = %s
"""

QUERY_INSERT_PAYMENT = """
INSERT INTO payments (
  bid_id
  , auction_id
  , user_id
  , price
  , created_at
  , status
) VALUES
  (%s, %s, %s, %s, %s, %s)
;
"""

class AuctionObj(NamedTuple):
    id: int
    name: str
    start_price: float
    seller_id: int
    start_at: str
    end_at: str
    status: str


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
    def create_auction(
        cls,
        auction_name: str,
        seller_id: int,
        start_price: float,
        start_at: str,
        end_at: str,
        status: str
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_INSERT_AUCTION, 
            (
                auction_name, 
                start_price,
                seller_id,
                start_at,
                end_at,
                status,
            ),
        )
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count
    
    @classmethod
    def get_auctions(
        cls,
        next_auction_id: int,
        status_filter: str,
        limit: int,
    ) -> List[AuctionObj]:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_SELECT_AUCTION, 
            (next_auction_id, status_filter, limit),
        )
        rows = cursor.fetchall()

        result = [
            AuctionObj(
                id=id,
                name=name,
                start_price=float(start_price),  # convert Decimal to float,
                seller_id=seller_id,
                start_at=str(start_at),  # convert Datetime to str,
                end_at=str(end_at),  # convert Datetime to str,
                status=status,
            ) for (
                id, 
                name, 
                start_price,
                seller_id,
                start_at, 
                end_at, 
                status,
            ) in rows
        ]

        cursor.close()
        cnx.close()

        return result
    
    @classmethod
    def update_payments(
        cls,
        payment_ids,
        status,
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        for payment_id in payment_ids:
          cursor.execute(
              QUERY_UPDATE_PAYMENT, (status, payment_id),
          )
        cnx.commit()
        cnx.close()

        count = cursor.rowcount
        cursor.close()

        return count
    
    @classmethod
    def create_payment(
        cls,
        bid_id: int,
        auction_id: int,
        user_id: int,
        price: float,
        created_at: str,
        status: str,
    ) -> int:
        cnx = cls._start_connection()
        cursor = cnx.cursor()
        cursor.execute(
            QUERY_INSERT_PAYMENT, 
            (
              bid_id,
              auction_id,
              user_id,
              price,
              created_at,
              status,
            ),
        )
        cnx.commit()
        cnx.close()

        lastrowid = cursor.lastrowid
        cursor.close()

        return lastrowid
